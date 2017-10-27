"""Stainless steel heavy reflector.

None of the public NuScale documents give information about the dimensions and
location of the water holes in the heavy neutron reflector. Thus, all the
dimensions of the water holes in the heavy reflectors were eyeballed from the DC
application, Figure 4.3-25. A screenshot was used to determine the size and
location of the water holes which were then converted to actual dimensions by
scaling according to the width of an assembly.

"""

import openmc

from .materials import mats
from .surfaces import surfs, lattice_pitch
from .assemblies import univs


def make_reflector(name, parameters):
    """Make an assembly-sized heavy neutron reflector block with cooling holes.

    Parameters
    ----------
    name : str
        Name of the universe to create
    parameters : iterable of 3-tuples
        Iterable containing tuple with the (x,y) coordinates of the center and
        the radius of a Z-cylinder and the

    """
    water_holes = []
    for x, y, r in parameters:
        zcyl = openmc.ZCylinder(x0=x, y0=y, R=r)
        hole = openmc.Cell(fill=mats['H2O'], region=-zcyl)
        water_holes.append(hole)

    ss_region = openmc.Intersection(~c.region for c in water_holes)
    ss_cell = openmc.Cell(name='{} SS'.format(name), fill=mats['SS'],
                          region=ss_region)

    univs[name] = openmc.Universe(name=name)
    univs[name].add_cells(water_holes)
    univs[name].add_cell(ss_cell)


# Reflector at northwest corner (fuel assemblies to the right and below)

width = 276
p1 = 59
p2 = 126
p3 = 196
p4 = 264

p5 = 105

p6 = 122
p7 = 164

p8 = 138
p9 = 222

p10 = 247

# There are 8 large water holes and all others appear to have the same, smaller
# diameter
d_small = 13
d_large = 30

# All pixel widths are scaled according to the actual width of an assembly
# divided by the width of an assembly in pixels
scale = lattice_pitch/width

# Physical positions
x1 = -lattice_pitch/2 + scale*(width - p4)
x2 = -lattice_pitch/2 + scale*(width - p3)
x3 = -lattice_pitch/2 + scale*(width - p2)
x4 = -lattice_pitch/2 + scale*(width - p1)
y1 = -lattice_pitch/2 + scale*p1
y2 = -lattice_pitch/2 + scale*p2
y3 = -lattice_pitch/2 + scale*p3
y4 = -lattice_pitch/2 + scale*p4

x5 = -lattice_pitch/2 + scale*(width - p5)
y5 = -lattice_pitch/2 + scale*p5
x6 = -lattice_pitch/2 + scale*(width - p7)
y6 = -lattice_pitch/2 + scale*p6
x7 = -lattice_pitch/2 + scale*(width - p6)
y7 = -lattice_pitch/2 + scale*p7
x8 = -lattice_pitch/2 + scale*(width - p9)
y8 = -lattice_pitch/2 + scale*p8
x9 = -lattice_pitch/2 + scale*(width - p8)
y9 = -lattice_pitch/2 + scale*p9

y10 = -lattice_pitch/2 + scale*p10

# Radius of small/large water holes
r1 = scale*d_small/2
r2 = scale*d_large/2

params = [
    (x1, y1, r1), (x2, y1, r1), (x3, y1, r1), (x4, y1, r2),
    (x4, y2, r1), (x4, y3, r1), (x4, y4, r1), (x5, y5, r1),
    (x6, y6, r1), (x7, y7, r1), (x8, y8, r1), (x9, y9, r1),
    (x1, y10, r1)
]

make_reflector('heavy reflector NW', params)

# Reflector at (1, 1)

params = [
    (x4, y1, r1),
    (lattice_pitch/2 - scale*103, -lattice_pitch/2 + scale*156, r1),
    (lattice_pitch/2 - scale*158, -lattice_pitch/2 + scale*103, r1)
]
make_reflector('heavy reflector 1,1', params)

# Left reflector (4,0)

left1 = 58
left2 = 118
left3 = 173
up3 = 76

x1 = -lattice_pitch/2 + scale*(width - left1)
x2 = -lattice_pitch/2 + scale*(width - left2)
d_y = scale*67
x3 = -lattice_pitch/2 + scale*(width - left3)
y3 = scale*up3

params = [
    (x1, 0, r1), (x1, d_y, r1), (x1, 2*d_y, r1), (x1, -d_y, r1), (x1, -2*d_y, r1),
    (x2, d_y/2, r1), (x2, 3/2*d_y, r1), (x2, -d_y/2, r1), (x2, -3/2*d_y, r1),
    (x3, y3, r1), (x3, -y3, r1)
]

make_reflector('heavy reflector 4,0', params)

# Reflector at (3,0)

params = []
for i in range(2, 7):
    params.append((x1, i*d_y - lattice_pitch, r1))
for i in (5, 7, 11):
    params.append((x2, i*d_y/2 - lattice_pitch, r1))

left3 = 140
left4 = 183
up3 = 159
up4 = 47

x3 = -lattice_pitch/2 + scale*(width - left3)
y3 = -lattice_pitch/2 + scale*up3
x4 = -lattice_pitch/2 + scale*(width - left4)
y4 = -lattice_pitch/2 + scale*up4
params += [(x3, y3, r1), (x4, y4, r1)]

make_reflector('heavy reflector 3,0', params)

# Reflector at (5,0)

params = [(x, -y, r) for x, y, r in params]
make_reflector('heavy reflector 5,0', params)

# Reflector at (2, 0)

params = [(-lattice_pitch/2 + scale*(width - 78),
           -lattice_pitch/2 + scale*98, r1)]
make_reflector('heavy reflector 2,0', params)

################################################################################
# Beyond this point, all universes are just copies of the ones previously
# created with a rotation applied

# NE corner
cell = openmc.Cell(name='heavy reflector NE', fill=univs['heavy reflector NW'])
cell.rotation = (0, 0, -90)
univs['heavy reflector NE'] = openmc.Universe(name='heavy reflector NE')
univs['heavy reflector NE'].add_cell(cell)

# SW corner
cell = openmc.Cell(name='heavy reflector SW', fill=univs['heavy reflector NW'])
cell.rotation = (0, 0, 90)
univs['heavy reflector SW'] = openmc.Universe(name='heavy reflector SW')
univs['heavy reflector SW'].add_cell(cell)

# SE corner
cell = openmc.Cell(name='heavy reflector SE', fill=univs['heavy reflector NW'])
cell.rotation = (0, 0, 180)
univs['heavy reflector SE'] = openmc.Universe(name='heavy reflector SE')
univs['heavy reflector SE'].add_cell(cell)

# Reflector at (0, 2)
name = 'heavy reflector 0,2'
cell = openmc.Cell(name=name, fill=univs['heavy reflector 2,0'])
cell.rotation = (0, 180, -90)
univs[name] = openmc.Universe(name=name, cells=[cell])

# Reflector at (0, 3)
name = 'heavy reflector 0,3'
cell = openmc.Cell(name=name, fill=univs['heavy reflector 5,0'])
cell.rotation = (0, 0, -90)
univs[name] = openmc.Universe(name=name, cells=[cell])

# Reflector at (0, 4)
name = 'heavy reflector 0,4'
cell = openmc.Cell(name=name, fill=univs['heavy reflector 4,0'])
cell.rotation = (0, 0, -90)
univs[name] = openmc.Universe(name=name, cells=[cell])

# Reflector at (0, 5)
name = 'heavy reflector 0,5'
cell = openmc.Cell(name=name, fill=univs['heavy reflector 3,0'])
cell.rotation = (0, 0, -90)
univs[name] = openmc.Universe(name=name, cells=[cell])

# Reflector at (0, 6)
name = 'heavy reflector 0,6'
cell = openmc.Cell(name=name, fill=univs['heavy reflector 2,0'])
cell.rotation = (0, 0, -90)
univs[name] = openmc.Universe(name=name, cells=[cell])

# Reflector at (1, 7)
name = 'heavy reflector 1,7'
cell = openmc.Cell(name=name, fill=univs['heavy reflector 1,1'])
cell.rotation = (0, 0, -90)
univs[name] = openmc.Universe(name=name, cells=[cell])

# Reflector at (2, 8)
name = 'heavy reflector 2,8'
cell = openmc.Cell(name=name, fill=univs['heavy reflector 2,0'])
cell.rotation = (0, 180, 0)
univs[name] = openmc.Universe(name=name, cells=[cell])

# Reflector at (3, 8)
name = 'heavy reflector 3,8'
cell = openmc.Cell(name=name, fill=univs['heavy reflector 3,0'])
cell.rotation = (0, 180, 0)
univs[name] = openmc.Universe(name=name, cells=[cell])

# Reflector at (4, 8)
name = 'heavy reflector 4,8'
cell = openmc.Cell(name=name, fill=univs['heavy reflector 4,0'])
cell.rotation = (0, 180, 0)
univs[name] = openmc.Universe(name=name, cells=[cell])

# Reflector at (5, 8)
name = 'heavy reflector 5,8'
cell = openmc.Cell(name=name, fill=univs['heavy reflector 3,0'])
cell.rotation = (0, 0, 180)
univs[name] = openmc.Universe(name=name, cells=[cell])

# Reflector at (6, 0)
name = 'heavy reflector 6,0'
cell = openmc.Cell(name=name, fill=univs['heavy reflector 2,0'])
cell.rotation = (180, 0, 0)
univs[name] = openmc.Universe(name=name, cells=[cell])

# Reflector at (6, 8)
name = 'heavy reflector 6,8'
cell = openmc.Cell(name=name, fill=univs['heavy reflector 2,0'])
cell.rotation = (0, 0, 180)
univs[name] = openmc.Universe(name=name, cells=[cell])

# Reflector at (7, 1)
name = 'heavy reflector 7,1'
cell = openmc.Cell(name=name, fill=univs['heavy reflector 1,1'])
cell.rotation = (180, 0, 0)
univs[name] = openmc.Universe(name=name, cells=[cell])

# Reflector at (7, 7)
name = 'heavy reflector 7,7'
cell = openmc.Cell(name=name, fill=univs['heavy reflector 1,1'])
cell.rotation = (0, 0, 180)
univs[name] = openmc.Universe(name=name, cells=[cell])

# Reflector at (8, 2)
name = 'heavy reflector 8,2'
cell = openmc.Cell(name=name, fill=univs['heavy reflector 2,0'])
cell.rotation = (0, 0, 90)
univs[name] = openmc.Universe(name=name, cells=[cell])

# Reflector at (8, 3)
name = 'heavy reflector 8,3'
cell = openmc.Cell(name=name, fill=univs['heavy reflector 3,0'])
cell.rotation = (0, 0, 90)
univs[name] = openmc.Universe(name=name, cells=[cell])

# Reflector at (8, 4)
name = 'heavy reflector 8,4'
cell = openmc.Cell(name=name, fill=univs['heavy reflector 4,0'])
cell.rotation = (0, 0, 90)
univs[name] = openmc.Universe(name=name, cells=[cell])

# Reflector at (8, 5)
name = 'heavy reflector 8,5'
cell = openmc.Cell(name=name, fill=univs['heavy reflector 5,0'])
cell.rotation = (0, 0, 90)
univs[name] = openmc.Universe(name=name, cells=[cell])

# Reflector at (8, 6)
name = 'heavy reflector 8,6'
cell = openmc.Cell(name=name, fill=univs['heavy reflector 2,0'])
cell.rotation = (0, 0, 180)
univs[name] = openmc.Universe(name=name, cells=[cell])

# Solid stainless steel universe

all_ss = openmc.Cell(name='heavy reflector', fill=mats['SS'])
univs['heavy reflector'] = openmc.Universe(
    name='heavy reflector', cells=[all_ss])
