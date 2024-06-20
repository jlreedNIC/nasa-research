import datetime as dt
from shape import Shape
import numpy as np

start = dt.datetime.now()
newshape = Shape('model_files/A38_Flexi_Baby_Dragon_Keychain.stl')
rivalshape = Shape('model_files/A38_Flexi_Baby_Dragon.stl')

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

padding = np.zeros((qcloud.shape[0]-pcloud.shape[0], 3))
pcloud = np.vstack((pcloud, padding))

print(f'{pcloud.shape} <-> {qcloud.shape}')

# # ----- testing scipy procrustes -------
# from scipy.spatial import procrustes
# from scipy.linalg import orthogonal_procrustes
# mtx1, mtx2, disparity = procrustes(pcloud, qcloud)
# print(round(disparity, 3))
# # res, sca = orthogonal_procrustes(pcloud, qcloud)
# # print(sca)
# stop = dt.datetime.now()
# print(f'\ntime to do procrustes: {stop-start}')
# # ------ end scipy procrustes ----------

# ------- testing theochem procrustes library --------

from procrustes import orthogonal, rotational, generic
# rotational procrustes on pcloud qcloud
result_rot = rotational(pcloud, qcloud, translate=True, scale=False)

# orthogonal procrustes
result_ortho = orthogonal(pcloud, qcloud, translate=True, scale=False)

# generic
result_gen = generic(pcloud, qcloud, translate=True, scale=False)

print(f'Rotational: {result_rot.error}')
print(f'Orthogonal: {result_ortho.error}')
print(f'Generic: {result_gen.error}')

transformed = np.dot(result_rot.new_a, result_rot.t)
sumofsquares=np.mean(np.sum((transformed - result_rot.new_b)**2, axis=1))
rmsd_after_rot = np.sqrt(np.mean(np.sum((transformed - result_rot.new_b)**2, axis=1)))
print(f'rmsd rotation: {round(rmsd_after_rot, 3)} M^2: {round(sumofsquares,3)}')

transformed = np.dot(result_ortho.new_a, result_ortho.t)
sumofsquares=np.mean(np.sum((transformed - result_ortho.new_b)**2, axis=1))
rmsd_after_ortho = np.sqrt(np.mean(np.sum((transformed - result_ortho.new_b)**2, axis=1)))
print(f'rmsd orthogonal: {round(rmsd_after_ortho, 3)} M^2: {round(sumofsquares,3)}')

transformed = np.dot(result_gen.new_a, result_gen.t)
sumofsquares=np.mean(np.sum((transformed - result_gen.new_b)**2, axis=1))
rmsd_after_gen = np.sqrt(np.mean(np.sum((transformed - result_gen.new_b)**2, axis=1)))
print(f'rmsd orthogonal: {round(rmsd_after_gen, 3)} M^2: {round(sumofsquares,3)}')

stop = dt.datetime.now()
print(f'\ntime to do procrustes: {stop-start}')

# ------- end theochem procrustes library --------