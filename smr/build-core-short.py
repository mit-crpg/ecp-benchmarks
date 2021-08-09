#!/usr/bin/env python3

import os
import shutil
import copy
import argparse
from math import pi, isclose
from pathlib import Path

import numpy as np

import openmc
from smr.materials import materials
from smr.plots import core_plots
from smr.surfaces import lattice_pitch, bottom_fuel_stack, top_active_core, \
    pellet_OR, surfs, pin_pitch, clad_IR, clad_OR
import smr.surfaces
import smr.pins
from smr.core import core_geometry
from smr import inlet_temperature


# Define command-line options
parser = argparse.ArgumentParser()
parser.add_argument('--multipole', action='store_true',
                    help='Use multipole cross sections')
parser.add_argument('--no-multipole', action='store_false',
                    help='Do not use multipole cross sections')
parser.add_argument('-a', '--axial', type=int, default=3,
                    help='Number of axial subdivisions in fuel')
parser.add_argument('-d', '--depleted', action='store_true',
                    help='Whether UO2 compositions should represent depleted fuel')
parser.add_argument('-o', '--output-dir', type=Path, default=None)
parser.set_defaults(multipole=True)
args = parser.parse_args()

# Make directory for inputs
if args.output_dir is None:
    if args.depleted:
        directory = Path('core-short-depleted')
    else:
        directory = Path('core-short-fresh')
else:
    directory = args.output_dir
directory.mkdir(exist_ok=True)

# Modify fuel length
length = 3. * pin_pitch
smr.surfaces.active_fuel_length = length
smr.pins.top_active_core = length
surfs['top active core'].z0 = length

# Change top and bottom of model to contain only fuel
surfs['lower bound'].z0 = 0.0
surfs['lower bound'].boundary_type = 'reflective'
surfs['upper bound'].z0 = length
surfs['upper bound'].boundary_type = 'reflective'

ring_radii = [0.1*pin_pitch, 0.2*pin_pitch]

geometry = core_geometry(ring_radii, args.axial, args.depleted)

h = length / args.axial
fuel_mats = {}

for cell in geometry.get_all_cells().values():
    if cell.fill in materials:
        # Determine volume of each fuel material
        name = cell.fill.name
        if 'UO2 Fuel' in name:
            upper_right = cell.region.bounding_box[1][0]
            if isclose(upper_right, ring_radii[0]):
                ri, ro = 0.0, ring_radii[0]
            elif isclose(upper_right, ring_radii[1]):
                ri, ro = ring_radii[0], ring_radii[1]
            else:
                ri, ro = ring_radii[1], pellet_OR
            if (name, ri) not in fuel_mats:
                cell.fill = cell.fill.clone()
                cell.fill.volume = pi * (ro*ro - ri*ri) * h
                fuel_mats[name, ri] = cell.fill
            else:
                cell.fill = fuel_mats[name, ri]
        elif name == 'Helium':
            cell.fill.volume = pi * (clad_IR**2 - pellet_OR**2) * h
        elif name == 'M5':
            # Clad is not subdivided
            cell.fill.volume = pi * (clad_OR**2 - clad_IR**2) * length
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

# Check assembly power distribution
core_lattice = geometry.get_cells_by_fill_name('Main core')[0].fill
mesh = openmc.RegularMesh.from_rect_lattice(core_lattice)
assembly_power = openmc.Tally()
assembly_power.filters = [openmc.MeshFilter(mesh)]
assembly_power.scores = ['nu-fission']
tallies = openmc.Tallies([assembly_power])
tallies.export_to_xml(directory / 'tallies.xml')
