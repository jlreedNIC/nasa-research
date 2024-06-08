# import numpy
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot as plt
import numpy as np

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

# may not be needed
def isVertexInList(vert, vertList:np.array):
    if vertList.size == 0:
        return False
    for i, entry in enumerate(vertList):
        # for i in range
        # if entry == vert:
        if np.array_equal(vert, entry):
            return i
    return False

def get_list_of_vertices(vectors):
    vert_list = np.copy(vectors)

    # reshape to get a single list of all vertices
    vert_list = np.reshape(vert_list, (vert_list.shape[0]*vert_list.shape[1], 3))

    # remove duplicates
    vert_list = np.unique(vert_list, axis=0)

    return vert_list.tolist()
    list_of_vertices = np.empty((1,3))
    # list_of_vertices = []
    print(f'empty array: {list_of_vertices} size: {list_of_vertices.size}')

    for facet in vectors:
        for vertex in facet:
            print(f'vertex: {vertex} type: {type(vertex)}')
            isInList = isVertexInList(vertex, list_of_vertices)
            print(f'is vertex in list? {isInList}')
            # if vertex not in list_of_vertices:
            if not isVertexInList(vertex, list_of_vertices):
                print(f'----appended: {vertex}')
                list_of_vertices = np.vstack([list_of_vertices, vertex])
                
                # list_of_vertices.append(vertex.tolist())
    print(f'array: {list_of_vertices}')
    
    return list_of_vertices


def compare_models_match_percentage(model1, model2):
    # if filename
    print('Opening files...')
    if type(model1) == str:
        model1 = open_stl_model(model1)
    if type(model2) == str:
        model2 = open_stl_model(model2)

    # get vertices of each model
    print('getting vertices of each model...')
    v1 = model1.data['vectors']
    v2 = model2.data['vectors']
    print(f'model 1 shape: {v1.shape} model 2 shape: {v2.shape}')

    # change numpy array to single list of vertices with no duplicates
    print('remove duplicates and flattening to 2 dimensions...')
    v1_list = get_list_of_vertices(v1)
    v2_list = get_list_of_vertices(v2)
    print(f'model 1 shape: {len(v1_list)} model 2 shape: {len(v2_list)}')

    # count total vertices and total number of duplicates between both models
    # think about just sorting them into two different lists - showing on matplotlib what are dups
    print('counting shared vertices...')
    total_verts = 0
    dup_verts = 0

    for vert in v1_list:
        total_verts += 1
        print(f'vertices compared: {total_verts}')
        if vert in v2_list:
            dup_verts += 1
            v2_list.remove(vert)
    total_verts += len(v2_list)

    print(f'\ndup verts: {dup_verts} total verts: {total_verts}')
    match = dup_verts/total_verts * 100
    print(f'model 1 and 2 match score: {match:.1f}%')

    return match

model1 = "model_files/A38_Flexi_Baby_Dragon_Keychain.stl"
model2 = "model_files/A38_Flexi_Baby_Dragon.stl"
score = compare_models_match_percentage(model1, model2)




