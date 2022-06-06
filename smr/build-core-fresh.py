#!/usr/bin/env python3

import copy
import argparse
from math import pi
from pathlib import Path

import numpy as np
import openmc
from tqdm import tqdm

from smr.materials import materials
from smr.surfaces import lattice_pitch, bottom_fuel_stack, top_active_core, \
    pellet_OR, active_fuel_length
from smr.core import core_geometry
from smr import inlet_temperature


def clone(material):
    """Perform copy of material but share nuclide densities"""
    shared_mat = copy.copy(material)
    shared_mat.id = None
    return shared_mat


# Define command-line options
parser = argparse.ArgumentParser()
parser.add_argument('--multipole', action='store_true',
                    help='Use multipole cross sections')
parser.add_argument('--no-multipole', dest='multipole', action='store_false',
                    help='Do not use multipole cross sections')
parser.add_argument('--clone', action='store_true',
                    help='Clone materials for each cell instance')
parser.add_argument('--no-clone', dest='clone', action='store_false',
                    help='Do not clone materials for each cell instance')
parser.add_argument('-r', '--rings', type=int, default=10,
                    help='Number of annular regions in fuel')
parser.add_argument('-a', '--axial', type=int, default=196,
                    help='Number of axial subdivisions in fuel')
parser.add_argument('-d', '--depleted', action='store_true',
                    help='Whether UO2 compositions should represent depleted fuel')
parser.add_argument('-o', '--output-dir', type=Path, default=None)
parser.set_defaults(clone=False, multipole=True)
args = parser.parse_args()

# Make directory for inputs
if args.output_dir is None:
    if args.depleted:
        directory = Path('core-depleted')
    else:
        directory = Path('core-fresh')
else:
    directory = args.output_dir
directory.mkdir(exist_ok=True)

if args.rings > 1:
    ring_radii = np.sqrt(np.arange(1, args.rings)*pellet_OR**2 / args.rings)
else:
    ring_radii = None
geometry = core_geometry(ring_radii, args.axial, args.depleted)

h = active_fuel_length / args.axial
fuel_mats = {}

# Count the number of instances for each cell and material
if args.clone:
    geometry.determine_paths(instances_only=True)

fuel_volume = pi * pellet_OR**2 * h / args.rings
for cell in tqdm(geometry.get_all_cells().values(),
                 desc='Differentiating materials / assigning volume'):
    if cell.fill in materials:
        # Determine if this material is fuel
        name = cell.fill.name
        is_fuel = 'UO2 Fuel' in name

        # Determine volume of each fuel material
        if is_fuel:
            if args.clone:
                # Fill cell with list of "differentiated" materials if requested
                cell.fill = [clone(cell.fill) for i in range(cell.num_instances)]
                for mat in cell.fill:
                    mat.volume = fuel_volume
            else:
                r_o = cell.region.bounding_box[1][0]
                if (name, r_o) not in fuel_mats:
                    cell.fill = cell.fill.clone()
                    cell.fill.volume = fuel_volume
                    fuel_mats[name, r_o] = cell.fill
                else:
                    cell.fill = fuel_mats[name, r_o]
        else:
            cell.fill.volume = 1.0

#### Create OpenMC "materials.xml" file
all_materials = geometry.get_all_materials()
materials = openmc.Materials(all_materials.values())
materials.export_to_xml(str(directory / 'materials.xml'))


#### Create OpenMC "geometry.xml" file
geometry.export_to_xml(str(directory / 'geometry.xml'))


#### Create OpenMC "settings.xml" file

# Construct uniform initial source distribution over fissionable zones
lower_left = [-7.*lattice_pitch/2., -7.*lattice_pitch/2., bottom_fuel_stack]
upper_right = [+7.*lattice_pitch/2., +7.*lattice_pitch/2., top_active_core]
source = openmc.source.Source(space=openmc.stats.Box(lower_left, upper_right))
source.space.only_fissionable = True

settings = openmc.Settings()
settings.batches = 200
settings.inactive = 100
settings.particles = 10000
settings.output = {'tallies': False, 'summary': False}
settings.source = source
settings.sourcepoint_write = False

settings.temperature = {
    'default': inlet_temperature,
    'method': 'interpolation',
    'range': (300.0, 1500.0),
}
if args.multipole:
    settings.temperature['multipole'] = True
    settings.temperature['tolerance'] = 1000

settings.export_to_xml(str(directory / 'settings.xml'))

