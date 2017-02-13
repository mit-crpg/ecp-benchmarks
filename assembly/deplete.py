from collections import OrderedDict
import copy
import os

import numpy as np

import openmc
import opendeplete


# FIXME: Export settings.xml with few particles
# FIXME: Run OpenMC to generate summary.h5 file

su = openmc.Summary('summary.h5')

geometry = su.openmc_geometry

fuel_cells = geometry.get_cells_by_name(name='radial 0: fuel', case_sensitive=True)
print(fuel_cells)

temperatures = OrderedDict()
sab = OrderedDict()
burn = OrderedDict()

mat_cells = geometry.get_all_material_cells()
for cell in mat_cells:
    temperatures[cell.fill.name] = cell.temperature
    if len(cell.fill._sab) > 0:
        sab[cell.fill.name] = cell.fill._sab[0]
    burn[cell.fill.name] = 'fuel' in cell.fill.name.lower()

# FIXME: Get initial densities
initial_densities = OrderedDict()
for cell in mat_cells:
    densities = cell.fill.get_nuclide_atom_densities()
    initial_densities[cell.fill.name] = OrderedDict()

    # Convert atom densities from at/b-cm to at/cc
    for nuclide in densities:
        initial_densities[cell.fill.name][nuclide.name] = \
            densities[nuclide][1] * 1e24

# Setup OpenDeplete Materials wrapper
materials = opendeplete.Materials()
materials.temperature = temperatures
materials.sab = sab
materials.initial_density = initial_densities
materials.burn = burn
materials.cross_sections = os.environ["OPENMC_CROSS_SECTIONS"]

# FIXME: Assign distribmats for each material
volumes = OrderedDict()
for cell in fuel_cells:
    new_materials = []
    num_instances = len(cell.distribcell_paths)

    for i in range(num_instances):
        new_material = copy.deepcopy(cell.fill)
        new_material.id = None
        new_materials.append(new_material)

        # FIXME: Compute volumes of burnable cells
        volumes[new_material.id] =  np.pi * 0.39218**2 * 5.

    cell.fill = new_materials

# Create dt vector for 1 month with 15 day timesteps
dt1 = 15*24*60*60  # 15 days
dt2 = 1.*30*24*60*60  # 1 months
N = np.floor(dt2/dt1)
dt = np.repeat([dt1], N)

# Create settings variable
settings = opendeplete.Settings()

settings.chain_file = "/home/wboyd/Documents/NSE-CRPG-Codes/opendeplete/chains/chain_simple.xml"
settings.openmc_call = ["mpirun", "openmc"]
settings.particles = 1000
settings.batches = 100
settings.inactive = 10
settings.lower_left = [-10.70864, -10.70864, 192.5]
settings.upper_right = [10.70864, 10.70864, 197.5]
settings.entropy_dimension = [17, 17, 1]

settings.power = 2.337e15 * (17.**2 / 1.5**2)  # MeV/second cm from CASMO
settings.dt_vec = dt
settings.output_dir = 'test'

op = opendeplete.Operator(geometry, volumes, materials, settings)

# Perform simulation using the MCNPX/MCNP6 algorithm
opendeplete.integrate(op, opendeplete.ce_cm_c1)
