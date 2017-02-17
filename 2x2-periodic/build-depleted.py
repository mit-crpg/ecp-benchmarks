from collections import OrderedDict, defaultdict
import copy
import os

import numpy as np
import openmc
import opendeplete

from geometry import beavrs, openmc_geometry


#### Create "dummy" inputs to export distribcell paths for burnable cells

# Create OpenMC "materials.xml" file
beavrs.write_openmc_materials()

# Create OpenMC "geometry.xml" file
openmc_geometry.export_to_xml()

# Construct uniform initial source distribution over fissionable zones
lower_left = [-21.41728, -21.41728, +192.5]
upper_right = [+21.41728, +21.41728, +197.5]
source = openmc.source.Source(space=openmc.stats.Box(lower_left, upper_right))
source.space.only_fissionable = True

# Create OpenMC "settings.xml" file
settings_file = openmc.Settings()
settings_file.batches = 2
settings_file.inactive = 1
settings_file.particles = 10
settings_file.output = {'tallies': False}
settings_file.source = source
settings_file.sourcepoint_write = False
settings_file.export_to_xml()

#  Create OpenMC "tallies.xml" file
tallies = openmc.Tallies()
fuel_cells = openmc_geometry.get_cells_by_name(
    name='radial 0: Fuel', case_sensitive=True)

# Instantiate a "dummy" distribcell tally for each cell we wish to deplete
for cell in fuel_cells:
    tally = openmc.Tally(name='dummy distribcell tally')
    distribcell_filter = openmc.DistribcellFilter([cell.id])
    tally.filters = [distribcell_filter]
    tally.scores = ['fission']
    tallies.append(tally)

tallies.export_to_xml()

# Run OpenMC to generate summary.h5 file
openmc.run()

# Open "summary.h5" file
su = openmc.Summary('summary.h5')
fuel_cells = su.openmc_geometry.get_cells_by_name(
    name='radial 0: Fuel', case_sensitive=True)


#### Setup OpenDeplete Materials wrapper

materials = opendeplete.Materials()
materials.temperature = OrderedDict()
materials.sab = OrderedDict()
materials.initial_density = OrderedDict()
materials.burn = OrderedDict()
materials.cross_sections = os.environ["OPENMC_CROSS_SECTIONS"]

# Extract cell materials, temperatures and sab
for cell in su.openmc_geometry.get_all_material_cells():
    materials.burn[cell.name] = 'fuel' in cell.fill.name.lower()
    materials.temperature[cell.name] = cell.temperature[0]
    if len(cell.fill._sab) > 0:
        materials.sab[cell.name] = cell.fill._sab[0]

# Extract initial fuel nuclide densities in units of at/cc
for cell in fuel_cells:
    densities = cell.fill.get_nuclide_atom_densities()
    materials.initial_density[cell.fill.name] = OrderedDict()

    # Convert atom densities from at/b-cm to at/cc
    for nuclide in densities:
        materials.initial_density[cell.fill.name][nuclide.name] = \
            densities[nuclide][1] * 1e24

# Determine the maximum material ID
all_mats = su.openmc_geometry.get_all_materials()
max_material_id = 0
for material in all_mats:
    max_material_id = max(max_material_id, material.id)

# FIXME: Automatically extract info needed to calculate burnable cell volumes
# Fuel rod geometric parameters
radius = 0.39218
height = 5.

# Use defaultdict since OpenDeplete assumes volumes specified for all cells
volumes = defaultdict(lambda: 1)

# Assign distribmats for each material
for cell in fuel_cells:
    new_materials = []
    num_instances = len(cell.distribcell_paths)

    for i in range(num_instances):
        new_material = copy.deepcopy(cell.fill)
        new_material.id = max_material_id + 1
        max_material_id += 1
        new_materials.append(new_material)

        # Store volume of burnable fuel rods cells
        volumes[new_material.id] =  np.pi * radius**2 * height

    cell.fill = new_materials

# Create dt vector for 1 month with 15 day timesteps
dt1 = 15*24*60*60  # 15 days
dt2 = 1.*30*24*60*60  # 1 months
N = np.floor(dt2/dt1)
dt = np.repeat([dt1], N)

# Create settings variable
settings = opendeplete.Settings()

settings.openmc_call = ["mpirun", "openmc"]
settings.particles = 1000
settings.batches = 50
settings.inactive = 10
settings.lower_left = lower_left
settings.upper_right = upper_right
settings.entropy_dimension = [17*2, 17*2, 1]

settings.power = 2.337e15 * ((17.*17.*2.) / 1.5**2)  # MeV/second cm from CASMO
settings.dt_vec = dt
settings.output_dir = 'depleted'

op = opendeplete.Operator()
op.geometry_fill(su.openmc_geometry, volumes, materials, settings)

# Perform simulation using the MCNPX/MCNP6 algorithm
opendeplete.integrate(op, opendeplete.ce_cm_c1)
