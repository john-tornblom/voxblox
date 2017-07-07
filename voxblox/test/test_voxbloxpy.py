#!/usr/bin/env python

import timeit

import sys;
sys.path.append('/home/mereweth/snappy/torq_gcs_catkin_ws/devel/.private/voxblox/lib/')

import voxblox
dir(voxblox.EsdfMap)

try:
    layer = voxblox.loadEsdfLayer('THIS_DOES_NOT_EXIST')
except RuntimeError as e:
    print(e)

layer = voxblox.loadEsdfLayer('/Users/mereweth/Desktop/cow_and_lady/cow_and_lady.esdf.proto')
assert(layer is not None)
map = voxblox.EsdfMap(layer)
#map = voxblox.EsdfMap('/Users/mereweth/Desktop/drl_munich_depth_motion_stereo/drl_munich_depth_motion_stereo.esdf.proto')
#map = voxblox.EsdfMap('/Users/mereweth/Desktop/terra_bella/terra_bella_10cm_16per_full_euclidean.esdf.proto')

print map.voxel_size
print map.block_size

import numpy as np

x_ = np.linspace(0.0, 0.2, 100)
y_ = np.linspace(0.0, 0.2, 100)
z_ = np.linspace(0.0, 0.2, 100)
x, y, z = np.meshgrid(x_, y_, z_)
query = np.matrix(np.c_[x.flatten(), y.flatten(), z.flatten()]).T

#query = np.matrix([[0,0,0.1],
#                   [0.1,0,0],
#                   [0.1,0.1,0],
#                   [0,0.1,0]], dtype='double').T

grad = np.matrix(np.zeros(np.shape(query), dtype='double'))

dist = np.matrix(np.zeros((np.shape(query)[1], 1), dtype='double'))

obs = np.matrix(np.zeros((np.shape(query)[1], 1), dtype='int32'))

map.isObserved(query, obs)
map.getDistanceAtPosition(query, dist, obs)

import pdb; pdb.set_trace()

def interp_fun():
    map.getDistanceAndGradientAtPosition(query, dist, grad, obs)
interp_duration = timeit.timeit(interp_fun, number=10) / 10.0
print(interp_duration)

num_pts = 1000 * 1000
slice_pos = np.matrix(np.zeros((3, num_pts)))
slice_dist = np.matrix(np.zeros((np.shape(slice_pos)[1], 1), dtype='double'))

def no_interp_fun():
    map.coordPlaneSliceGetDistance(2, # xy plane
                                   0.5, # z
                                   slice_pos,
                                   slice_dist,
                                   num_pts)
no_interp_duration = timeit.timeit(no_interp_fun, number=10) / 10.0
print(no_interp_duration)

try:
  import IPython; IPython.embed()

except:
  import code
  code.interact(local=dict(globals(), **locals()))
