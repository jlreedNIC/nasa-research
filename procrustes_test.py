import datetime as dt
from shape import Shape
import numpy as np

def frobenius_norm(matrix):
    res = np.sqrt(np.sum((matrix)**2))
    return res**2

start = dt.datetime.now()
# newshape = Shape('model_files/A38_Flexi_Baby_Dragon_Keychain.stl')
# rivalshape = Shape('model_files/A38_Flexi_Baby_Dragon.stl')

newshape = Shape('model_files/APC_orig_propeller.stl')
# newshape = Shape('model_files/APC_mod_propeller.stl')
rivalshape = Shape('model_files/APC_orig_propeller.stl')
# rivalshape = Shape('model_files/APC_mod_propeller.stl')
# rivalshape = Shape('model_files/APC_heavily_mod_propeller.stl')

# newshape = Shape('model_files/Dice.stl')
# newshape = Shape('model_files/CubeLibre_C.stl')
# rivalshape = Shape('model_files/CubeLibre_A.stl')
# rivalshape = Shape('model_files/CubeLibre_C.stl')
# rivalshape = Shape('model_files/Dice.stl')

# stop = dt.datetime.now()
# print(f'\ntime to load files with triangles and point clouds: {stop-start}')

# pad smaller point cloud to match shape of larger point cloud
print(newshape.point_cloud.shape, rivalshape.point_cloud.shape)
if newshape.point_cloud.shape[0] < rivalshape.point_cloud.shape[0]:
    pcloud = np.copy(newshape.point_cloud)
    qcloud = np.copy(rivalshape.point_cloud)
else:
    pcloud = np.copy(rivalshape.point_cloud)
    qcloud = np.copy(newshape.point_cloud)

# padding = np.zeros((qcloud.shape[0]-pcloud.shape[0], 3))
# pcloud = np.vstack((pcloud, padding))

# print(f'{pcloud.shape} <-> {qcloud.shape}')

# ------- testing theochem procrustes library --------

from procrustes import orthogonal, rotational, generic

def compare_with_procrustes(pcloud, qcloud, scale=False, threshhold=.005, rounding=4):
    """
    Compares 2 point clouds using the Procrustes method. Then compares computed point clouds to see how close each model is. Also computes frobenius norm, and root mean squared error. Accuracy score is based off threshold passed in. Can include scaling or not (see procrustes for more explanation). 

    :param pcloud: point cloud of first model, to fit to other model
    :param qcloud: point cloud of second model, used as reference model
    :param scale: whether or not to allow scaling, defaults to False
    :param threshhold: determines how close points are to determine if they 'match' for accuracy score, defaults to .005
    :param rounding: how many decimals to round to, defaults to 4
    :return: frobenius norm, root mean squared error, 'accuracy' score
    """
    result = generic(pcloud, qcloud, translate=True, scale=scale)
    frob_error = np.round(result.error, 4)

    # new reference matrix
    new_b = np.round(result.new_b, rounding)

    # transformed matrix p
    transformed = np.dot(result.new_a, result.t)
    transformed = np.round(transformed, rounding)

    # get root mean squared error (standard deviation of all errors)
    rmse = np.sqrt(np.mean(np.sum((transformed-result.new_b)**2, axis=1)))
    rmse = np.round(rmse, rounding)

    # give accuracy measure
    # find error=0
    matched = transformed == new_b
    count_matched = np.count_nonzero(matched.all(1))

    approx_match = np.round((transformed-result.new_b),rounding) <= threshhold
    count_approx_match = np.count_nonzero(approx_match.all(1))

    comparison_score = np.round(count_approx_match/transformed.shape[0],rounding)

    # print(f'matched: {count_matched} approx match: {count_approx_match}')
    # print(f'total: {transformed.shape[0]}')
    # print(f'Frobenius score: {frob_error} RMSE: {rmse} Score: {comparison_score*100}%')

    return frob_error, rmse, comparison_score
compare_with_procrustes(pcloud, qcloud)
# # rotational procrustes on pcloud qcloud
# result_rot = rotational(pcloud, qcloud, translate=True, scale=False)

# # orthogonal procrustes
# result_ortho = orthogonal(pcloud, qcloud, translate=True, scale=False)

# # generic
# result_gen = generic(pcloud, qcloud, translate=True, scale=False)

# print(f'Rotational: {result_rot.error}')
# print(f'Orthogonal: {result_ortho.error}')
# print(f'Generic: {result_gen.error}')
# # print(result_gen)
# transformed_rot = np.dot(result_rot.new_a, result_rot.t)
# transformed_ortho = np.dot(result_ortho.new_a, result_ortho.t)
# transformed_gen = np.dot(result_gen.new_a, result_gen.t)

# rmsd = np.round(np.sqrt(np.mean(np.sum((transformed_rot-result_rot.new_b)**2, axis=1))),4)
# print('rmsd: ', rmsd)

# # find where transformed matches new_b
# # print(np.round(transformed_rot, 4)[0])
# # print(np.round(result_rot.new_b, 4)[0])
# # print(np.round(transformed_rot, 4)[0] - np.round(result_rot.new_b, 4)[0])
# res_rot = np.round(transformed_rot, 4)==np.round(result_rot.new_b,4)
# approx_res_rot = np.round((transformed_rot-result_rot.new_b),5)<=rmsd
# # print(transformed_rot-result_rot.new_b)
# res_ortho = transformed_ortho==result_ortho.new_b
# res_gen = transformed_gen==result_gen.new_b

# # print(res_rot)
# # print('if all rows are true: ', res_rot.all(1))
# # print('how many are true: ', np.count_nonzero(res_rot.all(1)))
# # print(res_rot.all(1).count())
# print(f'rounded then compared: {np.count_nonzero(res_rot.all(1))}')
# print('how many are approx close: ', np.count_nonzero(approx_res_rot.all(1)))
# print(f'total points: {approx_res_rot.shape[0]} {result_rot.new_b.shape[0]} {qcloud.shape[0]}')
# print(f'percent close: {(np.count_nonzero(approx_res_rot.all(1))/approx_res_rot.shape[0])*100:.2f}%')
# # print(np.count_nonzero(res_gen.all(1)))
# # print(transformed_rot.shape[0])


stop = dt.datetime.now()
print(f'\ntime to do procrustes: {stop-start}')

# ------- end theochem procrustes library --------

# # ------ testing personal compare -------
# newshape.compare_shapes(rivalshape, 5)
# stop = dt.datetime.now()
# print(f'\ntime to do comparison: {stop-start}')
# # ------ end personal compare func -------