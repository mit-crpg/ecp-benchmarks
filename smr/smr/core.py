"""Instantiate the main core lattice."""

import numpy as np

import openmc

from .materials import mats
from .surfaces import surfs, lattice_pitch
from .reflector import univs


#### CONSTRUCT MAIN CORE LATTICE

core = openmc.RectLattice(name='Main core')
core.lower_left = [-9*lattice_pitch/2, -9*lattice_pitch/2]
core.pitch = [lattice_pitch, lattice_pitch]
universes = np.tile(univs['heavy reflector'], (9,9))

universes[0, 2] = univs['heavy reflector 0,2']
universes[0, 3] = univs['heavy reflector 0,3']
universes[0, 4] = univs['heavy reflector 0,4']
universes[0, 5] = univs['heavy reflector 0,5']
universes[0, 6] = univs['heavy reflector 0,6']

universes[1, 1] = univs['heavy reflector 1,1']
universes[1, 2] = univs['heavy reflector NW']
universes[1, 3] = univs['Assembly (3.1%) instr']
universes[1, 4] = univs['Assembly (2.4%) CR D']
universes[1, 5] = univs['Assembly (3.1%) instr']
universes[1, 6] = univs['heavy reflector NE']
universes[1, 7] = univs['heavy reflector 1,7']

universes[2, 0] = univs['heavy reflector 2,0']
universes[2, 1] = univs['heavy reflector NW']
universes[2, 2] = univs['Assembly (3.1%) instr']
universes[2, 3] = univs['Assembly (2.4%) CR D']
universes[2, 4] = univs['Assembly (3.1%) 16BA']
universes[2, 5] = univs['Assembly (2.4%) CR D']
universes[2, 6] = univs['Assembly (3.1%) instr']
universes[2, 7] = univs['heavy reflector NE']
universes[2, 8] = univs['heavy reflector 2,8']

universes[3, 0] = univs['heavy reflector 3,0']
universes[3, 1] = univs['Assembly (3.1%) instr']
universes[3, 2] = univs['Assembly (2.4%) CR D']
universes[3, 3] = univs['Assembly (3.1%) 16BA']
universes[3, 4] = univs['Assembly (2.4%) CR D']
universes[3, 5] = univs['Assembly (3.1%) 16BA']
universes[3, 6] = univs['Assembly (2.4%) CR D']
universes[3, 7] = univs['Assembly (3.1%) instr']
universes[3, 8] = univs['heavy reflector 3,8']

universes[4, 0] = univs['heavy reflector 4,0']
universes[4, 1] = univs['Assembly (2.4%) CR D']
universes[4, 2] = univs['Assembly (3.1%) 16BA']
universes[4, 3] = univs['Assembly (2.4%) CR D']
universes[4, 4] = univs['Assembly (1.6%) instr']
universes[4, 5] = univs['Assembly (2.4%) CR D']
universes[4, 6] = univs['Assembly (3.1%) 16BA']
universes[4, 7] = univs['Assembly (2.4%) CR D']
universes[4, 8] = univs['heavy reflector 4,8']

universes[5, 0] = univs['heavy reflector 5,0']
universes[5, 1] = univs['Assembly (3.1%) instr']
universes[5, 2] = univs['Assembly (2.4%) CR D']
universes[5, 3] = univs['Assembly (3.1%) 16BA']
universes[5, 4] = univs['Assembly (2.4%) CR D']
universes[5, 5] = univs['Assembly (3.1%) 16BA']
universes[5, 6] = univs['Assembly (2.4%) CR D']
universes[5, 7] = univs['Assembly (3.1%) instr']
universes[5, 8] = univs['heavy reflector 5,8']

universes[6, 0] = univs['heavy reflector 6,0']
universes[6, 1] = univs['heavy reflector SW']
universes[6, 2] = univs['Assembly (3.1%) instr']
universes[6, 3] = univs['Assembly (2.4%) CR D']
universes[6, 4] = univs['Assembly (3.1%) 16BA']
universes[6, 5] = univs['Assembly (2.4%) CR D']
universes[6, 6] = univs['Assembly (3.1%) instr']
universes[6, 7] = univs['heavy reflector SE']
universes[6, 8] = univs['heavy reflector 6,8']

universes[7, 1] = univs['heavy reflector 7,1']
universes[7, 2] = univs['heavy reflector SW']
universes[7, 3] = univs['Assembly (3.1%) instr']
universes[7, 4] = univs['Assembly (2.4%) CR D']
universes[7, 5] = univs['Assembly (3.1%) instr']
universes[7, 6] = univs['heavy reflector SE']
universes[7, 7] = univs['heavy reflector 7,7']

universes[8, 2] = univs['heavy reflector 8,2']
universes[8, 3] = univs['heavy reflector 8,3']
universes[8, 4] = univs['heavy reflector 8,4']
universes[8, 5] = univs['heavy reflector 8,5']
universes[8, 6] = univs['heavy reflector 8,6']

core.universes = universes


#### CONSTRUCT ROOT UNIVERSE AND CELLS

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


#### CONSTRUCT NEUTRON SHIELD PANELS

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


#### CONSTRUCT DOWNCOMER

cell = openmc.Cell(name='downcomer')
cell.fill = mats['H2O']
cell.region = (+surfs['neutron shield OR'] & -surfs['RPV IR'] &
               +surfs['lower bound'] & -surfs['upper bound'])
root_univ.add_cell(cell)


#### CONSTRUCT REACTOR PRESSURE VESSEL

cell = openmc.Cell(name='reactor pressure vessel')
cell.fill = mats['CS']
cell.region = (+surfs['RPV IR'] & -surfs['RPV OR'] &
               +surfs['lower bound'] & -surfs['upper bound'])
root_univ.add_cell(cell)


#### CONSTRUCT GEOMETRY

geometry = openmc.Geometry(root_univ)
