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
        
        # set faces
        print(f'-- Grabbing {model_mesh.data['vectors'].shape[0]} triangles...')
        for vector in model_mesh.data['vectors']:
            self.faces.append(Triangle(vector))
        
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

        # print(f'point cloud attr: {self.point_cloud.shape}')

    def remove_dup_points_from_point_cloud(self, q_cloud):
        """
        Remove the duplicate points from a point cloud you are comparing.

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

    def compare_shapes(self, other_shape, athresh=None):
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

# newshape = Shape('model_files/CubeLibre_C.stl')
# # newshape = Shape('model_files/Dice.stl')
# # newshape = Shape('model_files/A38_Flexi_Baby_Dragon_Keychain.stl')

# rivalshape = Shape('model_files/CubeLibre_A.stl')
# # rivalshape = Shape('model_files/A38_Flexi_Baby_Dragon.stl')

# stop = dt.datetime.now()
# print(f'\ntime to load files with triangles and point clouds: {stop-start}')

# # newshape.compare_shapes(rivalshape)
# # rivalshape.compare_shapes(newshape)
# stop = dt.datetime.now()
# print(f'\ntime to compare models: {stop-start}')

