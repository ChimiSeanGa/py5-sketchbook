import py5
import math
import cmath
import numpy as np

# Complex valued function
def f(z):
   return z**3 - 1

# Weierstrass p function for a given lattice
def wp(z, L):
   global lattice_sum_limit
   (w1, w2) = L

   if z == 0:
      return 1E10

   result = 1/z**2
   for m in range(-lattice_sum_limit, lattice_sum_limit+1):
      for n in range(-lattice_sum_limit, lattice_sum_limit+1):
         if m == 0 and n == 0:
            continue
         lattice_pt = m*w1 + n*w2
         if z-lattice_pt == 0:
            return 1E10
         result += 1/(z-lattice_pt)**2 - 1/lattice_pt**2

   return result

# Derivative of Weierstrass p function for a given lattice
def wp_prime(z, L):
   global lattice_sum_limit
   (w1, w2) = L

   result = 0
   for m in range(-lattice_sum_limit, lattice_sum_limit+1):
      for n in range(-lattice_sum_limit, lattice_sum_limit+1):
         lattice_pt = m*w1 + n*w2
         if z-lattice_pt == 0:
            return 1E10
         result += 1/(z-lattice_pt)**3

   return -2*result

# Color the real points of a complex elliptic curve
def real_points(z, L):
   x = wp(z, L)
   y = wp_prime(z, L)

   if abs(x.imag) < 1E-5 and abs(y.imag) < 1E-5:
      return 0
   return 1E10

# Return the color corresponding to the complex number z
def complex_to_color(z):
   saturation = 100
   brightness = 100
   if abs(z) < 1E-1:
      brightness = 100*(abs(z)/1E-1)**0.2
   if abs(z) > 1E2:
      saturation = 100*(1E2/abs(z))**0.5
   arg = cmath.phase(z)
   if arg < 0:
      arg += 2*math.pi
   return py5.color(np.degrees(arg), saturation, brightness)

# Return the complex number corresponding to the given pixel coordinates
def pixel_coord_to_complex(i, j):
   global view_center
   global view_radius

   m = min(py5.pixel_width, py5.pixel_height)

   x = (2*i/m-1)*view_radius + view_center.real
   y = -(2*j/m-1)*view_radius + view_center.imag

   return x + y*1j

# Set the pixels of the screen according to the complex function fun
def set_pixels(fun):
   for j in range(py5.pixel_height):
      for i in range(py5.pixel_width):
         idx = j*py5.pixel_width + i
         z = pixel_coord_to_complex(i, j)
         py5.pixels[idx] = complex_to_color(fun(z))

def setup():
   global view_center
   global view_radius
   global lattice_sum_limit

   py5.size(500, 500)
   py5.frame_rate(60)
   py5.color_mode(py5.HSB, 360, 100, 100)

   view_center = 0.5
   view_radius = 0.5

   lattice_sum_limit = 5

   py5.load_pixels()
   # set_pixels(lambda z : wp(z, (1, 1j)))
   # set_pixels(lambda z : wp_prime(z, (1, 1j)))
   # set_pixels(f)
   set_pixels(lambda z : real_points(z, (1, 1j)))
   py5.update_pixels()
   py5.save("./real_points_1_i.png")

py5.run_sketch()
