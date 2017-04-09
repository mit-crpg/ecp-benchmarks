"""Creates a 2D 2x2 assembly colorset with a water reflector."""

import os
import shutil
import copy

import numpy as np
import openmc

from geometry import beavrs, openmc_geometry


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
    openmc_geometry.determine_paths()

    # Determine the maximum material ID
    max_material_id = 0
    for material in openmc_geometry.get_all_materials().values():
        max_material_id = max(max_material_id, material.id)

    # Extract all cells filled by a fuel material
    fuel_cells = openmc_geometry.get_cells_by_name(
        name='enr radial 0: Fuel', case_sensitive=True)

    # Assign distribmats for each material
    for cell in fuel_cells:
        new_materials = []

        for i in range(cell.num_instances):
            new_material = copy.deepcopy(cell.fill)
            new_material.id = max_material_id + 1
            max_material_id += 1
            new_materials.append(new_material)

        # Fill cell with list of "differentiated" materials
        cell.fill = new_materials


#### Create OpenMC "materials.xml" file
all_materials = openmc_geometry.get_all_materials()
materials = openmc.Materials(all_materials.values())
materials.export_to_xml()


#### Create OpenMC "geometry.xml" file
openmc_geometry.export_to_xml()


#### Create OpenMC "settings.xml" file

# Construct uniform initial source distribution over fissionable zones
lower_left = [-32.12592, -32.12592, 192.5]
upper_right = [32.12592, 32.12592, 197.5]
lat_width = (np.array(upper_right) - np.array(lower_left))
lat_width[:2] /= 3.

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
plot.width = [64.25184, 64.25184]
plot.origin = [0., 0., 195.]
plot.color_by = 'material'
plot.filename = '2x2-reflector'
plot.pixels = [1000, 1000]

plot_file = openmc.Plots([plot])
plot_file.export_to_xml()


####  Create OpenMC "tallies.xml" file
tallies = openmc.Tallies()

# Extract all fuel materials
materials = openmc_geometry.get_materials_by_name(name='Fuel', matching=False)

# If using distribcells, create distribcell tally needed for depletion
if distrib == 'cell':
    fuel_cells = openmc_geometry.get_cells_by_name(
        name='enr radial 0: Fuel', case_sensitive=True, matching=False)
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
