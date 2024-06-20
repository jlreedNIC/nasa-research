# import numpy
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot as plt

def open_stl_model(model_file):
    model_mesh = mesh.Mesh.from_file(model_file)
    return model_mesh

def show_3d_model(model_mesh):
    if type(model_mesh) == str:
        print('Need to load file first. Opening...')
        model_mesh = open_stl_model(model_mesh)
    
    # Create a new plot
    figure = plt.figure(f'3D Model')
    axes = figure.add_subplot(projection='3d')
    

    # Load the STL files and add the vectors to the plot
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(model_mesh.vectors))

    # Auto scale to the mesh size
    scale = model_mesh.points.flatten()
    axes.auto_scale_xyz(scale, scale, scale)

    # Show the plot to the screen
    plt.show()
 
# ----- main test -------
   
# show_3d_model('Dice.stl')
your_mesh = open_stl_model('model_files/CubeLibre_C.stl')

volume, cog, inertia = your_mesh.get_mass_properties()
print("Volume                                  = {0}".format(volume))
print("Position of the center of gravity (COG) = {0}".format(cog))
print("Inertia matrix at expressed at the COG  = {0}".format(inertia[0,:]))
print("                                          {0}".format(inertia[1,:]))
print("                                          {0}".format(inertia[2,:]))

# print(your_mesh.info)
# print(your_mesh.name)
# show_3d_model(your_mesh)


# print(your_mesh.normals)
print(f'Normals: {your_mesh.normals.shape}')
print(f'Num of facets: {your_mesh.normals.shape[0]}')
# print(your_mesh.normals)

print(f"\nVectors: {your_mesh.data['vectors'].shape}")
triangle = your_mesh.data['vectors'][0]
vertex = triangle[0]
print(triangle, vertex)
# print(your_mesh.data['vectors'])

print(f"\n{your_mesh.v0}")