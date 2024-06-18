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
        """
        sets the vertices of the triangle. Format is a numpy array shape of (3,3). Calculates the edges and area of triangle based on vertices

        :param verts: can be list, empty, or numpy array. If not empty, must be shape of (3,3)
        :raises Exception: if verts is not right size
        """
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
    
    def calculate_edge(self, v1=None, v2=None):
        """
        Calculates the distance between 2 points in 3D space

        :param v1: point 1, of shape (1,3), defaults to None
        :param v2: point 2, of shape (1,3), defaults to None
        :raises Exception: if values are not given
        :return: distance rounded to 3 decimal points
        """
        if v1 is None or v2 is None:
            raise Exception("Need point/vertex values.")
        
        d1 = math.sqrt( pow((v1[0]-v2[0]), 2) + pow((v1[1]-v2[1]), 2) + pow((v1[2]-v2[2]), 2) )
        
        return round(d1, 3)

    def calculate_edge_lengths(self, v1=None, v2=None, v3=None):
        """
        Calculates all edge distances between 3 points. If no points are given, calculate edge distances for the triangle.

        :param v1: point 1, of shape (1,3), defaults to None
        :param v2: point 2, of shape (1,3), defaults to None
        :param v3: point 3, of shape (1,3), defaults to None
        :return: array of edge distances, 
        where edge[0]=distance between v1 and v2, 
        edge[1]=distance between v1 and v3, and 
        edge[2]=distance between v2 and v3
        """
        if v1 is None or v2 is None or v3 is None:
            v1 = self.vertices[0]
            v2 = self.vertices[1]
            v3 = self.vertices[2]
            
        d1 = self.calculate_edge(v1, v2)
        d2 = self.calculate_edge(v1, v3)
        d3 = self.calculate_edge(v2, v3)

        return np.array([d1,d2,d3])

    def calculate_area_of_triangle(self, v1=None, v2=None, v3=None):
        """
        Calculates the area of a triange in 3D space by first calculating edge distances

        :param v1: _description_, defaults to None
        :param v2: _description_, defaults to None
        :param v3: _description_, defaults to None
        :return: area of triangle rounded to 3 decimal points
        """
        edges = None 
        if v1 is None or v2 is None or v3 is None:
            v1 = self.vertices[0]
            v2 = self.vertices[1]
            v3 = self.vertices[2]
            if self.edges is None:
                self.edges = self.calculate_edge_lengths()
            edges = self.edges

        if edges is None:
            edges = self.calculate_edge_lengths(v1, v2, v3)

        s = (edges[0] + edges[1] + edges[2])/2
        area = math.sqrt( s * (s-edges[0]) * (s-edges[1]) * (s-edges[2]))

        return round(area, 3)
    
    def isPointInTriangle(self, point=None):
        """
        Check to see if the given point is in the triangle, by using the area of the triangle

        :param point: point to check, of shape (1,3), defaults to None
        :raises Exception: if the triangle vertices have not been set
        :raises Exception: if no point is given
        :return: True if point is in triangle, else False
        """
        if self.vertices is None:
            # print('The vertices of the triangle must be set first!')
            raise Exception('The vertices of the triangle must be set first!')
        if point is None:
            raise Exception("'point' cannot be None.")
        if type(point) is list:
            point = np.array(point)
        
        # calculate area of 3 triangles with point and see if they add up to area
        area1 = self.calculate_area_of_triangle(self.vertices[0], self.vertices[1], point)
        area2 = self.calculate_area_of_triangle(self.vertices[0], self.vertices[2], point)
        area3 = self.calculate_area_of_triangle(self.vertices[1], self.vertices[2], point)

        # print(f'{self.area} == ({area1} + {area2} + {area3}) = {area1+area2+area3}')
        return round(self.area,2) == round((area1 + area2 + area3), 2)

    def isPointCloseToTriangle(self, point=None, alpha=.15):
        """
        Checks if a point is 'close' to the triangle by checking the edge distances between the given point and the vertices of the triangle. If the minimum distance away is within a certain threshhold, it is considered close.

        :param point: point to check if close, defaults to None
        :param alpha: threshhold of closeness, defaults to .15
        :raises Exception: vertices of triangle not set
        :raises Exception: no point given
        :return: true if point with threshhold distance away, False if else
        """
        if self.vertices is None:
            # print('The vertices of the triangle must be set first!')
            raise Exception('The vertices of the triangle must be set first!')
        if point is None:
            raise Exception("'point' cannot be None.")
        if type(point) is list:
            point = np.array(point)
        
        # calculate edges and see if it is less than threshold
        edges = [0,0,0]
        for i in range(0, 3):
            # print(f'comparing {point} and {self.vertices[i]}')
            edges[i] = self.calculate_edge(point, self.vertices[i])
        
        print(f'edges: {edges}')
        # print(f'{min(edges)} <= {alpha}')
        return min(edges) <= alpha
    
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

point = [0,0,0]
res = ntriangle.isPointInTriangle(point)
print(f'\nIs point in triangle? {res}')

threshhold = 2
res = ntriangle.isPointCloseToTriangle(point, threshhold)
print(f'Is point within {threshhold} distance of triangle? {res}')


