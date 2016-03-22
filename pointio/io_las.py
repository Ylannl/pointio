# This file is part of pointio.

# pointio is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pointio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pointio.  If not, see <http://www.gnu.org/licenses/>.

# Copyright 2015 Ravi Peters

import numpy as np
try:
	import laspy
except ImportError:
	print "Cannot read las files without laspy module"
	raise

def read_las(infile, move_to_origin=True):
	inFile = laspy.file.File(infile)

	datadict = {}
	datadict['offset'] = np.zeros(3, dtype=np.double)
	if move_to_origin:
		max_ = inFile.header.max
		min_ = inFile.header.min
		datadict['offset'][0] = min_[0] + (max_[0]-min_[0])/2
		datadict['offset'][1] = min_[1] + (max_[1]-min_[1])/2
		datadict['offset'][2] = min_[2] + (max_[2]-min_[2])/2
	datadict['coords'] = np.column_stack([ np.array(a, dtype=np.float32) for a in [inFile.x-datadict['offset'][0], inFile.y-datadict['offset'][1], inFile.z-datadict['offset'][2]] ])
	
	return datadict

def write_las(outfile, datadict, mask=None):
	scale = 100.0
	if mask is None:
		coords = (datadict['coords']*scale).astype(np.int) + (datadict['offset']*scale).astype(np.int)
	else:
		coords = (datadict['coords'][mask]*scale).astype(np.int) + (datadict['offset']*scale).astype(np.int)
	header = laspy.header.Header()
	header.x_scale=1/scale
	header.y_scale=1/scale
	header.z_scale=1/scale
	outfile = laspy.file.File(outfile, mode="w", header=header)
	outfile.X = coords[:,0]
	outfile.Y = coords[:,1]
	outfile.Z = coords[:,2]
	outfile.close()
	