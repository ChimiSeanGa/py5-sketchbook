import py5
import random
import numpy as np
import math
import cv2

num_rows = 80
points = np.zeros((num_rows,num_rows), dtype='f,f')

# Transform a point from uniform coordinates to pixel coordinates
def pixel_coords(pt):
   return ((pt[0]+1)*py5.width/2, (pt[1]+1)*py5.height/2)

# Transform a list of points to pixel coordinates.
def pixel_coords_list(pts):
   return [pixel_coords(pt) for pt in pts]

# Transform a point from pixel coordinates to uniform coordinates
def uniform_coords(pt):
   return (pt[0]*2/py5.width - 1, pt[1]*2/py5.height - 1)

# Transform a list of points to uniform coordinates.
def uniform_coords_list(pts):
   return [uniform_coords(pt) for pt in pts]

# Trivial grid of points, centered in each cell.
def uniform_points():
   x = np.linspace(-1, 1, num_rows)
   y = np.linspace(-1, 1, num_rows)
   xv, yv = np.meshgrid(x, y)
   for j in range(num_rows):
      for i in range(num_rows):
         points[j,i] = (xv[j,i],yv[j,i])

# Apply a radial warp centered at c to the points grid with distortion factor k
def radial_warp(c, k):
   for j in range(num_rows):
      for i in range(num_rows):
         pt = points[j,i]
         ru = math.dist(pt, c)
         rd = ru/(1+k/(ru*10)**2)
         new_pt = ((pt[0]-c[0])/ru*rd + c[0],(pt[1]-c[1])/ru*rd + c[1])
         points[j,i] = new_pt

# For each point within a distance d of the center point c,
# adjust the distance to c by a factor of 1/k.
def radial_compactify(c, d, k):
   for j in range(num_rows):
      for i in range(num_rows):
         pt = points[j,i]
         ru = math.dist(pt, c)
         rd = ru
         if ru < d:
            t = ru/d
            rd = ru*t + ru/k*(1-t)
         new_pt = ((pt[0]-c[0])/ru*rd + c[0],(pt[1]-c[1])/ru*rd + c[1])
         points[j,i] = new_pt

# Given a list of vertices, interpolate them with curves.
# Vertices should be in pixel coordinates.
def curve_interpolation(vertices):
   py5.no_fill()
   py5.begin_shape()
   py5.curve_vertex(vertices[0][0], vertices[0][1])
   for i in range(len(vertices)):
      py5.curve_vertex(vertices[i][0], vertices[i][1])
   py5.curve_vertex(vertices[-1][0], vertices[-1][1])
   py5.end_shape()

# Get the coordinates of the darkest pixels in an image.
def get_black_pixel_coords(img_name):
   img = cv2.imread(img_name)
   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   threshold = 10
   coords = np.column_stack(np.where(gray < threshold))
   return coords

def setup():
   # py5.size(4094, 4094, py5.SVG, 'yinyang_moire.svg')
   py5.size(1000, 1000)
   py5.no_fill()
   py5.background(255)

   uniform_points()
   # radial_compactify((0,0), 0.5, 2)
   
   # pinch_coords = uniform_coords_list(get_black_pixel_coords('selfie1.jpg'))
   # step = 200
   # for i in range(0, len(pinch_coords), step):
   #    radial_compactify(pinch_coords[i][::-1], 0.05, 1.2)

   for i in range(num_rows):
      curve_interpolation(pixel_coords_list(points[i]))
      curve_interpolation([pixel_coords(points[j,i]) for j in range(num_rows)])

   py5.save('grid.jpg')
   py5.exit_sketch()
   

py5.run_sketch()