import numpy as np

import openmc

from materials import mats
from surfaces import surfs, lattice_pitch
from baffle import univs


# CONSTRUCT MAIN CORE LATTICE

core = openmc.RectLattice(name='Main core')
core.lower_left = [-19.*lattice_pitch/2., -19.*lattice_pitch/2.]
core.pitch = [lattice_pitch, lattice_pitch]
universes = np.empty((19,19), dtype=openmc.Universe)
universes[:,:] = univs['water pin']
core.universes = universes

core.universes[5, 7] = univs['baffle southeast corner']
core.universes[5, 8] = univs['baffle south']
core.universes[5, 9] = univs['baffle south']
core.universes[5, 10] = univs['baffle south']
core.universes[5, 11] = univs['baffle southwest corner']

core.universes[6, 6] = univs['baffle southeast corner']
core.universes[6, 7] = univs['baffle southeast']
core.universes[6, 8] = univs['Assembly (3.1\%) instr']
core.universes[6, 9] = univs['Assembly (1.6\%) CR B']
core.universes[6, 10] = univs['Assembly (3.1\%) instr']
core.universes[6, 11] = univs['baffle southwest']
core.universes[6, 12] = univs['baffle southwest corner']

core.universes[7, 5] = univs['baffle southeast corner']
core.universes[7, 6] = univs['baffle southeast']
core.universes[7, 7] = univs['Assembly (3.1\%) instr']
core.universes[7, 8] = univs['Assembly (1.6\%) CR B']
core.universes[7, 9] = univs['Assembly (3.1\%) 16BA']
core.universes[7, 10] = univs['Assembly (1.6\%) CR B']
core.universes[7, 11] = univs['Assembly (3.1\%) instr']
core.universes[7, 12] = univs['baffle southwest']
core.universes[7, 13] = univs['baffle southwest corner']

core.universes[8, 5] = univs['baffle east']
core.universes[8, 6] = univs['Assembly (3.1\%) instr']
core.universes[8, 7] = univs['Assembly (1.6\%) CR B']
core.universes[8, 8] = univs['Assembly (3.1\%) 16BA']
core.universes[8, 9] = univs['Assembly (2.4\%) CR D']
core.universes[8, 10] = univs['Assembly (3.1\%) 16BA']
core.universes[8, 11] = univs['Assembly (1.6\%) CR B']
core.universes[8, 12] = univs['Assembly (3.1\%) instr']
core.universes[8, 13] = univs['baffle west']

core.universes[9, 5] = univs['baffle east']
core.universes[9, 6] = univs['Assembly (1.6\%) CR B']
core.universes[9, 7] = univs['Assembly (3.1\%) 16BA']
core.universes[9, 8] = univs['Assembly (2.4\%) CR D']
core.universes[9, 9] = univs['Assembly (1.6\%) instr']
core.universes[9, 10] = univs['Assembly (2.4\%) CR D']
core.universes[9, 11] = univs['Assembly (3.1\%) 16BA']
core.universes[9, 12] = univs['Assembly (1.6\%) CR B']
core.universes[9, 13] = univs['baffle west']

core.universes[10, 5] = univs['baffle east']
core.universes[10, 6] = univs['Assembly (3.1\%) instr']
core.universes[10, 7] = univs['Assembly (1.6\%) CR B']
core.universes[10, 8] = univs['Assembly (3.1\%) 16BA']
core.universes[10, 9] = univs['Assembly (2.4\%) CR D']
core.universes[10, 10] = univs['Assembly (3.1\%) 16BA']
core.universes[10, 11] = univs['Assembly (1.6\%) CR B']
core.universes[10, 12] = univs['Assembly (3.1\%) instr']
core.universes[10, 13] = univs['baffle west']

core.universes[11, 5] = univs['baffle northeast corner']
core.universes[11, 6] = univs['baffle northeast']
core.universes[11, 7] = univs['Assembly (3.1\%) instr']
core.universes[11, 8] = univs['Assembly (1.6\%) CR B']
core.universes[11, 9] = univs['Assembly (3.1\%) 16BA']
core.universes[11, 10] = univs['Assembly (1.6\%) CR B']
core.universes[11, 11] = univs['Assembly (3.1\%) instr']
core.universes[11, 12] = univs['baffle northwest']
core.universes[11, 13] = univs['baffle northwest corner']

core.universes[12, 6] = univs['baffle northeast corner']
core.universes[12, 7] = univs['baffle northeast']
core.universes[12, 8] = univs['Assembly (3.1\%) instr']
core.universes[12, 9] = univs['Assembly (1.6\%) CR B']
core.universes[12, 10] = univs['Assembly (3.1\%) instr']
core.universes[12, 11] = univs['baffle northwest']
core.universes[12, 12] = univs['baffle northwest corner']

core.universes[13, 7] = univs['baffle northeast corner']
core.universes[13, 8] = univs['baffle north']
core.universes[13, 9] = univs['baffle north']
core.universes[13, 10] = univs['baffle north']
core.universes[13, 11] = univs['baffle northwest corner']


# CONSTRUCT ROOT UNIVERSE AND CELLS

root_univ = openmc.Universe(universe_id=0, name='root universe')

cell = openmc.Cell(name='Main core')
cell.fill = core
cell.region = \
    -surfs['core barrel IR'] & +surfs['lower bound'] & -surfs['upper bound']
root_univ.add_cell(cell)


# CONSTRUCT CORE BARREL

cell = openmc.Cell(name='core barrel')
cell.fill = mats['SS']
cell.region = (+surfs['core barrel IR'] & -surfs['core barrel OR'] &
               +surfs['lower bound'] & -surfs['upper bound'])
root_univ.add_cell(cell)


# CONSTRUCT SHIELD PANELS

cell = openmc.Cell(name='neutron shield panel NW')
cell.fill = mats['SS']
cell.region = (+surfs['core barrel OR'] & -surfs['neutron shield OR'] &
               +surfs['neutron shield NWbot SEtop'] &
               -surfs['neutron shield NWtop SEbot'] &
               +surfs['lower bound'] & -surfs['upper bound'])
root_univ.add_cell(cell)

cell = openmc.Cell(name='neutron shield panel N')
cell.fill = mats['H2O']
cell.region = (+surfs['core barrel OR'] & -surfs['neutron shield OR'] &
               +surfs['neutron shield NWtop SEbot'] &
               -surfs['neutron shield NEtop SWbot'] &
               +surfs['lower bound'] & -surfs['upper bound'])
root_univ.add_cell(cell)

cell = openmc.Cell(name='neutron shield panel SE')
cell.fill = mats['SS']
cell.region = (+surfs['core barrel OR'] & -surfs['neutron shield OR'] &
               -surfs['neutron shield NWbot SEtop'] &
               +surfs['neutron shield NWtop SEbot'] &
               +surfs['lower bound'] & -surfs['upper bound'])
root_univ.add_cell(cell)

cell = openmc.Cell(name='neutron shield panel E')
cell.fill = mats['H2O']
cell.region = (+surfs['core barrel OR'] & -surfs['neutron shield OR'] &
               +surfs['neutron shield NWbot SEtop'] &
               +surfs['neutron shield NEbot SWtop'] &
               +surfs['lower bound'] & -surfs['upper bound'])
root_univ.add_cell(cell)

cell = openmc.Cell(name='neutron shield panel NE')
cell.fill = mats['SS']
cell.region = (+surfs['core barrel OR'] & -surfs['neutron shield OR'] &
               +surfs['neutron shield NEbot SWtop'] &
               -surfs['neutron shield NEtop SWbot'] &
               +surfs['lower bound'] & -surfs['upper bound'])
root_univ.add_cell(cell)

cell = openmc.Cell(name='neutron shield panel S')
cell.fill = mats['H2O']
cell.region = (+surfs['core barrel OR'] & -surfs['neutron shield OR'] &
               -surfs['neutron shield NWtop SEbot'] &
               +surfs['neutron shield NEtop SWbot'] &
               +surfs['lower bound'] & -surfs['upper bound'])
root_univ.add_cell(cell)

cell = openmc.Cell(name='neutron shield panel SW')
cell.fill = mats['SS']
cell.region = (+surfs['core barrel OR'] & -surfs['neutron shield OR'] &
               -surfs['neutron shield NEbot SWtop'] &
               +surfs['neutron shield NEtop SWbot'] &
               +surfs['lower bound'] & -surfs['upper bound'])
root_univ.add_cell(cell)

cell = openmc.Cell(name='neutron shield panel W')
cell.fill = mats['H2O']
cell.region = (+surfs['core barrel OR'] & -surfs['neutron shield OR'] &
               -surfs['neutron shield NWbot SEtop'] &
               -surfs['neutron shield NEbot SWtop'] &
               +surfs['lower bound'] & -surfs['upper bound'])
root_univ.add_cell(cell)


# CONSTRUCT DOWNCOMER

cell = openmc.Cell(name='downcomer')
cell.fill = mats['H2O']
cell.region = (+surfs['neutron shield OR'] & -surfs['RPV IR'] &
               +surfs['lower bound'] & -surfs['upper bound'])
root_univ.add_cell(cell)


# CONSTRUCT REACTOR PRESSURE VESSEL

cell = openmc.Cell(name='reactor pressure vessel')
cell.fill = mats['CS']
cell.region = (+surfs['RPV IR'] & -surfs['RPV OR'] &
               +surfs['lower bound'] & -surfs['upper bound'])
root_univ.add_cell(cell)


# CONSTRUCT GEOMETRY

geometry = openmc.Geometry()
geometry.root_universe = root_univ
