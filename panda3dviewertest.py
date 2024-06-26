import numpy as np
import time
from shape import Shape
from panda3d_viewer import Viewer, ViewerConfig

newshape = Shape('model_files/APC_orig_propeller.stl')
rivalshape = Shape('model_files/APC_heavily_mod_propeller.stl')

indices_of_approx_match, indices_of_match, transformed = newshape.compare_with_procrustes(rivalshape, scale=True)#, threshhold=.0005)

# pad shapes
pcloud = []
qcloud = []
if newshape.point_cloud.shape[0] < rivalshape.point_cloud.shape[0]:
    print('pcloud is original')
    pcloud = np.copy(newshape.point_cloud)
    qcloud = np.copy(rivalshape.point_cloud)
else:
    print('pcloud is new shape')
    qcloud = np.copy(newshape.point_cloud)
    pcloud = np.copy(rivalshape.point_cloud)

# pad it
padding = np.zeros((qcloud.shape[0]-pcloud.shape[0], 3))
pcloud = np.vstack((pcloud, padding))


colors_of_approx = np.ones((pcloud.shape[0], 4), np.float32)
# print(colors_of_approx)
# print(colors_of_approx.shape, np.count_nonzero(indices_of_approx_match))

indices_of_no_match = np.invert(indices_of_approx_match.all(1))
colors_of_approx[indices_of_no_match,:] = np.array([1,0,0,3])
colors_of_approx[indices_of_approx_match.all(1),:] = np.array([0.85,1,.64,3])
colors_of_approx[indices_of_match.all(1), :] = np.array([0,1,0,3])
# print(colors_of_approx)
# print(colors_of_approx[indices_of_approx_match])

shape = np.vstack((pcloud, qcloud))
print(shape.shape, pcloud.shape, qcloud.shape)
shape = np.concatenate((pcloud, qcloud))
# shape = np.ones((pcloud.shape[0]+qcloud.shape[0],3), np.float32)
color_copy = np.copy(colors_of_approx)
all_colors = np.ones((shape.shape[0], 4), np.float32)

print(shape.shape)
print(all_colors.shape)

print(qcloud.shape)
print(colors_of_approx.shape)


# print(res.shape)
# print(type(res))
print(np.max(qcloud))
# qcloud = shape

def show_point_cloud(cloud, colors):
    with Viewer(show_grid=False) as viewer:
        viewer.reset_camera((10, 10, 15), look_at=(0, 0, 0))
        viewer.append_group('root')
        viewer.append_cloud('root', 'cloud', thickness=4)

        while True:
            # vertices = np.random.randn(300000, 3).astype(np.float32)
            if np.max(cloud) < 10:
                vertices = cloud*100
            elif np.max(cloud) > 100:
                vertices = cloud/100
            # colors = np.ones((vertices.shape[0], 4), np.float32)
            # colors_of_approx[:, :3] = np.clip(np.abs(vertices), 0, 3) / 3
            viewer.set_cloud_data('root', 'cloud', vertices, colors)
            time.sleep(0.03)

show_point_cloud(qcloud, colors_of_approx)