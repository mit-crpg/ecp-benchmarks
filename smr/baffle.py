import openmc

from materials import mats
from surfaces import surfs, lattice_pitch
from assemblies import univs


# FIXME: is this necessary??
latts = {}

# NORTH BAFFLE

univs['baffle north dummy'] = openmc.Universe(name='baffle north dummy')

cell = openmc.Cell(name='baffle dummy SS')
cell.material = mats['SS']
cell.region = +surfs['baffle north']
univs['baffle north dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle north water')
cell.material = mats['H2O']
cell.region = -surfs['baffle north']
univs['baffle north dummy'].add_cell(cell)

# FIXME: Is this necessary? Or can we simply fill the lattice with this universe???
latts['baffle north'] = openmc.RectLattice(name='baffle north')
latts['baffle north'].lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
latts['baffle north'].pitch = [lattice_pitch/2., lattice_pitch/2.]
latts['baffle north'].universes = [
    [univs['baffle north dummy'], univs['baffle north dummy']],
    [univs['water pin'],          univs['water pin']]]

univs['baffle north'] = openmc.Universe(name='baffle north')

cell = openmc.Cell(name='baffle north')
cell.fill = latts['baffle north']
cell.region = -surfs['dummy outer']
univs['baffle north'].add_cell(cell)


# SOUTH BAFFLE

univs['baffle south dummy'] = openmc.Universe(name='baffle south dummy')

cell = openmc.Cell(name='baffle dummy SS')
cell.material = mats['H2O']
cell.region = +surfs['baffle south']
univs['baffle south dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle south water')
cell.material = mats['SS']
cell.region = -surfs['baffle south']
univs['baffle south dummy'].add_cell(cell)

# FIXME: Is this necessary? Or can we simply fill the lattice with this universe???
latts['baffle south'] = openmc.RectLattice(name='baffle south')
latts['baffle south'].lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
latts['baffle south'].pitch = [lattice_pitch/2., lattice_pitch/2.]
latts['baffle south'].universes = [
    [univs['water pin'],          univs['water pin']],
    [univs['baffle south dummy'], univs['baffle south dummy']]]

univs['baffle south'] = openmc.Universe(name='baffle south')

cell = openmc.Cell(name='baffle south')
cell.fill = latts['baffle south']
cell.region = -surfs['dummy outer']
univs['baffle south'].add_cell(cell)


# EAST BAFFLE

univs['baffle east dummy'] = openmc.Universe(name='baffle east dummy')

cell = openmc.Cell(name='baffle dummy SS')
cell.material = mats['SS']
cell.region = +surfs['baffle east']
univs['baffle east dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle east water')
cell.material = mats['H2O']
cell.region = -surfs['baffle east']
univs['baffle east dummy'].add_cell(cell)

# FIXME: Is this necessary? Or can we simply fill the lattice with this universe???
latts['baffle east'] = openmc.RectLattice(name='baffle east')
latts['baffle east'].lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
latts['baffle east'].pitch = [lattice_pitch/2., lattice_pitch/2.]
latts['baffle east'].universes = [
    [univs['water pin'], univs['baffle east dummy']],
    [univs['water pin'], univs['baffle east dummy']]]

univs['baffle east'] = openmc.Universe(name='baffle east')

cell = openmc.Cell(name='baffle east')
cell.fill = latts['baffle east']
cell.region = -surfs['dummy outer']
univs['baffle east'].add_cell(cell)


# WEST BAFFLE

univs['baffle west dummy'] = openmc.Universe(name='baffle west dummy')

cell = openmc.Cell(name='baffle dummy SS')
cell.material = mats['H2O']
cell.region = +surfs['baffle west']
univs['baffle west dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle west water')
cell.material = mats['SS']
cell.region = -surfs['baffle west']
univs['baffle west dummy'].add_cell(cell)

# FIXME: Is this necessary? Or can we simply fill the lattice with this universe???
latts['baffle west'] = openmc.RectLattice(name='baffle west')
latts['baffle west'].lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
latts['baffle west'].pitch = [lattice_pitch/2., lattice_pitch/2.]
latts['baffle west'].universes = [
    [univs['baffle west dummy'], univs['water pin']],
    [univs['baffle west dummy'], univs['water pin']]]

univs['baffle west'] = openmc.Universe(name='baffle west')

cell = openmc.Cell(name='baffle west')
cell.fill = latts['baffle west']
cell.region = -surfs['dummy outer']
univs['baffle west'].add_cell(cell)


# NORTHWEST BAFFLE

univs['baffle northwest dummy'] = openmc.Universe(name='baffle northwest dummy')

cell = openmc.Cell(name='baffle northwest dummy 1')
cell.material = mats['H2O']
cell.region = +surfs['baffle west'] & -surfs['baffle north']
univs['baffle northwest dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle northwest dummy 2')
cell.material = mats['SS']
cell.region = +surfs['baffle west'] & +surfs['baffle north']
univs['baffle northwest dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle northwest dummy 3')
cell.material = mats['SS']
cell.region = -surfs['baffle west']
univs['baffle northwest dummy'].add_cell(cell)

# FIXME: Is this necessary? Or can we simply fill the lattice with this universe???
latts['baffle northwest'] = openmc.RectLattice(name='baffle northwest')
latts['baffle northwest'].lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
latts['baffle northwest'].pitch = [lattice_pitch/2., lattice_pitch/2.]
latts['baffle northwest'].universes = [
    [univs['baffle northwest dummy'], univs['baffle north dummy']],
    [univs['baffle west dummy'],      univs['water pin']]]

univs['baffle northwest'] = openmc.Universe(name='baffle northwest')

cell = openmc.Cell(name='baffle northwest')
cell.fill = latts['baffle northwest']
cell.region = -surfs['dummy outer']
univs['baffle northwest'].add_cell(cell)


# NORTHEAST BAFFLE

univs['baffle northeast dummy'] = openmc.Universe(name='baffle northeast dummy')

cell = openmc.Cell(name='baffle northeast dummy 1')
cell.material = mats['H2O']
cell.region = -surfs['baffle north'] & -surfs['baffle east']
univs['baffle northeast dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle northeast dummy 2')
cell.material = mats['SS']
cell.region = +surfs['baffle north'] & -surfs['baffle east']
univs['baffle northeast dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle northeast dummy 3')
cell.material = mats['SS']
cell.region = +surfs['baffle east']
univs['baffle northeast dummy'].add_cell(cell)

# FIXME: Is this necessary? Or can we simply fill the lattice with this universe???
latts['baffle northeast'] = openmc.RectLattice(name='baffle northeast')
latts['baffle northeast'].lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
latts['baffle northeast'].pitch = [lattice_pitch/2., lattice_pitch/2.]
latts['baffle northeast'].universes = [
    [univs['baffle north dummy'], univs['baffle northeast dummy']],
    [univs['water pin'],          univs['baffle east']]]

univs['baffle northeast'] = openmc.Universe(name='baffle northeast')

cell = openmc.Cell(name='baffle northeast')
cell.fill = latts['baffle northeast']
cell.region = -surfs['dummy outer']
univs['baffle northeast'].add_cell(cell)


# SOUTHWEST BAFFLE

univs['baffle southwest dummy'] = openmc.Universe(name='baffle southwest dummy')

cell = openmc.Cell(name='baffle southwest dummy 1')
cell.material = mats['H2O']
cell.region = +surfs['baffle south'] & +surfs['baffle east']
univs['baffle southwest dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle southwest dummy 2')
cell.material = mats['SS']
cell.region = -surfs['baffle south'] & +surfs['baffle west']
univs['baffle southwest dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle southwest dummy 3')
cell.material = mats['SS']
cell.region = -surfs['baffle west']
univs['baffle southwest dummy'].add_cell(cell)

# FIXME: Is this necessary? Or can we simply fill the lattice with this universe???
latts['baffle southwest'] = openmc.RectLattice(name='baffle southwest')
latts['baffle southwest'].lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
latts['baffle southwest'].pitch = [lattice_pitch/2., lattice_pitch/2.]
latts['baffle southwest'].universes = [
    [univs['baffle west dummy'],      univs['water pin']],
    [univs['baffle southwest dummy'], univs['baffle south dummy']]]

univs['baffle southwest'] = openmc.Universe(name='baffle southwest')

cell = openmc.Cell(name='baffle southwest')
cell.fill = latts['baffle southwest']
cell.region = -surfs['dummy outer']
univs['baffle southwest'].add_cell(cell)


# SOUTHEAST BAFFLE

univs['baffle southeast dummy'] = openmc.Universe(name='baffle southeast dummy')

cell = openmc.Cell(name='baffle southeast dummy 1')
cell.material = mats['H2O']
cell.region = +surfs['baffle south'] & -surfs['baffle east']
univs['baffle southeast dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle southeast dummy 2')
cell.material = mats['SS']
cell.region = -surfs['baffle south'] & -surfs['baffle east']
univs['baffle southeast dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle southeast dummy 3')
cell.material = mats['SS']
cell.region = +surfs['baffle east']
univs['baffle southeast dummy'].add_cell(cell)

# FIXME: Is this necessary? Or can we simply fill the lattice with this universe???
latts['baffle southeast'] = openmc.RectLattice(name='baffle southeast')
latts['baffle southeast'].lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
latts['baffle southeast'].pitch = [lattice_pitch/2., lattice_pitch/2.]
latts['baffle southeast'].universes = [
    [univs['water pin'],          univs['baffle east dummy']],
    [univs['baffle south dummy'], univs['baffle southeast dummy']]]

univs['baffle southeast'] = openmc.Universe(name='baffle southeast')

cell = openmc.Cell(name='baffle southeast')
cell.fill = latts['baffle southeast']
cell.region = -surfs['dummy outer']
univs['baffle southeast'].add_cell(cell)


# NORTHWEST CORNER BAFFLE

univs['baffle northwest corner dummy'] = \
    openmc.Universe(name='baffle northwest corner dummy')

cell = openmc.Cell(name='baffle northwest corner dummy 1')
cell.material = mats['H2O']
cell.region = -surfs['baffle west'] & -surfs['baffle north']
univs['baffle northwest corner dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle northwest corner dummy 2')
cell.material = mats['H2O']
cell.region = +surfs['baffle west']
univs['baffle northwest corner dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle northwest corner dummy 3')
cell.material = mats['SS']
cell.region = +surfs['baffle north'] & -surfs['baffle west']
univs['baffle northwest corner dummy'].add_cell(cell)

# FIXME: Is this necessary? Or can we simply fill the lattice with this universe???
latts['baffle northwest corner'] = openmc.RectLattice(name='baffle northwest corner')
latts['baffle northwest corner'].lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
latts['baffle northwest corner'].pitch = [lattice_pitch/2., lattice_pitch/2.]
latts['baffle northwest corner'].universes = [
    [univs['baffle northwest corner dummy'], univs['water pin']],
    [univs['water pin'],                     univs['water pin']]]

univs['baffle northwest corner'] = \
    openmc.Universe(name='baffle northwest corner')

cell = openmc.Cell(name='baffle northwest corner')
cell.fill = latts['baffle northwest corner']
cell.region = -surfs['dummy outer']
univs['baffle northwest corner'].add_cell(cell)


# NORTHEAST CORNER BAFFLE

univs['baffle northeast corner dummy'] = \
    openmc.Universe(name='baffle northeast corner dummy')

cell = openmc.Cell(name='baffle northeast corner dummy 1')
cell.material = mats['H2O']
cell.region = +surfs['baffle east'] & -surfs['baffle north']
univs['baffle northeast corner dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle northeast corner dummy 2')
cell.material = mats['H2O']
cell.region = -surfs['baffle east']
univs['baffle northeast corner dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle northeast corner dummy 3')
cell.material = mats['SS']
cell.region = +surfs['baffle north'] & -surfs['baffle east']
univs['baffle northeast corner dummy'].add_cell(cell)

# FIXME: Is this necessary? Or can we simply fill the lattice with this universe???
latts['baffle northeast corner'] = openmc.RectLattice(name='baffle northeast corner')
latts['baffle northeast corner'].lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
latts['baffle northeast corner'].pitch = [lattice_pitch/2., lattice_pitch/2.]
latts['baffle northeast corner'].universes = [
    [univs['water pin'], univs['baffle northeast corner dummy']],
    [univs['water pin'], univs['water pin']]]

univs['baffle northeast corner'] = \
    openmc.Universe(name='baffle northeast corner')

cell = openmc.Cell(name='baffle northeast corner')
cell.fill = latts['baffle northeast corner']
cell.region = -surfs['dummy outer']
univs['baffle northeast corner'].add_cell(cell)


# SOUTHEAST CORNER BAFFLE

univs['baffle southeast corner dummy'] = \
    openmc.Universe(name='baffle southeast corner dummy')

cell = openmc.Cell(name='baffle southeast corner dummy 1')
cell.material = mats['H2O']
cell.region = +surfs['baffle east'] & +surfs['baffle south']
univs['baffle southeast corner dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle southeast corner dummy 2')
cell.material = mats['H2O']
cell.region = -surfs['baffle east']
univs['baffle southeast corner dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle southeast corner dummy 3')
cell.material = mats['SS']
cell.region = -surfs['baffle south'] & +surfs['baffle east']
univs['baffle southeast corner dummy'].add_cell(cell)

# FIXME: Is this necessary? Or can we simply fill the lattice with this universe???
latts['baffle southeast corner'] = openmc.RectLattice(name='baffle southeast corner')
latts['baffle southeast corner'].lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
latts['baffle southeast corner'].pitch = [lattice_pitch/2., lattice_pitch/2.]
latts['baffle southeast corner'].universes = [
    [univs['water pin'], univs['water pin']],
    [univs['water pin'], univs['baffle southeast corner dummy']]]

univs['baffle southeast corner'] = \
    openmc.Universe(name='baffle southeast corner')

cell = openmc.Cell(name='baffle southeast corner')
cell.fill = latts['baffle southeast corner']
cell.region = -surfs['dummy outer']
univs['baffle southeast corner'].add_cell(cell)


# SOUTHWEST CORNER BAFFLE

univs['baffle southwest corner dummy'] = \
    openmc.Universe(name='baffle southwest corner dummy')

cell = openmc.Cell(name='baffle southwest corner dummy 1')
cell.material = mats['H2O']
cell.region = -surfs['baffle west'] & +surfs['baffle south']
univs['baffle southwest corner dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle southwest corner dummy 2')
cell.material = mats['H2O']
cell.region = +surfs['baffle west']
univs['baffle southwest corner dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle southwest corner dummy 3')
cell.material = mats['SS']
cell.region = -surfs['baffle south'] & -surfs['baffle west']
univs['baffle southwest corner dummy'].add_cell(cell)

# FIXME: Is this necessary? Or can we simply fill the lattice with this universe???
latts['baffle southwest corner'] = openmc.RectLattice(name='baffle southwest corner')
latts['baffle southwest corner'].lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
latts['baffle southwest corner'].pitch = [lattice_pitch/2., lattice_pitch/2.]
latts['baffle southwest corner'].universes = [
    [univs['water pin'],                     univs['water pin']],
    [univs['baffle southwest corner dummy'], univs['water pin']]]

univs['baffle southwest corner'] = \
    openmc.Universe(name='baffle southwest corner')

cell = openmc.Cell(name='baffle southwest corner')
cell.fill = latts['baffle southwest corner']
cell.region = -surfs['dummy outer']
univs['baffle southwest corner'].add_cell(cell)
