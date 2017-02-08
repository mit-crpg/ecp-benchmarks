"""Instantiate each fuel assembly as an OpenMC Lattice."""

import numpy as np

import openmc

from .materials import mats
from .surfaces import surfs, pin_pitch
from .pins import univs


def make_assembly(name, universes):
    """Instantiate an OpenMC Lattice for this fuel assembly.

    This method creates a 17x17 PWR lattice with axially spaced
    sleeves defined in the global surfs dictionary.

    Parameters
    ----------
    name: str
        The string name to assign to the Lattice
    universes: numpy.ndarray of openmc.Universe
        A 2D NumPy array of Universes to use for the Lattice

    Returns
    -------
    universe: openmc.Universe
        A Universe with a Cell filled by the Lattice
    """

    # Instantiate the lattice
    lattice = openmc.RectLattice(name=name)
    lattice.lower_left = [-17.*pin_pitch/2., -17.*pin_pitch/2.]
    lattice.pitch = [pin_pitch, pin_pitch]
    lattice.universes = universes

    # Create rectangular prism cylinder for lattice grid box
    lat_grid_box = (surfs['lat grid box outer'] &
                    openmc.Complement(surfs['lat grid box inner']))

    # Add lattice to bounding cell
    univ_name = name + ' lattice'
    universe = openmc.Universe(name=univ_name)
    cell = openmc.Cell(name=univ_name)
    cell.fill = lattice
    cell.region = surfs['lat grid box inner']
    universe.add_cell(cell)

    # Add outer water cell
    cell = openmc.Cell(name=univ_name + ' outer water')
    cell.fill = univs['water pin']
    cell.region = openmc.Complement(surfs['lat grid box outer'])
    universe.add_cell(cell)

    # Make bottom axial cell for outside of assembly (without sleeve)
    cell = openmc.Cell(name=univ_name + ' axial (0)')
    cell.fill = mats['H2O']
    cell.region = lat_grid_box & -surfs['grid1bot']
    universe.add_cell(cell)

    # Make axial cell for outside of assembly (with sleeve)
    cell = openmc.Cell(name=univ_name + ' axial (1)')
    cell.fill = mats['SS']
    cell.region = lat_grid_box & +surfs['grid1bot'] & -surfs['grid1top']
    universe.add_cell(cell)

    # Make axial cell for outside of assembly (without sleeve)
    cell = openmc.Cell(name=univ_name + ' axial (2)')
    cell.fill = mats['H2O']
    cell.region = lat_grid_box & +surfs['grid1top'] & -surfs['grid2bot']
    universe.add_cell(cell)

    # Make axial cell for outside of assembly (with sleeve)
    cell = openmc.Cell(name=univ_name + ' axial (3)')
    cell.fill = mats['Zr']
    cell.region = lat_grid_box & +surfs['grid2bot'] & -surfs['grid2top']
    universe.add_cell(cell)

    # Make axial cell for outside of assembly (without sleeve)
    cell = openmc.Cell(name=univ_name + ' axial (4)')
    cell.fill = mats['H2O']
    cell.region = lat_grid_box & +surfs['grid2top'] & -surfs['grid3bot']
    universe.add_cell(cell)

    # Make axial cell for outside of assembly (with sleeve)
    cell = openmc.Cell(name=univ_name + ' axial (5)')
    cell.fill = mats['Zr']
    cell.region = lat_grid_box & +surfs['grid3bot'] & -surfs['grid3top']
    universe.add_cell(cell)

    # Make axial cell for outside of assembly (without sleeve)
    cell = openmc.Cell(name=univ_name + ' axial (6)')
    cell.fill = mats['H2O']
    cell.region = lat_grid_box & +surfs['grid3top'] & -surfs['grid4bot']
    universe.add_cell(cell)

    # Make axial cell for outside of assembly (with sleeve)
    cell = openmc.Cell(name=univ_name + ' axial (7)')
    cell.fill = mats['SS']
    cell.region = lat_grid_box & +surfs['grid4bot'] & -surfs['grid4top']
    universe.add_cell(cell)

    # Make top axial cell for outside of assembly (without sleeve)
    cell = openmc.Cell(name=univ_name + ' axial (last)')
    cell.fill = mats['H2O']
    cell.region = lat_grid_box & +surfs['grid4top']
    universe.add_cell(cell)

    return universe


# commonly needed universes
gtu = univs['GT empty']
gti = univs['GT empty instr']
bas = univs['BA stack']
ins = univs['IT stack']
crA = univs['GT CR bank A']
crB = univs['GT CR bank B']
crC = univs['GT CR bank C']
crD = univs['GT CR bank D']
crSA = univs['GT CR bank SA']
crSB = univs['GT CR bank SB']
crSC = univs['GT CR bank SC']
crSD = univs['GT CR bank SD']
crSE = univs['GT CR bank SE']


# Define the NumPy array indices for assembly locations where there
# may be CR guide tubes, instrument tubes and burnable absorbers
nonfuel_y = \
    np.array([2,2,2,3,3,5,5,5,5,5,8,8,8,8,8,11,11,11,11,11,13,13,14,14,14])
nonfuel_x = \
    np.array([5,8,11,3,13,2,5,8,11,14,2,5,8,11,14,2,5,8,11,14,3,13,5,8,11])


#### 1.6% ENRICHED ASSEMBLIES

for cent, comment in [(gti, ''), (ins, ' instr')]:

    # NO BURNABLE ABSORBERS
    universes = np.empty((17,17), dtype=openmc.Universe)
    universes[:,:] = univs['Fuel (1.6\%) stack']
    universes[nonfuel_y, nonfuel_x] = [    gtu,   gtu,   gtu,
                                         gtu,              gtu,
                                       gtu, gtu,  gtu,  gtu, gtu,
                                       gtu, gtu,  cent, gtu, gtu,
                                       gtu, gtu,  gtu,  gtu, gtu,
                                         gtu,              gtu,
                                           gtu,   gtu,   gtu     ]
    univs['Assembly (1.6\%)' + comment] = \
        make_assembly('Assembly (1.6\%) no BAs' + comment, universes)

    # WITH EACH CONTROL ROD BANK
    for bank, comment2 in [(crA, 'A'), (crB, 'B'), (crC, 'C'), (crD, 'D'),
                 (crSB, 'SB'), (crSC, 'SC'), (crSD, 'SD'), (crSE, 'SE')]:

        universes = np.empty((17,17), dtype=openmc.Universe)
        universes[:,:] = univs['Fuel (1.6\%) stack']
        universes[nonfuel_y, nonfuel_x] = [    bank,    bank,   bank,
                                             bank,                 bank,
                                           bank, bank,  bank,  bank, bank,
                                           bank, bank,  cent,  bank, bank,
                                           bank, bank,  bank,  bank, bank,
                                             bank,                 bank,
                                               bank,    bank,   bank     ]
        univs['Assembly (1.6\%) CR {}'.format(comment2) + comment] = \
            make_assembly('Assembly (1.6\%) CR {}'.format(comment2) + comment, universes)


#### 2.4% ENRICHED ASSEMBLIES

for cent, comment in [(gti, ''), (ins, ' instr')]:

    # NO BURNABLE ABSORBERS
    universes = np.empty((17,17), dtype=openmc.Universe)
    universes[:,:] = univs['Fuel (2.4\%) stack']
    universes[nonfuel_y, nonfuel_x] = [    gtu,   gtu,   gtu,
                                         gtu,              gtu,
                                       gtu, gtu,  gtu,  gtu, gtu,
                                       gtu, gtu,  cent, gtu, gtu,
                                       gtu, gtu,  gtu,  gtu, gtu,
                                         gtu,              gtu,
                                           gtu,   gtu,   gtu     ]
    univs['Assembly (2.4\%) no BAs' + comment] = \
        make_assembly('Assembly (2.4\%) no BAs' + comment, universes)

    # WITH CONTROL ROD D BANK
    universes = np.empty((17,17), dtype=openmc.Universe)
    universes[:,:] = univs['Fuel (2.4\%) stack']
    universes[nonfuel_y, nonfuel_x] = [    crD,   crD,   crD,
                                         crD,              crD,
                                       crD, crD,  crD,  crD, crD,
                                       crD, crD,  cent, crD, crD,
                                       crD, crD,  crD,  crD, crD,
                                         crD,              crD,
                                           crD,   crD,   crD     ]
    univs['Assembly (2.4\%) CR D' + comment] = \
        make_assembly('Assembly (2.4\%) CR D' + comment, universes)

    # WITH 12 BURNABLE ABSORBERS
    universes = np.empty((17,17), dtype=openmc.Universe)
    universes[:,:] = univs['Fuel (2.4\%) stack']
    universes[nonfuel_y, nonfuel_x] = [    bas,   gtu,   bas,
                                         bas,              bas,
                                       bas, gtu,  gtu,  gtu, bas,
                                       gtu, gtu,  cent, gtu, gtu,
                                       bas, gtu,  gtu,  gtu, bas,
                                         bas,              bas,
                                           bas,   gtu,   bas     ]
    univs['Assembly (2.4\%) 12BA' + comment] = \
        make_assembly('Assembly (2.4\%) 12BA' + comment, universes)

    # WITH 16 BURNABLE ABSORBERS
    universes = np.empty((17,17), dtype=openmc.Universe)
    universes[:,:] = univs['Fuel (2.4\%) stack']
    universes[nonfuel_y, nonfuel_x] = [    bas,   bas,   bas,
                                         bas,              bas,
                                       bas, gtu,  gtu,  gtu, bas,
                                       bas, gtu,  cent, gtu, bas,
                                       bas, gtu,  gtu,  gtu, bas,
                                         bas,              bas,
                                           bas,   bas,   bas     ]
    univs['Assembly (2.4\%) 16BA' + comment] = \
        make_assembly('Assembly (2.4\%) 16BA' + comment, universes)


#### 3.1% ENRICHED ASSEMBLIES

for cent, comment in [(gti, ''), (ins, ' instr')]:

    # NO BURNABLE ABSORBERS
    universes = np.empty((17,17), dtype=openmc.Universe)
    universes[:,:] = univs['Fuel (3.1\%) stack']
    universes[nonfuel_y, nonfuel_x] = [    gtu,   gtu,   gtu,
                                         gtu,              gtu,
                                       gtu, gtu,  gtu,  gtu, gtu,
                                       gtu, gtu,  cent, gtu, gtu,
                                       gtu, gtu,  gtu,  gtu, gtu,
                                         gtu,              gtu,
                                           gtu,   gtu,   gtu     ]
    univs['Assembly (3.1\%)' + comment] = \
        make_assembly('Assembly (3.1\%) no BAs' + comment, universes)

    # WITH CONTROL ROD SA BANK
    universes = np.empty((17,17), dtype=openmc.Universe)
    universes[:,:] = univs['Fuel (3.1\%) stack']
    universes[nonfuel_y, nonfuel_x] = [     crSA,    crSA,   crSA,
                                          crSA,                crSA,
                                       crSA,  crSA,  crSA,  crSA,  crSA,
                                       crSA,  crSA,  cent,  crSA,  crSA,
                                       crSA,  crSA,  crSA,  crSA,  crSA,
                                          crSA,                crSA,
                                            crSA,    crSA,   crSA     ]
    univs['Assembly (3.1\%) CR SA' + comment] = \
        make_assembly('Assembly (3.1\%) CR SA' + comment, universes)

    # WITH 20 BURNABLE ABSORBERS
    universes = np.empty((17,17), dtype=openmc.Universe)
    universes[:,:] = univs['Fuel (3.1\%) stack']
    universes[nonfuel_y, nonfuel_x] = [    bas,   bas,   bas,
                                         bas,              bas,
                                       bas, bas,  gtu,  bas, bas,
                                       bas, gtu,  cent, gtu, bas,
                                       bas, bas,  gtu,  bas, bas,
                                         bas,              bas,
                                           bas,   bas,   bas     ]
    univs['Assembly (3.1\%) 20BA' + comment] = \
        make_assembly('Assembly (3.1\%) 20BA' + comment, universes)

    # WITH 16 BURNABLE ABSORBERS
    universes = np.empty((17,17), dtype=openmc.Universe)
    universes[:,:] = univs['Fuel (3.1\%) stack']
    universes[nonfuel_y, nonfuel_x] = [    bas,   bas,   bas,
                                         bas,              bas,
                                       bas, gtu,  gtu,  gtu, bas,
                                       bas, gtu,  cent, gtu, bas,
                                       bas, gtu,  gtu,  gtu, bas,
                                         bas,              bas,
                                           bas,   bas,   bas     ]
    univs['Assembly (3.1\%) 16BA' + comment] = \
        make_assembly('Assembly (3.1\%) 16BA' + comment, universes)

    # WITH 15 BURNABLE ABSORBERS NW
    universes = np.empty((17,17), dtype=openmc.Universe)
    universes[:,:] = univs['Fuel (3.1\%) stack']
    universes[nonfuel_y, nonfuel_x] = [    gtu,   gtu,   gtu,
                                         gtu,              gtu,
                                       gtu, bas,  bas,  bas, bas,
                                       gtu, bas,  cent, bas, bas,
                                       gtu, bas,  bas,  bas, bas,
                                         gtu,              bas,
                                           bas,   bas,   bas     ]
    univs['Assembly (3.1\%) 15BANW' + comment] = \
        make_assembly('Assembly (3.1\%) 15BANW' + comment, universes)

    # WITH 15 BURNABLE ABSORBERS NE
    universes = np.empty((17,17), dtype=openmc.Universe)
    universes[:,:] = univs['Fuel (3.1\%) stack']
    universes[nonfuel_y, nonfuel_x] = [    gtu,   gtu,   gtu,
                                         gtu,              gtu,
                                       gtu, bas,  bas,  bas, gtu,
                                       bas, bas,  cent, bas, gtu,
                                       bas, bas,  bas,  bas, gtu,
                                         bas,              gtu,
                                           bas,   bas,   bas     ]
    univs['Assembly (3.1\%) 15BANE' + comment] = \
        make_assembly('Assembly (3.1\%) 15BANE' + comment, universes)

    # WITH 15 BURNABLE ABSORBERS SW
    universes = np.empty((17,17), dtype=openmc.Universe)
    universes[:,:] = univs['Fuel (3.1\%) stack']
    universes[nonfuel_y, nonfuel_x] = [    bas,   bas,   bas,
                                         gtu,              bas,
                                       gtu, bas,  bas,  bas, bas,
                                       gtu, bas,  cent, bas, bas,
                                       gtu, bas,  bas,  bas, bas,
                                         gtu,              gtu,
                                           gtu,   gtu,   gtu     ]
    univs['Assembly (3.1\%) 15BASW' + comment] = \
        make_assembly('Assembly (3.1\%) 15BASW' + comment, universes)

    # WITH 15 BURNABLE ABSORBERS SE
    universes = np.empty((17,17), dtype=openmc.Universe)
    universes[:,:] = univs['Fuel (3.1\%) stack']
    universes[nonfuel_y, nonfuel_x] = [    bas,   bas,   bas,
                                         bas,              gtu,
                                       bas, bas,  bas,  bas, gtu,
                                       bas, bas,  cent, bas, gtu,
                                       bas, bas,  bas,  bas, gtu,
                                         gtu,              gtu,
                                           gtu,   gtu,   gtu     ]
    univs['Assembly (3.1\%) 15BASE' + comment] = \
        make_assembly('Assembly (3.1\%) 15BASE' + comment, universes)

    # WITH 6 BURNABLE ABSORBERS N
    universes = np.empty((17,17), dtype=openmc.Universe)
    universes[:,:] = univs['Fuel (3.1\%) stack']
    universes[nonfuel_y, nonfuel_x] = [    gtu,   gtu,   gtu,
                                         gtu,              gtu,
                                       gtu, gtu,  gtu,  gtu, gtu,
                                       gtu, gtu,  cent, gtu, gtu,
                                       bas, gtu,  gtu,  gtu, bas,
                                         bas,              bas,
                                           bas,   gtu,   bas     ]
    univs['Assembly (3.1\%) 6BAN' + comment] = \
        make_assembly('Assembly (3.1\%) 6BAN' + comment, universes)

    # WITH 6 BURNABLE ABSORBERS S
    universes = np.empty((17,17), dtype=openmc.Universe)
    universes[:,:] = univs['Fuel (3.1\%) stack']
    universes[nonfuel_y, nonfuel_x] = [    bas,   gtu,   bas,
                                         bas,              bas,
                                       bas, gtu,  gtu,  gtu, bas,
                                       gtu, gtu,  cent, gtu, gtu,
                                       gtu, gtu,  gtu,  gtu, gtu,
                                         gtu,              gtu,
                                           gtu,   gtu,   gtu     ]
    univs['Assembly (3.1\%) 6BAS' + comment] = \
        make_assembly('Assembly (3.1\%) 6BAS' + comment, universes)

    # WITH 6 BURNABLE ABSORBERS W
    universes = np.empty((17,17), dtype=openmc.Universe)
    universes[:,:] = univs['Fuel (3.1\%) stack']
    universes[nonfuel_y, nonfuel_x] = [    gtu,   gtu,   bas,
                                         gtu,              bas,
                                       gtu, gtu,  gtu,  gtu, bas,
                                       gtu, gtu,  cent, gtu, gtu,
                                       gtu, gtu,  gtu,  gtu, bas,
                                         gtu,              bas,
                                           gtu,   gtu,   bas     ]
    univs['Assembly (3.1\%) 6BAW' + comment] = \
        make_assembly('Assembly (3.1\%) 6BAW' + comment, universes)

    # WITH 6 BURNABLE ABSORBERS E
    universes = np.empty((17,17), dtype=openmc.Universe)
    universes[:,:] = univs['Fuel (3.1\%) stack']
    universes[nonfuel_y, nonfuel_x] = [    bas,   gtu,   gtu,
                                         bas,              gtu,
                                       bas, gtu,  gtu,  gtu, gtu,
                                       gtu, gtu,  cent, gtu, gtu,
                                       bas, gtu,  gtu,  gtu, gtu,
                                         bas,              gtu,
                                           bas,   gtu,   gtu     ]
    univs['Assembly (3.1\%) 6BAE' + comment] = \
        make_assembly('Assembly (3.1\%) 6BAE' + comment, universes)