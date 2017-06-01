#!/usr/bin/env python3

import numpy as np
import opendeplete

from geometry import openmc_geometry


# FIXME: Automatically extract info needed to calculate burnable cell volumes
# Fuel rod geometric parameters
radius = 0.39218
height = 5.

# Count the number of instances for each cell and material
openmc_geometry.determine_paths(instances_only=True)

# Extract all cells filled by a fuel material
fuel_cells = openmc_geometry.get_cells_by_name(
    name='enr radial 0: Fuel', case_sensitive=True)

# Assign distribmats for each material
for cell in fuel_cells:
    cell.fill.volume = np.pi * radius**2 * height
    cell.fill.depletable = True
    cell.fill.temperature = 300.0

    cell.fill = [cell.fill.clone() for i in range(cell.num_instances)]

# Set temperature for all cells
cells = openmc_geometry.get_all_cells()

for cell_id in cells:
    cells[cell_id].temperature = 300.0

# Create dt vector for 1 month with 5 day timesteps
dt1 = 5*24*60*60  # 5 days
dt2 = 1.*30*24*60*60  # 1 months
N = np.floor(dt2/dt1)
dt = np.repeat([dt1], N)

# Create settings variable
settings = opendeplete.OpenMCSettings()
settings.openmc_call = "openmc"
settings.particles = 30000
settings.batches = 20
settings.inactive = 10
settings.lower_left = [-10.70864, -10.70864, +192.5]
settings.upper_right = [+10.70864, +10.70864, +197.5]
settings.entropy_dimension = [17, 17, 1]

# MeV/second cm from CASMO
settings.power = 2.337e15 * (17.**2 / 1.5**2) * height
settings.dt_vec = dt
settings.output_dir = 'depleted'

op = opendeplete.OpenMCOperator(openmc_geometry, settings)

# Perform simulation using the MCNPX/MCNP6 algorithm
opendeplete.cecm(op)
