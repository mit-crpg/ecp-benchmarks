import numpy as np

import openmc
from smr.materials import materials
from smr.plots import plots
from smr.surfaces import lattice_pitch, bottom_fuel_stack, top_active_core
from smr.core import geometry


#### Create OpenMC "geometry.xml" file
geometry.export_to_xml()


#### Create OpenMC "materials.xml" file
materials.export_to_xml()


#### Create OpenMC "settings.xml" file

# Query the user on whether to use multipole cross sections
multipole = input('Use multipole cross sections? (y/n): ').lower()
multipole = (multipole == 'y')

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


#### Create OpenMC MGXS libraries

# Get all cells filled with a "fuel" material
mat_cells = geometry.get_all_material_cells()
fuel_cells = []
for cell in mat_cells:
    if 'fuel' in cell.fill.name.lower():
        fuel_cells.append(cell)

# CASMO 8-group structure
energy_groups = openmc.mgxs.EnergyGroups()
energy_groups.group_edges = np.array([0., 0.058e-6, 0.14e-6, 0.28e-6,
                                      0.625e-6, 4.e-6, 5.53e-3, 821.e-3, 20.])

# Initialize a 70-group "distribcell" MGXS library
cell_mgxs_lib = openmc.mgxs.Library(geometry, by_nuclide=True)
cell_mgxs_lib.energy_groups = energy_groups
cell_mgxs_lib.mgxs_types = ['total', 'nu-fission', 'nu-scatter matrix', 'chi']
cell_mgxs_lib.domain_type = 'distribcell'
cell_mgxs_lib.domains = fuel_cells
cell_mgxs_lib.correction = None
cell_mgxs_lib.build_library()

# Initialize a 70-group "material" MGXS library
mat_mgxs_lib = openmc.mgxs.Library(geometry, by_nuclide=True)
mat_mgxs_lib.energy_groups = energy_groups
mat_mgxs_lib.mgxs_types = ['total', 'nu-fission', 'nu-scatter matrix', 'chi']
mat_mgxs_lib.domain_type = 'material'
mat_mgxs_lib.correction = None
mat_mgxs_lib.build_library()


####  Create mesh tallies for verification of pin-wise reaction rates

# Instantiate a tally Mesh
mesh = openmc.Mesh(name='assembly mesh')
mesh.type = 'regular'
mesh.dimension = [7*17, 7*17, 100]
mesh.lower_left = lower_left
mesh.width = (np.array(upper_right) - np.array(lower_left))
mesh.width[:2] /= (7*17)
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