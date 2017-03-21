"""Creates a 2D 2x2 assembly colorset with periodic BCs."""

import os
import shutil

import numpy as np
import openmc

from geometry import beavrs, openmc_geometry


#### Create OpenMC "materials.xml" file
beavrs.write_openmc_materials()


#### Create OpenMC "geometry.xml" file
openmc_geometry.export_to_xml()


#### Create OpenMC "settings.xml" file

# Query the user on whether to use multipole cross sections
multipole = input('Use multipole cross sections? (y/n): ').lower()
multipole = (multipole == 'y')

# Construct uniform initial source distribution over fissionable zones
lower_left = [-21.41728, -21.41728, +192.5]
upper_right = [+21.41728, +21.41728, +197.5]
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
plot.width = [21.41728*2, 21.41728*2]
plot.origin = [0., 0., 195.]
plot.color_by = 'material'
plot.filename = '2x2-periodic'
plot.colors = beavrs.plots.colors_mat
plot.pixels = [1000, 1000]

plot_file = openmc.Plots([plot])
plot_file.export_to_xml()


#### Create OpenMC MGXS libraries

# Get all cells filled with a "fuel" material
fuel_cells = []
for cell in openmc_geometry.get_all_material_cells().values():
    if 'fuel' in cell.fill.name.lower():
        fuel_cells.append(cell)

# CASMO 70-group structure
energy_groups = openmc.mgxs.EnergyGroups()
energy_groups.group_edges = np.array([
    0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.042, 0.05, 0.058, 0.067,
    0.08, 0.1, 0.14, 0.18, 0.22, 0.25, 0.28, 0.3, 0.32, 0.35, 0.4, 0.5, 0.625,
    0.78, 0.85, 0.91, 0.95, 0.972, 0.996, 1.02, 1.045, 1.071, 1.097, 1.123,
    1.15, 1.3, 1.5, 1.855, 2.1, 2.6, 3.3, 4., 9.877, 15.968, 27.7, 48.052,
    75.501, 148.73, 367.26001, 906.90002, 1.4251e3, 2.2395e3, 3.5191e3, 5.53e3,
    9.118e3, 15.03e3, 24.78e3, 40.85e3, 67.34e3, 111.e3, 183e3, 302.5e3, 500e3,
    821e3, 1.353e6, 2.231e6, 3.679e6, 6.0655e6, 2e7])

# Initialize a 70-group "distribcell" MGXS library
cell_mgxs_lib = openmc.mgxs.Library(openmc_geometry, by_nuclide=True)
cell_mgxs_lib.energy_groups = energy_groups
cell_mgxs_lib.mgxs_types = ['total', 'nu-fission', 'nu-scatter matrix', 'chi']
cell_mgxs_lib.domain_type = 'distribcell'
cell_mgxs_lib.domains = fuel_cells
cell_mgxs_lib.correction = None
cell_mgxs_lib.build_library()

# Initialize a 70-group "material" MGXS library
mat_mgxs_lib = openmc.mgxs.Library(openmc_geometry, by_nuclide=True)
mat_mgxs_lib.energy_groups = energy_groups
mat_mgxs_lib.mgxs_types = ['total', 'nu-fission', 'nu-scatter matrix', 'chi']
mat_mgxs_lib.domain_type = 'material'
mat_mgxs_lib.correction = None
mat_mgxs_lib.build_library()


####  Create mesh tallies for verification of pin-wise reaction rates

# Instantiate a tally Mesh
mesh = openmc.Mesh(name='assembly mesh')
mesh.type = 'regular'
mesh.dimension = [34, 34, 1]
mesh.lower_left = lower_left
mesh.width = (np.array(upper_right) - np.array(lower_left))
mesh.width /= mesh.dimension
mesh_filter = openmc.MeshFilter(mesh)

# Instantiate energy-integrated fission rate mesh Tally
fission_rates = openmc.Tally(name='fission rates')
fission_rates.filters = [mesh_filter]
fission_rates.scores = ['fission']

# Instantiate energy-wise U-238 capture rate mesh Tally
capture_rates = openmc.Tally(name='u-238 capture')
capture_rates.filters = [mesh_filter]
capture_rates.nuclides = ['U238']
capture_rates.scores = ['absorption', 'fission']


####  Create OpenMC "tallies.xml" file

# Create a "tallies.xml" file for the mesh tallies
tallies_file = openmc.Tallies([fission_rates, capture_rates])
cell_mgxs_lib.add_to_tallies_file(tallies_file, merge=True)
mat_mgxs_lib.add_to_tallies_file(tallies_file, merge=True)
tallies_file.export_to_xml()


#### Move all XML files to 'fresh' directory

if not os.path.exists('fresh'):
    os.makedirs('fresh')
    
shutil.move('materials.xml', 'fresh/materials.xml')
shutil.move('geometry.xml', 'fresh/geometry.xml')
shutil.move('settings.xml', 'fresh/settings.xml')
shutil.move('tallies.xml', 'fresh/tallies.xml')
shutil.move('plots.xml', 'fresh/plots.xml')
