#!/usr/bin/env python3

import os
import shutil
import copy

import numpy as np

import openmc
from smr.materials import materials
from smr.plots import plots
from smr.surfaces import lattice_pitch, bottom_fuel_stack, top_active_core
from smr.core import geometry


#### Query the user for options

# Query the user on whether to use multipole cross sections
multipole = input('Use multipole cross sections? (y/n): ').lower()
multipole = (multipole == 'y')

# Query the user on whether to use distribmats or distribcells
# If using distribmats, the geometry must be "differentiated" with unique
# material instances for each instance of a fuel cell
distrib = input('Use distribmat or distribcells? [mat/cell]: ').lower()

if distrib not in ['cell', 'mat']:
    raise InputError('Distrib type "{}" is unsupported'.format(distrib))


#### "Differentiate" the geometry if using distribmats
if distrib == 'mat':

    # Count the number of instances for each cell and material
    geometry.determine_paths()

    # Extract all cells filled by a fuel material
    fuel_cells = geometry.get_cells_by_name(
        name='(1.6%) (0)', case_sensitive=True)
    fuel_cells.extend(geometry.get_cells_by_name(
        name='(1.6%) grid (bottom) (0)', case_sensitive=True))
    fuel_cells.extend(geometry.get_cells_by_name(
        name='(1.6%) grid (intermediate) (0)', case_sensitive=True))
    fuel_cells.extend(geometry.get_cells_by_name(
        name='(2.4%) (0)', case_sensitive=True))
    fuel_cells.extend(geometry.get_cells_by_name(
        name='(2.4%) grid (bottom) (0)', case_sensitive=True))
    fuel_cells.extend(geometry.get_cells_by_name(
        name='(2.4%) grid (intermediate) (0)', case_sensitive=True))
    fuel_cells.extend(geometry.get_cells_by_name(
        name='(3.1%) (0)', case_sensitive=True))
    fuel_cells.extend(geometry.get_cells_by_name(
        name='(3.1%) grid (bottom) (0)', case_sensitive=True))
    fuel_cells.extend(geometry.get_cells_by_name(
        name='(3.1%) grid (intermediate) (0)', case_sensitive=True))

    # Assign distribmats for each material
    for cell in fuel_cells:
        new_materials = []

        for i in range(cell.num_instances):
            new_materials.append(cell.fill.clone())

        # Fill cell with list of "differentiated" materials
        cell.fill = new_materials


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

if multipole:
    settings.temperature = {'multipole': True, 'tolerance': 1000}

settings.export_to_xml()


#### Create OpenMC "plots.xml" file
plots.export_to_xml()


####  Create OpenMC "tallies.xml" file
tallies = openmc.Tallies()

# Extract all fuel materials
materials = geometry.get_materials_by_name(name='Fuel', matching=False)

# If using distribcells, create distribcell tally needed for depletion
if distrib == 'cell':

    # Extract all cells filled by a fuel material
    fuel_cells = geometry.get_cells_by_name(
        name='(1.6%) (0)', case_sensitive=True)
    fuel_cells.extend(geometry.get_cells_by_name(
        name='(1.6%) grid (bottom) (0)', case_sensitive=True))
    fuel_cells.extend(geometry.get_cells_by_name(
        name='(1.6%) grid (intermediate) (0)', case_sensitive=True))
    fuel_cells.extend(geometry.get_cells_by_name(
        name='(2.4%) (0)', case_sensitive=True))
    fuel_cells.extend(geometry.get_cells_by_name(
        name='(2.4%) grid (bottom) (0)', case_sensitive=True))
    fuel_cells.extend(geometry.get_cells_by_name(
        name='(2.4%) grid (intermediate) (0)', case_sensitive=True))
    fuel_cells.extend(geometry.get_cells_by_name(
        name='(3.1%) (0)', case_sensitive=True))
    fuel_cells.extend(geometry.get_cells_by_name(
        name='(3.1%) grid (bottom) (0)', case_sensitive=True))
    fuel_cells.extend(geometry.get_cells_by_name(
        name='(3.1%) grid (intermediate) (0)', case_sensitive=True))

    for cell in fuel_cells:
        tally = openmc.Tally(name='depletion tally')
        tally.scores = ['(n,p)', '(n,a)', '(n,gamma)',
                        'fission', '(n,2n)', '(n,3n)', '(n,4n)']
        tally.nuclides = cell.fill.get_nuclides()
        tally.filters.append(openmc.DistribcellFilter([cell.id]))
        tallies.append(tally)

# If using distribmats, create material tally needed for depletion
elif distrib == 'mat':
    tally = openmc.Tally(name='depletion tally')
    tally.scores = ['(n,p)', '(n,a)', '(n,gamma)',
                    'fission', '(n,2n)', '(n,3n)', '(n,4n)']
    tally.nuclides = materials[0].get_nuclides()
    material_ids = [material.id for material in materials]
    tally.filters.append(openmc.MaterialFilter(material_ids))
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
