"""Instantiate components to use for the stainless steel heavy reflector."""

import openmc

from .materials import mats
from .surfaces import surfs, lattice_pitch
from .assemblies import univs


#### HEAVY REFLECTOR

# All the dimensions of the water holes in the heavy reflectors were eyeballed
# from DC, Figure 4.3-25

# Pixel widths from the Figure -- we'll convert these to actual coordinates
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

d_small = 13
d_large = 30

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

r1 = scale*d_small/2
r2 = scale*d_large/2

dims = [
    (x1, y1, r1), (x2, y1, r1), (x3, y1, r1), (x4, y1, r2),
    (x4, y2, r1), (x4, y3, r1), (x4, y4, r1), (x5, y5, r1),
    (x6, y6, r1), (x7, y7, r1), (x8, y8, r1), (x9, y9, r1),
    (x1, y10, r1)
]

water_holes = []
for x, y, r in dims:
    zcyl = openmc.ZCylinder(x0=x, y0=y, R=r)
    hole = openmc.Cell(fill=mats['H2O'], region=-zcyl)
    water_holes.append(hole)

ss_region = openmc.Intersection(~c.region for c in water_holes)

ss_cell = openmc.Cell(name='heavy reflector SS', fill=mats['SS'],
                      region=ss_region)

univs['heavy reflector NW'] = openmc.Universe(name='heavy reflector NW')
univs['heavy reflector NW'].add_cells(water_holes)
univs['heavy reflector NW'].add_cell(ss_cell)


# NE corner

cell = openmc.Cell(name='heavy reflector NE', fill=univs['heavy reflector NW'])
cell.rotation = (0, 180, 0)
univs['heavy reflector NE'] = openmc.Universe(name='heavy reflector NE')
univs['heavy reflector NE'].add_cell(cell)

# SW corner

cell = openmc.Cell(name='heavy reflector SW', fill=univs['heavy reflector NW'])
cell.rotation = (180, 0, 0)
univs['heavy reflector SW'] = openmc.Universe(name='heavy reflector SW')
univs['heavy reflector SW'].add_cell(cell)

# SE corner

cell = openmc.Cell(name='heavy reflector SE', fill=univs['heavy reflector NW'])
cell.rotation = (0, 0, 180)
univs['heavy reflector SE'] = openmc.Universe(name='heavy reflector SE')
univs['heavy reflector SE'].add_cell(cell)


# Solid stainless steel universe

all_ss = openmc.Cell(name='heavy reflector', fill=mats['SS'])
univs['heavy reflector'] = openmc.Universe(
    name='heavy reflector', cells=[all_ss])
