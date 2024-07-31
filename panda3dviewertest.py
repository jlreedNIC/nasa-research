# ------------------------
# @file     panda3dviewertest.py
# @date     June 2024
# @author   Jordan Reed
# @email    reed5204@vandals.uidaho.edu
# @brief    for testing a procrustes viewing implementation in the panda3d viewer library
# ------------------------

import numpy as np
import time
from shape import Shape
from panda3d_viewer import Viewer, ViewerConfig
from procrustes import generic, rotational

def show_point_cloud(cloud, colors):
    print('showing point cloud')

    # make model fit in window by shrinking/expanding as needed
    print(f'model max: {np.max(cloud)}')
    if np.max(cloud) < 10:
        # scale model up
        vertices = cloud*10
    elif np.max(cloud) > 100:
        # scale model down
        vertices = cloud/100
    else:
        vertices = cloud
    
    # convert array to float32 then uint32 to ensure viewer processes correctly
    vertices = np.array(vertices, np.float32)
    vertices = vertices.view(dtype=np.uint32)

    if not isinstance(cloud, np.ndarray):
        print('issue found')

    # create window
    with Viewer(show_grid=False) as viewer:
        viewer.reset_camera((10, 10, 15), look_at=(0, 0, 0))
        viewer.append_group('root')
        viewer.append_cloud('root', 'cloud', thickness=4)

        while True:
            viewer.set_cloud_data('root', 'cloud', vertices, colors)
            time.sleep(0.03)

def pad_point_cloud(orig_cloud, other_cloud):
    # pad shapes

    padding = np.zeros(( np.abs(orig_cloud.shape[0]-other_cloud.shape[0]), 3))
    
    # if orig smaller than other
    if orig_cloud.shape[0] < other_cloud.shape[0]:
        print('orig is smaller')
        orig_cloud = np.concatenate((orig_cloud, padding))
    else:
        print('other cloud smaller')
        other_cloud = np.concatenate((other_cloud, padding))
    
    return orig_cloud, other_cloud
    
def compare_with_procrustes(orig_point_cloud, other_point_cloud, scale=False, threshhold=.005, rounding=4):
    """
    Compares 2 point clouds using the Procrustes method. Then compares computed point clouds to see how close each model is. Also computes frobenius norm, and root mean squared error. Accuracy score is based off threshold passed in. Can include scaling or not (see procrustes for more explanation). 

    # NOTES: threshhold of approximate closeness needs adjusting. Not accurate for all models. Need way to measure accurate measure also.

    :param other_shape: model to compare to, used as reference model
    :param scale: whether or not to allow scaling, defaults to False
    :param threshhold: determines how close points are to determine if they 'match' for accuracy score, defaults to .005
    :param rounding: how many decimals to round to, defaults to 4
    :return: frobenius norm, root mean squared error, 'accuracy' score
    """
    result = rotational(orig_point_cloud, other_point_cloud, translate=True, scale=scale, pad=True)
    
    frob_error = np.round(result.error, 4)
    
    # new reference matrix
    new_b = np.round(result.new_b, rounding)

    # transformed matrix p
    transformed = np.dot(result.new_a, result.t)
    transformed = np.round(transformed, rounding)

    # get error for every value
    error = transformed-result.new_b
    error = np.round(error, rounding)
    # print(f'max error: {np.max(error)} {np.min(error)} shape: {error.shape}')
    # print(f'row 1: {error[0]}')

    # find distance between points
    squared_dist = np.sum((transformed-new_b)**2, axis=1)
    dist = np.round(np.sqrt(squared_dist), rounding)
    print(f'shape: {dist.shape} max dist: {np.max(dist)} min dist: {np.min(dist)}')
    
    # get root mean squared error (standard deviation of all errors)
    rmse = np.sqrt(np.mean(np.sum((error)**2, axis=1)))
    rmse = np.round(rmse, rounding)
    print(f'rmse: {rmse}')

    # root mean squared distance
    rmsd = np.sqrt(np.sum(dist**2)/dist.shape[0])
    rmsd = np.round(rmsd, rounding)
    print(f'rmsd: {rmsd}')

    # find which match
    approx_match = dist < rmsd
    matched = dist <= .001
    no_match = dist >= rmsd
    # print(dist[no_match])
    print('approx match shape', approx_match.shape, matched.shape)

    # give accuracy measure
    count_matched = np.count_nonzero(matched)

    # approx_match = error <= rmse
    count_approx_match = np.count_nonzero(approx_match)

    comparison_score = np.round(count_approx_match/transformed.shape[0],rounding)

    print(f'matched: {count_matched} approx match: {count_approx_match}')
    print(f'total: {transformed.shape[0]}')
    print(f'Frobenius score: {frob_error} RMSE: {rmse} Score: {comparison_score*100}%')
    return approx_match, matched, transformed, result.new_a, result.new_b

def create_color_arrays(orig_array, other_array, indices_of_approx_match, indices_of_match):
    # create color array for display
    colors_of_orig = np.ones((orig_array.shape[0], 4), np.float32)

    indices_of_no_match = np.invert(indices_of_match)
    colors_of_orig[indices_of_no_match,:] = np.array([1,.5,0,3])                    # orange
    colors_of_orig[indices_of_approx_match,:] = np.array([.75,.75,.5,3])     # light green
    colors_of_orig[indices_of_match, :] = np.array([0,0,1,3])                # blue

    # color array for other shape
    colors_of_other = np.ones((other_array.shape[0], 4), np.float32)
    colors_of_other[indices_of_no_match,:] = np.array([1,0,0,3])                   # red
    colors_of_other[indices_of_approx_match,:] = np.array([.72,.62,.32,3])  # light brown
    colors_of_other[indices_of_match, :] = np.array([0,1,0,3])              # green

    shape = np.vstack((other_array, orig_array))
    all_colors = np.vstack((colors_of_other, colors_of_orig))

    return shape, all_colors, colors_of_orig, colors_of_other


# ----- testing -------

def main():
    # open files
    # newshape = Shape('model_files/shaft_mod.stl')
    # rivalshape = Shape('model_files/shaft_orig_2.stl')

    newshape = Shape('model_files/APC_orig_propeller.stl')
    rivalshape = Shape('model_files/APC_heavily_mod_propeller.stl')

    # pad point clouds with 0's
    orig_padded, other_padded = pad_point_cloud(newshape.point_cloud, rivalshape.point_cloud)
    # perform procrustes
    indices_of_approx_match, indices_of_match, transformed, newa, newb = compare_with_procrustes(newshape.point_cloud, rivalshape.point_cloud, scale=False)#, threshhold=.0005)
    # indices_of_match, indices_of_approx_match = newshape.compare_point_clouds(rivalshape)
    shape, all_colors, orig_colors, other_colors = create_color_arrays(newb, transformed, indices_of_approx_match, indices_of_match)


    # show_point_cloud(orig_padded, orig_colors)
    # show_point_cloud(other_padded, other_colors)
    show_point_cloud(shape, all_colors)

    # overlap_origs = np.vstack((transformed, newb))
    # show_point_cloud(overlap_origs, all_colors)

# main()