from collections import OrderedDict
import copy
import os

import numpy as np
import openmc
import opendeplete

from geometry import beavrs, openmc_geometry


# Setup OpenDeplete Materials wrapper
materials = opendeplete.Materials()
materials.temperature = OrderedDict()
materials.sab = OrderedDict()
materials.initial_density = OrderedDict()
materials.burn = OrderedDict()
materials.cross_sections = os.environ["OPENMC_CROSS_SECTIONS"]

# Count the number of instances for each cell and material
openmc_geometry.determine_paths()

# Extract all cells filled by a fuel material
fuel_cells = openmc_geometry.get_cells_by_name(
    name='enr radial 0: Fuel', case_sensitive=True)

# Extract cell materials, temperatures and sab
for cell in openmc_geometry.get_all_material_cells().values():
    materials.burn[cell.name] = 'fuel' in cell.fill.name.lower()
    materials.temperature[cell.name] = 300
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
max_material_id = 0
for material in openmc_geometry.get_all_materials().values():
    max_material_id = max(max_material_id, material.id)

# FIXME: Automatically extract info needed to calculate burnable cell volumes
# Fuel rod geometric parameters
radius = 0.39218
height = 5.

# Assign distribmats for each material
for cell in fuel_cells:
    new_materials = []

    for i in range(cell.num_instances):
        new_material = copy.deepcopy(cell.fill)
        new_material.id = max_material_id + 1
        max_material_id += 1
        new_materials.append(new_material)

        # Store volume of burnable fuel rods cells
        new_material.volume = np.pi * radius**2 * height
        new_material.depletable = True
        new_material.temperature = 300

    cell.fill = new_materials

# Create dt vector for 1 month with 5 day timesteps
dt1 = 5*24*60*60  # 5 days
dt2 = 1.*30*24*60*60  # 1 months
N = np.floor(dt2/dt1)
dt = np.repeat([dt1], N)

# Create settings variable
settings = opendeplete.OpenMCSettings()
settings.openmc_call = ["mpirun", "openmc"]
settings.particles = 120000
settings.batches = 20
settings.inactive = 10
settings.lower_left = [-21.41728, -21.41728, +192.5]
settings.upper_right = [+21.41728, +21.41728, +197.5]
settings.entropy_dimension = [17*2, 17*2, 1]

# MeV/second cm from CASMO
settings.power = 2.337e15 * ((17.*17.*2.) / 1.5**2) * height
settings.dt_vec = dt
settings.output_dir = 'depleted'

op = opendeplete.OpenMCOperator(openmc_geometry, settings)

# Perform simulation using the MCNPX/MCNP6 algorithm
opendeplete.integrate(op, opendeplete.ce_cm_c1)
