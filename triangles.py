# ------------------------
# @file     triangles.py
# @date     June 2024
# @author   Jordan Reed
# @email    reed5204@vandals.uidaho.edu
# @brief    for creating/comparing stl models
# ------------------------

import numpy as np

class Triangle:
    def __init__(self, verts=[]):
        
        self.vertices = np.empty((3,3))
        self.edges = np.empty((1,3))        # contain lengths of edges??

        self.set_vertices(verts)
    
    def set_vertices(self, verts=[]):
        if type(verts) == list:
            if verts == []:
                self.vertices = np.zeros((3,3))
            else:
                right_size = True
                if len(verts) != 3:
                    right_size = False
                for vert in verts:
                    if len(vert) != 3:
                        right_size = False
                        break
                if not right_size:
                    print(f'Your list of vertices is not the right size.')
                    exit(1)

                self.vertices = np.array(verts, np.float32)
        else:
            self.vertices = verts
        
    def print(self):
        print(self.vertices)


# ----- testing ------
test = np.array([[1,2,3],[2,3,4],[4,5,6]])
# print(test.shape, test)
ntriangle = Triangle()
ntriangle.set_vertices(test)
ntriangle.print()

