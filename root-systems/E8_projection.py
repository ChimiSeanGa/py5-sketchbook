import py5
import math
import numpy as np
from itertools import combinations, product

global draw_vectors
global draw_edges
global draw_rings
global colors

# Return distance squared between vertices v1 and v2
def dist_sq(v1, v2):
   return sum([(v1[i]-v2[i])**2 for i in range(len(v1))])

# Return distance between vertex and origin
def radius(v):
   return math.sqrt(v[0]**2 + v[1]**2)

# Generate list of root vectors of E8 root system
def gen_E8_vectors():
   vectors = []
   exps = [0, 1]
   indices = [i for i in range(8)]
   for c in combinations(indices, 2):
      for p in product(exps, repeat=2):
         v = [0 for i in range(8)]
         v[c[0]] = (-1)**(p[0])
         v[c[1]] = (-1)**(p[1])
         vectors.append(v)

   for m in range(5):
      for c in combinations(indices, 2*m):
         v = [0.5 for i in range(8)]
         for k in c:
            v[k] = -0.5
         vectors.append(v)

   return vectors

# Generate list of edges between vectors of E8 root system
def gen_E8_edges(vectors):
   edges = []
   for i in range(len(vectors)):
      for j in range(i+1, len(vectors)):
         v1 = vectors[i]
         v2 = vectors[j]
         if dist_sq(v1, v2) == 2:
            edges.append((i,j))
   return edges

# Return a basis for the Coxeter plane of a given Cartan type
def gen_E8_coxeter_basis():
   # A set of simple roots listed by rows of delta
   delta = np.array([
      [1, -1, 0, 0, 0, 0, 0, 0],
      [0, 1, -1, 0, 0, 0, 0, 0],
      [0, 0, 1, -1, 0, 0, 0, 0],
      [0, 0, 0, 1, -1, 0, 0, 0],
      [0, 0, 0, 0, 1, -1, 0, 0],
      [0, 0, 0, 0, 0, 1, 1, 0],
      [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5],
      [0, 0, 0, 0, 0, 1, -1, 0]
   ])

   # Cartan matrix
   cartan_matrix = delta @ np.transpose(delta)

   # Eigenvalues of Cartan matrix
   eigenvalues, eigenvectors = np.linalg.eigh(cartan_matrix)

   # Get minimal eigenvalue and corresponding eigenvector
   min_vec = eigenvectors[:, 0]

   # Get basis for Coxeter plane
   I = [0, 2, 4, 6]
   J = [1, 3, 5, 7]
   u1 = np.sum([min_vec[i] * delta[i] for i in I], axis=0)
   u2 = np.sum([min_vec[j] * delta[j] for j in J], axis=0)

   # Use Gram-Schmidt to normalize u1 and u2
   u1 = u1 / np.linalg.norm(u1)
   u2 = u2 - np.inner(u1, u2) * u1
   u2 = u2 / np.linalg.norm(u2)

   return (u1, u2)

# Return list of 2-dimensional vectors obtain by projecting the given vectors
# onto the plane given by the Coxeter basis
def project_vectors(vectors, coxeter_basis):
   proj_vecs = []
   (u1, u2) = coxeter_basis
   MT = np.array([u1, u2])
   M = np.transpose(MT)
   A = M @ np.linalg.inv(MT @ M) @ MT
   for v in vectors:
      vec = np.array(v)
      proj_vecs.append(np.ndarray.tolist(MT @ vec))
   return proj_vecs

# The projected vectors occur in circular rings.
# This function returns the collection of rings as a partition
# of the set of vectors.
def get_rings(proj_vectors):
   rings = {}
   for i in range(len(proj_vectors)):
      v = proj_vectors[i]
      r = round(radius(v), 5)
      if r in rings.keys():
         rings[r].append(i)
      else:
         rings[r] = [i]
   return rings

# Return larger radius between two vertices of the given edge
def max_radius(e):
   global draw_vectors
   return max(radius(draw_vectors[e[0]]), radius(draw_vectors[e[1]]))

# Rotate the vectors in a given ring by an angle of theta
def rotate_ring(ring, theta):
   global draw_vectors
   for i in ring:
      v = draw_vectors[i]
      rot_v = [
         math.cos(theta)*v[0] - math.sin(theta)*v[1],
         math.sin(theta)*v[0] + math.cos(theta)*v[1]
      ]
      draw_vectors[i] = rot_v

# Given a list of angles, rotate the corresponding rings
def rotate_rings(sorted_radii, angles):
   global draw_vectors
   global draw_rings
   i = 0
   for r in sorted_radii:
      ring = draw_rings[r]
      rotate_ring(ring, angles[i])
      i += 1

def setup():
   global draw_vectors
   global draw_edges
   global draw_rings
   global colors

   py5.size(500, 500, py5.SVG, 'E8_ring0.svg')
   # py5.frame_rate(60)

   vectors = gen_E8_vectors()
   edges = gen_E8_edges(vectors)
   coxeter_basis = gen_E8_coxeter_basis()

   draw_vectors = project_vectors(vectors, coxeter_basis)
   draw_edges = edges
   draw_rings = get_rings(draw_vectors)
   colors = ["#4287F5", "#48F542", "#F5DD42",
      "#F59842", "#F54242", "#9342F5", "#F542F5", "#27BAC2"]

def draw():
   global draw_vectors
   global draw_edges
   global draw_rings
   global colors

   py5.background('#FFFFFF')
   py5.translate(py5.width/2, py5.height/2)

   m = py5.width/2.5

   # Draw edges in white
   # py5.stroke(255)
   # py5.stroke_weight(0.5)
   # for e in draw_edges:
   #    v = draw_vectors[e[0]]
   #    w = draw_vectors[e[1]]
   #    py5.line(v[0]*m, v[1]*m, w[0]*m, w[1]*m)

   # Draw vertices in white
   # py5.fill(255)
   # for v in draw_vectors:
   #    py5.circle(v[0]*m, v[1]*m, 3)

   # Draw vertices in color depending on ring
   # c = 0
   # rads = list(draw_rings.keys())
   # rads.sort(reverse=True)
   # for r in rads:
   #    py5.fill(colors[c])
   #    for i in draw_rings[r]:
   #       v = draw_vectors[i]
   #       py5.circle(v[0]*m, v[1]*m, 20)
   #    c += 1

   # Draw edges in color depending on outer vertex ring
   rads = list(draw_rings.keys())
   rads.sort(reverse=True)
   sorted_edges = sorted(draw_edges, key=max_radius, reverse=True)
   # angles = [2*math.pi/600 * (-1)**i for i in range(8)]
   # rotate_rings(rads, angles)
   py5.stroke_weight(0.5)
   for e in sorted_edges:
      v = draw_vectors[e[0]]
      w = draw_vectors[e[1]]
      r = round(max_radius(e), 5)

      # Draw only one ring
      if r != rads[0]:
         continue

      c = rads.index(r)
      py5.stroke(colors[c])
      py5.line(v[0]*m, v[1]*m, w[0]*m, w[1]*m)

   # if py5.frame_count == 1:
   #    py5.save_frame('./E8_roots.png')

   # if py5.frame_count <= 600:
   #    py5.save_frame('./E8_movie_###.png')

   py5.exit_sketch()

py5.run_sketch()
