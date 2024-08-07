import py5
import numpy as np
from scipy.spatial import Voronoi
from random import randrange

# This program generates a Voronoi diagram by randomly picking a number of
# points in the box [-1,1] x [-1,1].

# Generate num_points points in the box [-1,1] x [-1,1]
def random_points(num_points):
   return np.array([[randrange(-1, 1), randrange(-1, 1)]
      for n in range(num_points)])

points = random_points(50)
vor = Voronoi(points)

def draw_region(region):
   for i in region:
      vert = vor.vertices[i]

def setup():
   py5.size(500, 500)
   py5.rect_mode(py5.CENTER)

def draw():
   py5.rect(py5.mouse_x, py5.mouse_y, 10, 10)

py5.run_sketch()