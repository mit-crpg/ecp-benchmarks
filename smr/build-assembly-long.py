#!/usr/bin/env python3

import argparse
import copy
from math import pi, isclose
from pathlib import Path

import numpy as np
from tqdm import tqdm
import openmc

from smr.materials import materials, mats
from smr.surfaces import surfs, lattice_pitch, pin_pitch, bottom_fuel_stack, \
    top_active_core, pellet_OR, clad_OR, clad_IR, guide_tube_IR, guide_tube_OR, \
    active_fuel_length
from smr.pins import pin_universes, make_stack


# Define command-line options
parser = argparse.ArgumentParser()
parser.add_argument('--multipole', action='store_true',
                    help='Use multipole cross sections')
parser.add_argument('--no-multipole', action='store_false',
                    help='Do not use multipole cross sections')
parser.add_argument('-a', '--axial', type=int, default=100,
                    help='Number of axial subdivisions in fuel')
parser.add_argument('-d', '--depleted', action='store_true',
                    help='Whether UO2 compositions should represent depleted fuel')
parser.add_argument('-o', '--output-dir', type=Path, default=None)
parser.set_defaults(multipole=True)
args = parser.parse_args()

# Make directory for inputs
if args.output_dir is None:
    if args.depleted:
        directory = Path('assembly-long-depleted')
    else:
        directory = Path('assembly-long-fresh')
else:
    directory = args.output_dir
directory.mkdir(exist_ok=True)

rings = [0.1*pin_pitch, 0.2*pin_pitch]

assembly_long_surfs = [
    surfs['bottom FR'],
    surfs['bot active core'],
    surfs['top active core'],
    surfs['top pin plenum'],
    surfs['top FR'],
    surfs['bot upper nozzle'],
    surfs['top upper nozzle']
]

univs = pin_universes(rings, args.axial, args.depleted)
fuel_univ = make_stack(
    'Fuel (3.1%) stack no grid',
    surfaces=assembly_long_surfs,
    universes=[
        univs['water pin'],
        univs['end plug'],
        univs['Fuel pin (3.1%) no grid'],
        univs['pin plenum'],
        univs['end plug'],
        univs['water pin']
    ]
)

# Define the NumPy array indices for assembly locations where there
# may be CR guide tubes, instrument tubes and burnable absorbers
nonfuel_y = np.array([2,2,2,3,3,5,5,5,5,5,8,8,8,8,8,11,11,11,11,11,13,13,14,14,14])
nonfuel_x = np.array([5,8,11,3,13,2,5,8,11,14,2,5,8,11,14,2,5,8,11,14,3,13,5,8,11])

universes = np.full((17,17), fuel_univ)
universes[nonfuel_y, nonfuel_x] = univs['GT empty']

# Instantiate the lattice
lattice = openmc.RectLattice(name='Pin lattice')
lattice.lower_left = (-17.*pin_pitch/2., -17.*pin_pitch/2.)
lattice.pitch = (pin_pitch, pin_pitch)
lattice.universes = universes

# Add lattice to bounding cell
root_universe = openmc.Universe(name='Root universe')
cell = openmc.Cell(name='Lattice cell')
cell.fill = lattice
z_bounds = +surfs['bottom FR'] & -surfs['top FR']
cell.region = surfs['lat grid box inner'] & z_bounds
root_universe.add_cell(cell)

# Apply reflective boundaries on sides and vacuum on bottom/top
surfs['bottom FR'].boundary_type = 'vacuum'
surfs['top FR'].boundary_type = 'vacuum'
for halfspace in surfs['lat grid box inner']:
    halfspace.surface.boundary_type = 'reflective'

# Define geometry with a single assembly
geometry = openmc.Geometry(root_universe)

h = active_fuel_length / args.axial

fuel_mats = {}

for cell in tqdm(geometry.get_all_material_cells().values(),
                 desc='Assigning volume'):
    if cell.fill in materials:
        # Determine volume of each fuel material
        if 'UO2 Fuel' in cell.fill.name:
            upper_right = cell.region.bounding_box[1]
            if isclose(upper_right[0], rings[0]):
                ri, ro = 0.0, rings[0]
            elif isclose(upper_right[0], rings[1]):
                ri, ro = rings[0], rings[1]
            else:
                ri, ro = rings[1], pellet_OR
            if ri not in fuel_mats:
                cell.fill = cell.fill.clone()
                cell.fill.volume = pi * (ro*ro - ri*ri) * h
                fuel_mats[ri] = cell.fill
            else:
                cell.fill = fuel_mats[ri]
        else:
            cell.fill.volume = 1.0

#### Create OpenMC "materials.xml" file
print('Getting materials...')
all_materials = geometry.get_all_materials()
print('Creating materials collection...')
materials = openmc.Materials(all_materials.values())
print('Exporting materials to XML...')
materials.export_to_xml(str(directory / 'materials.xml'))


#### Create OpenMC "geometry.xml" file
geometry.export_to_xml(str(directory / 'geometry.xml'))


#### Create OpenMC "settings.xml" file

# Construct uniform initial source distribution over fissionable zones
lower_left = (-lattice_pitch/2, -lattice_pitch/2, bottom_fuel_stack)
upper_right = (lattice_pitch/2, lattice_pitch/2, top_active_core)
source = openmc.source.Source(space=openmc.stats.Box(lower_left, upper_right))
source.space.only_fissionable = True

settings = openmc.Settings()
settings.batches = 200
settings.inactive = 100
settings.particles = 10000
settings.output = {'tallies': False, 'summary': False}
settings.source = source
settings.sourcepoint = {'write': False}

if args.multipole:
    settings.temperature = {
        'multipole': True,
        'tolerance': 1000,
        'default': 531.5,
        'method': 'interpolation',
        'range': (500.0, 1300.0)
    }

settings.export_to_xml(str(directory / 'settings.xml'))
