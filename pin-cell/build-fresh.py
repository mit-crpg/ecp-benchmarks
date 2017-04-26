#!/usr/bin/env python3

"""Creates a 2D fuel pin with reflective BCs."""

import os
import shutil

import numpy as np
import openmc

from geometry import beavrs, openmc_geometry


#### Query the user for options

# Query the user on whether to use multipole cross sections
multipole = input('Use multipole cross sections? (y/n): ').lower()
multipole = (multipole == 'y')


#### Create OpenMC "materials.xml" file
beavrs.write_openmc_materials()


#### Create OpenMC "geometry.xml" file
openmc_geometry.export_to_xml()


#### Create OpenMC "settings.xml" file

# Construct uniform initial source distribution over fissionable zones
lower_left = [-0.62992, -0.62992, -10.0]
upper_right = [+0.62992, +0.62992, +10.0]
source = openmc.source.Source(space=openmc.stats.Box(lower_left, upper_right))
source.space.only_fissionable = True

settings_file = openmc.Settings()
settings_file.batches = 10
settings_file.inactive = 5
settings_file.particles = 10000
settings_file.output = {'tallies': False}
settings_file.source = source
settings_file.sourcepoint_write = False

if multipole:
    settings_file.temperature = {'multipole': True, 'tolerance': 1000}

settings_file.export_to_xml()


#### Create OpenMC "plots.xml" file

# Initialize the BEAVRS color mapping scheme
beavrs.write_openmc_plots()

# Create a plot colored by materials
plot = openmc.Plot()
plot.width = [1.25984, 1.25984]
plot.origin = [0., 0., np.inf]
plot.color_by = 'material'
plot.filename = 'fuel-pin'
plot.colors = beavrs.plots.colors_mat
plot.pixels = [1000, 1000]

plot_file = openmc.Plots([plot])
plot_file.export_to_xml()


#### Create a tally akin to that used by OpenDeplete for depletion

# Extract all fuel materials
materials = openmc_geometry.get_materials_by_name(name='Fuel', matching=False)

# If using distribmats, create material tally needed for depletion
tally = openmc.Tally(name='depletion tally')
tally.scores = ['(n,p)', '(n,a)', '(n,gamma)',
                'fission', '(n,2n)', '(n,3n)', '(n,4n)']
tally.nuclides = materials[0].get_nuclides()
material_ids = [material.id for material in materials]
tally.filters.append(openmc.MaterialFilter(material_ids))


####  Create OpenMC "tallies.xml" file
tallies = openmc.Tallies()
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
