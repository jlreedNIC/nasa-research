# ------------------------
# @file     triangles.py
# @date     June 2024
# @author   Jordan Reed
# @email    reed5204@vandals.uidaho.edu
# @brief    for creating/comparing stl models
# ------------------------

import numpy as np
import math

class Triangle:
    def __init__(self, verts=[]):
        
        self.vertices = None
        self.edges = None        # contain lengths of edges??
        self.area = None

        self.set_vertices(verts)
        self.edges = self.calculate_edge_lengths()
        self.area = self.calculate_area_of_triangle()
    
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
                    # print(f'Your list of vertices is not the right size.')
                    raise Exception('Your list of vertices is not the right size.')
                    # exit(1)

                self.vertices = np.array(verts, np.float32)
        else:
            self.vertices = verts
        
        self.edges = self.calculate_edge_lengths()
        self.area = self.calculate_area_of_triangle()
    
    def calculate_edge_lengths(self, v1=None, v2=None, v3=None):
        # edge 0 = edge between 0 and 1
        # edge 1 = edge between 0 and 2
        # edge 2 = edge between 1 and 2
        if v1 is None or v2 is None or v3 is None:
            v1 = self.vertices[0]
            v2 = self.vertices[1]
            v3 = self.vertices[2]
        # print(self.edges)
        d1 = math.sqrt( pow((v1[0]-v2[0]), 2) + pow((v1[1]-v2[1]), 2) + pow((v1[2]-v2[2]), 2) )
        d1 = round(d1, 2)

        d2 = math.sqrt( pow((v1[0]-v3[0]), 2) + pow((v1[1]-v3[1]), 2) + pow((v1[2]-v3[2]), 2) )
        d2 = round(d2, 2)

        d3 = math.sqrt( pow((v2[0]-v3[0]), 2) + pow((v2[1]-v3[1]), 2) + pow((v2[2]-v3[2]), 2) )
        d3 = round(d3, 2)

        # print(np.array([d1,d2,d3]))
        return np.array([d1,d2,d3])

    def calculate_area_of_triangle(self, v1=None, v2=None, v3=None):
        if v1 is None or v2 is None or v3 is None:
            v1 = self.vertices[0]
            v2 = self.vertices[1]
            v3 = self.vertices[2]
            if self.edges is None:
                self.edges = self.calculate_edge_lengths()
            edges = self.edges

        edges = self.calculate_edge_lengths(v1, v2, v3)
        s = (edges[0] + edges[1] + edges[2])/2
        area = math.sqrt( s * (s-edges[0]) * (s-edges[1]) * (s-edges[2]))
        return round(area, 2)

    
    def __str__(self):
        return f'{self.vertices} \narea: {self.area} \nedge lengths: {self.edges}'


# ----- testing ------
test = np.array([[1,1,1],[4,3,3],[2,5,5]])
# print(test.shape, test)
ntriangle = Triangle()
ntriangle.set_vertices(test)

ntriangle.calculate_edge_lengths()
ntriangle.calculate_area_of_triangle()

print(ntriangle)


