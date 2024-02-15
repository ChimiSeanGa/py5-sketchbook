import py5
import numpy as np
from random import randrange
import math
import cmath
import colorsys

# Given two (possibly overlapping) circles centered at -1 and 1,
# this program draws the exceptional set for an angle and
# number of iterations.
# For more info, see https://vrs.amsi.org.au/wp-content/uploads/sites/92/2020/01/gossow_martin_vrs-report.pdf

theta1 = math.pi/5 # angle of rotation 1
theta2 = -math.pi/7 # angle of rotation 2
iters = 150 # number of iterations to transform each point
rad = 2 # radius of each circle
delta = 0.005 # minimum distance to atom boundary

view_radius = 3.2
view_center = 0

# Rotation transformation of circle centered at -1
def rot1(z):
   if abs(z+1) <= rad:
      return cmath.exp(1j*theta1)*(z+1) - 1
   return z

# Rotation transformation of circle centered at -1
def rot2(z):
   if abs(z-1) <= rad:
      return cmath.exp(1j*theta2)*(z-1) + 1
   return z

# Determine if a complex number z is on the boundary of an atom
def is_near_atom_boundary(z):
   if abs(abs(z+1) - rad) < delta or abs(abs(rot1(z)-1) - rad) < delta:
      return True
   elif abs(abs(z+1) - rad) < delta:
      return True
   elif abs(abs(z-1) - rad) < delta:
      return True
   return False

# Given a complex number z, apply the given transformation
def transform(z):
   if abs(z+1) <= rad and abs(rot1(z)-1) <= rad:
      return rot2(rot1(z))
   elif abs(z+1) <= rad:
      return rot1(z)
   elif abs(z-1) <= rad:
      return rot2(z)
   return z

# Determine the color of the complex number z
def get_color(z):
   if transform(z) == z:
      return py5.color(0, 0, 0)
   w = z
   for n in range(iters):
      if is_near_atom_boundary(w):
         # (r,g,b) = colorsys.hsv_to_rgb(n/iters, 1, 1)
         # return py5.color(255*r, 255*g, 255*b)
         return py5.color(255, 255, 255)
      w = transform(w)
   return py5.color(0, 0, 0)

# Return the complex number corresponding to the given pixel coordinates
def pixel_coord_to_complex(i, j):
   m = min(py5.pixel_width, py5.pixel_height)

   x = (2*i/m-1)*view_radius + view_center.real
   y = -(2*j/m-1)*view_radius + view_center.imag

   return x + y*1j

# Set the pixels of the screen
def set_pixels():
   for j in range(py5.pixel_height):
      for i in range(py5.pixel_width):
         idx = j*py5.pixel_width + i
         z = pixel_coord_to_complex(i, j)
         py5.pixels[idx] = get_color(z)

def setup():
   py5.size(1000, 1000)
   py5.rect_mode(py5.CENTER)

   py5.load_pixels()
   set_pixels()
   py5.update_pixels()
   py5.save("./real_points_1_i.png")

# def draw():
   

py5.run_sketch()