from collections import OrderedDict, defaultdict
import copy
import os

import numpy as np

import openmc
import opendeplete


# FIXME: Export settings.xml with few particles
# FIXME: Run OpenMC to generate summary.h5 file

su = openmc.Summary('summary.h5')

# Extract all cells filled with a fuel material
fuel_cells = su.openmc_geometry.get_cells_by_name(
    name='radial 0: fuel', case_sensitive=True)

# Setup OpenDeplete Materials wrapper
materials = opendeplete.Materials()
materials.temperature = OrderedDict()
materials.sab = OrderedDict()
materials.initial_density = OrderedDict()
materials.burn = OrderedDict()
materials.cross_sections = os.environ["OPENMC_CROSS_SECTIONS"]

for cell in su.openmc_geometry.get_all_material_cells():
    materials.burn[cell.name] = 'fuel' in cell.fill.name.lower()
    materials.temperatures[cell.name] = cell.temperature[0]
    if len(cell.fill._sab) > 0:
        materials.sab[cell.name] = cell.fill._sab[0]

# Extract initial fuel nuclide densities in units of at/cc
for cell in fuel_cells:
    densities = cell.fill.get_nuclide_atom_densities()
    materials.initial_densities[cell.fill.name] = OrderedDict()

    # Convert atom densities from at/b-cm to at/cc
    for nuclide in densities:
        materials.initial_densities[cell.fill.name][nuclide.name] = \
            densities[nuclide][1] * 1e24

# Determine the maximum material ID
all_mats = su.opencg_geometry.get_all_materials()
max_material_id = 0
for material in all_mats:
    max_material_id = max(max_material_id, material.id)

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

settings.chain_file = "/home/wboyd/Documents/NSE-CRPG-Codes/opendeplete/chains/chain_full.xml"
settings.openmc_call = ["mpirun", "openmc"]
settings.particles = 10000
settings.batches = 100
settings.inactive = 10
settings.lower_left = [-10.70864, -10.70864, 192.5]
settings.upper_right = [10.70864, 10.70864, 197.5]
settings.entropy_dimension = [17, 17, 1]

settings.power = 2.337e15 * (17.**2 / 1.5**2)  # MeV/second cm from CASMO
settings.dt_vec = dt
settings.output_dir = 'test'

op = opendeplete.Operator(su.opencg_geometry, volumes, materials, settings)

# Perform simulation using the MCNPX/MCNP6 algorithm
opendeplete.integrate(op, opendeplete.ce_cm_c1)
