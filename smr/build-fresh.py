#!/usr/bin/env python3

import os
import shutil
import copy
import argparse

import numpy as np

import openmc
from smr.materials import materials
from smr.plots import plots
from smr.surfaces import lattice_pitch, bottom_fuel_stack, top_active_core
from smr.core import core_geometry


# Define command-line options
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--multipole', action='store_true',
                    help='Whether to use multipole cross sections')
parser.add_argument('-t', '--tallies', choices=('cell', 'mat'), default='cell',
                    help='Whether to use distribmats or distribcells for tallies')
args = parser.parse_args()


geometry = core_geometry()

#### "Differentiate" the geometry if using distribmats
if args.tallies == 'mat':
    # Count the number of instances for each cell and material
    geometry.determine_paths(instances_only=True)

    # Extract all cells filled by a fuel material
    fuel_mats = {m for m in materials if 'UO2 Fuel' in m.name}

    for cell in geometry.get_all_cells().values():
        if cell.fill in fuel_mats:
            # Fill cell with list of "differentiated" materials
            cell.fill = [cell.fill.clone() for i in range(cell.num_instances)]

#### Create OpenMC "materials.xml" file
all_materials = geometry.get_all_materials()
materials = openmc.Materials(all_materials.values())
materials.export_to_xml()


#### Create OpenMC "geometry.xml" file
geometry.export_to_xml()


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
settings.output = {'tallies': False}
settings.source = source
settings.sourcepoint_write = False

if args.multipole:
    settings.temperature = {'multipole': True, 'tolerance': 1000}

settings.export_to_xml()


#### Create OpenMC "plots.xml" file
plots.export_to_xml()


####  Create OpenMC "tallies.xml" file
tallies = openmc.Tallies()

# Extract all fuel materials
materials = geometry.get_materials_by_name(name='Fuel', matching=False)

# If using distribcells, create distribcell tally needed for depletion
if args.tallies == 'cell':
    # Extract all cells filled by a fuel material
    fuel_cells = []
    for cell in geometry.get_all_cells().values():
        if cell.fill in materials:
            tally = openmc.Tally(name='depletion tally')
            tally.scores = ['(n,p)', '(n,a)', '(n,gamma)',
                            'fission', '(n,2n)', '(n,3n)', '(n,4n)']
            tally.nuclides = cell.fill.get_nuclides()
            tally.filters.append(openmc.DistribcellFilter([cell]))
            tallies.append(tally)

# If using distribmats, create material tally needed for depletion
elif args.tallies == 'mat':
    tally = openmc.Tally(name='depletion tally')
    tally.scores = ['(n,p)', '(n,a)', '(n,gamma)',
                    'fission', '(n,2n)', '(n,3n)', '(n,4n)']
    tally.nuclides = materials[0].get_nuclides()
    tally.filters = [openmc.MaterialFilter(materials)]
    tallies.append(tally)

tallies.export_to_xml()


#### Move all XML files to 'fresh' directory

if not os.path.exists('fresh'):
    os.makedirs('fresh')

shutil.move('materials.xml', 'fresh/materials.xml')
shutil.move('geometry.xml', 'fresh/geometry.xml')
shutil.move('settings.xml', 'fresh/settings.xml')
shutil.move('tallies.xml', 'fresh/tallies.xml')
shutil.move('plots.xml', 'fresh/plots.xml')
