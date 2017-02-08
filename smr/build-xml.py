import numpy as np

import openmc

from surfaces import lattice_pitch, bottom_fuel_stack, top_active_core
from core import geometry
from materials import materials
from plots import plots


#### Create OpenMC "geometry.xml" file
geometry.export_to_xml()


#### Create OpenMC "materials.xml" file
materials.export_to_xml()


##### Create OpenMC "settings.xml" file

# Query the user on whether to use multipole cross sections
multipole = input('Use multipole cross sections? (y/n): ').lower()
multipole = True if multipole == 'y' else False

# Construct uniform initial source distribution over fissionable zones
lower_left = [-7.*lattice_pitch/2., -7.*lattice_pitch/2., bottom_fuel_stack]
upper_right = [+7.*lattice_pitch/2., +7.*lattice_pitch/2., top_active_core]
source = openmc.source.Source(space=openmc.stats.Box(lower_left, upper_right))
source.space.only_fissionable = True

settings_file = openmc.Settings()
settings_file.batches = 10
settings_file.inactive = 5
settings_file.particles = 10000
settings_file.ptables = True
settings_file.output = {'tallies': False}
settings_file.source = source
settings_file.sourcepoint_write = False

if multipole:
    settings_file.temperature = {'multipole': True, 'tolerance': 1000}

settings_file.export_to_xml()


#### Create OpenMC "plots.xml" file
plots.export_to_xml()


#### Create OpenMC "tallies.xml" file

# Create a pin-wise mesh
mesh = openmc.Mesh(name='pin-wise mesh')
mesh.type = 'regular'
mesh.dimension = [7*17, 7*17]
mesh.lower_left = lower_left[:2]
mesh.width = np.array(upper_right[:2]) - np.array(lower_left[:2])
mesh_filter = openmc.MeshFilter(mesh)

# Create a fission rate mesh tally
fission_rates = openmc.Tally(name='fission rates')
fission_rates.filters = [mesh_filter]
fission_rates.scores = ['fission']

# Export tallies to XML
tallies_file = openmc.Tallies([fission_rates])
tallies_file.export_to_xml()
