# ------------------------
# @file     shape.py
# @date     June 2024
# @author   Jordan Reed
# @email    reed5204@vandals.uidaho.edu
# @brief    for creating/comparing stl models
# ------------------------

from triangles import Triangle
from stl import mesh
import numpy as np
from procrustes import generic, rotational

class Shape:
    def __init__(self, stl_file):
        self.faces = []       # list of triangles
        self.point_cloud = [] # list of vertices with no duplicates
        self.approx_thresh = 10

        print(f'Starting {stl_file} ...')
        self.open_stl_file(stl_file)
    
    def open_stl_file(self, stl_file):
        """
        Open a STL file and load each triangle into faces list and get list with no duplicates into point_cloud

        :param stl_file: string location of stl file
        """

        model_mesh = mesh.Mesh.from_file(stl_file)
        
        # triangles not needed with procrustes comparison
        # # set faces
        # print(f'-- Grabbing {model_mesh.data['vectors'].shape[0]} triangles...')
        # for vector in model_mesh.data['vectors']:
        #     self.faces.append(Triangle(vector))
        
        # print(f'vector shape: {model_mesh.data['vectors'].shape}')
        # print(f'faces shape: {len(self.faces)}')
        # print(f'first face: {self.faces[0]}')

        # set vertex list
        # get list of vertices
        print(f'-- Getting point cloud...')
        self.point_cloud = np.copy(model_mesh.data['vectors'])
        # make 1x3 dimensional list instead of 3x3
        self.point_cloud = np.reshape(self.point_cloud, (self.point_cloud.shape[0]*self.point_cloud.shape[1], 3))
        # remove duplicate values
        self.point_cloud = np.unique(self.point_cloud, axis=0)

    def compare_with_procrustes(self, other_shape, scale=False, threshhold=.005, rounding=4):
        """
        Compares 2 point clouds using the Procrustes method. Then compares computed point clouds to see how close each model is. Also computes frobenius norm, and root mean squared error. Accuracy score is based off threshold passed in. Can include scaling or not (see procrustes for more explanation). 

        # NOTES: threshhold of approximate closeness needs adjusting. Not accurate for all models. Need way to measure accurate measure also.

        :param other_shape: model to compare to, used as reference model
        :param scale: whether or not to allow scaling, defaults to False
        :param threshhold: determines how close points are to determine if they 'match' for accuracy score, defaults to .005
        :param rounding: how many decimals to round to, defaults to 4
        :return: frobenius norm, root mean squared error, 'accuracy' score
        """
        result = rotational(self.point_cloud, other_shape.point_cloud, translate=True, scale=scale)
        frob_error = np.round(result.error, 4)

        # new reference matrix
        new_b = np.round(result.new_b, rounding)

        # transformed matrix p
        transformed = np.dot(result.new_a, result.t)
        transformed = np.round(transformed, rounding)

        # get error for every value
        error = transformed-result.new_b
        error = np.round(error, rounding)
        print(error)

        # get root mean squared error (standard deviation of all errors)
        rmse = np.sqrt(np.mean(np.sum((error)**2, axis=1)))
        rmse = np.round(rmse, rounding)

        # give accuracy measure
        # find error=0
        matched = transformed == new_b
        count_matched = np.count_nonzero(matched.all(1))

        approx_match = error <= rmse
        count_approx_match = np.count_nonzero(approx_match.all(1))

        comparison_score = np.round(count_approx_match/transformed.shape[0],rounding)

        

        print(f'matched: {count_matched} approx match: {count_approx_match}')
        print(f'total: {transformed.shape[0]}')
        print(f'Frobenius score: {frob_error} RMSE: {rmse} Score: {comparison_score*100}%')
        return approx_match, matched, transformed
        # return frob_error, rmse, comparison_score

    def remove_dup_points_from_point_cloud(self, q_cloud):
        """
        DEPRACATED WITH ADDITION OF PROCRUSTES
        Remove the duplicate points from a point cloud you are comparing your point cloud to.

        :param q_cloud: point cloud of another shape
        :returns
        """
        # model2_dup = []
        # model2_no_dup = []
        model2_dup = np.empty((0,3))
        model2_no_dup = np.empty((0,3))
        print(f'other point cloud size: {q_cloud.shape[0]}')
        print(f'my point cloud size: {self.point_cloud.shape[0]}')

        total_verts = 0
        for vert in q_cloud:
            total_verts += 1
            if (vert==self.point_cloud).all(1).any():
                # model2_dup.append(vert)
                model2_dup = np.vstack((model2_dup, vert))
            else:
                # model2_no_dup.append(vert)
                model2_no_dup = np.vstack((model2_no_dup, vert))
        
        for vert in self.point_cloud:
            if not (vert==q_cloud).all(1).any():
                total_verts += 1
                
        # print(f'dups: {len(model2_dup)} no dups: {len(model2_no_dup)}')
        print(f'dups: {model2_dup.shape[0]} no dups: {model2_no_dup.shape[0]} ({total_verts})')
        return model2_no_dup, model2_dup, total_verts

    def compare_point_clouds(self, other_shape):
        padding = np.zeros(( np.abs(self.point_cloud.shape[0]-other_shape.point_cloud.shape[0]), 3))
        orig_cloud = self.point_cloud
        other_cloud = other_shape.point_cloud
        # if orig smaller than other
        if orig_cloud.shape[0] < other_cloud.shape[0]:
            print('orig is smaller')
            orig_cloud = np.concatenate((orig_cloud, padding))
        else:
            print('other cloud smaller')
            other_cloud = np.concatenate((other_cloud, padding))

        squared_dist = np.sum((self.point_cloud-other_cloud)**2, axis=1)
        dist = np.sqrt(squared_dist)

        matched = dist <= .001
        approx_match = dist <= .01
        no_match = dist > .01

        print(dist[matched])
        return matched, approx_match
    
    def compare_shapes(self, other_shape, athresh=None):
        # DEPRACATED WITH ADDITION OF PROCRUSTES
        if athresh is None:
            athresh=self.approx_thresh
        print('starting comparison...')
        list_no_dups, list_dups, total_points = self.remove_dup_points_from_point_cloud(other_shape.point_cloud)
        match_list = np.empty((0,3))
        approx_list = np.empty((0,3))
        no_match_list = np.empty((0,3))

        print(len(self.faces))
        for i, vert in enumerate(list_no_dups):
            for j in range(i-10, i+10):
            # for j, face in enumerate(self.faces):
                isIn = self.faces[j].isPointInTriangle(vert)
                if isIn:
                    match_list = np.vstack((match_list, vert))
                    break
                else:
                    isClose = self.faces[j].isPointCloseToTriangle(vert, athresh)
                    if isClose:
                        approx_list = np.vstack((approx_list, vert))
                        break
                    # else:
                    #     no_match_list = np.vstack((no_match_list, vert))
        
        print(f'matched: {match_list.shape[0]}')
        print(f'approximately close within {athresh}: {approx_list.shape[0]}')
        # print(f'not close or matched: {no_match_list.shape[0]}')

        # total_points = list_dups.shape[0] + list_no_dups.shape[0]
        total_matched_or_close = list_dups.shape[0] + match_list.shape[0] + (approx_list.shape[0]*.5)
        print(f'score: {total_matched_or_close}/{total_points}={(total_matched_or_close/total_points)*100:.2f}%')
            

# # --------- testing ----------
# import datetime as dt

# start = dt.datetime.now()

# # newshape = Shape('model_files/CubeLibre_C.stl')
# # newshape = Shape('model_files/Dice.stl')
# newshape = Shape('model_files/A38_Flexi_Baby_Dragon_Keychain.stl')

# # rivalshape = Shape('model_files/CubeLibre_A.stl')
# rivalshape = Shape('model_files/A38_Flexi_Baby_Dragon.stl')

# stop = dt.datetime.now()
# print(f'\ntime to load files with triangles and point clouds: {stop-start}')

# start = dt.datetime.now()
# res = newshape.compare_with_procrustes(rivalshape, scale=True)
# stop = dt.datetime.now()
# print(f'time to compare models: {stop-start}')

# print(f"\n{res}")

