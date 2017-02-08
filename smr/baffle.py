import openmc

from materials import mats
from surfaces import surfs, lattice_pitch
from assemblies import univs


# NORTH BAFFLE

univs['baffle north dummy'] = openmc.Universe(name='baffle north dummy')

cell = openmc.Cell(name='baffle dummy SS')
cell.fill = mats['SS']
cell.region = +surfs['baffle north']
univs['baffle north dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle north water')
cell.fill = mats['H2O']
cell.region = -surfs['baffle north']
univs['baffle north dummy'].add_cell(cell)

lattice = openmc.RectLattice(name='baffle north')
lattice.lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
lattice.pitch = [lattice_pitch/2., lattice_pitch/2.]
lattice.universes = [
    [univs['baffle north dummy'], univs['baffle north dummy']],
    [univs['water pin'],          univs['water pin']]]

univs['baffle north'] = openmc.Universe(name='baffle north')

cell = openmc.Cell(name='baffle north')
cell.fill = lattice
univs['baffle north'].add_cell(cell)


# SOUTH BAFFLE

univs['baffle south dummy'] = openmc.Universe(name='baffle south dummy')

cell = openmc.Cell(name='baffle dummy SS')
cell.fill = mats['H2O']
cell.region = +surfs['baffle south']
univs['baffle south dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle south water')
cell.fill = mats['SS']
cell.region = -surfs['baffle south']
univs['baffle south dummy'].add_cell(cell)

lattice = openmc.RectLattice(name='baffle south')
lattice.lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
lattice.pitch = [lattice_pitch/2., lattice_pitch/2.]
lattice.universes = [
    [univs['water pin'],          univs['water pin']],
    [univs['baffle south dummy'], univs['baffle south dummy']]]

univs['baffle south'] = openmc.Universe(name='baffle south')

cell = openmc.Cell(name='baffle south')
cell.fill = lattice
univs['baffle south'].add_cell(cell)


# EAST BAFFLE

univs['baffle east dummy'] = openmc.Universe(name='baffle east dummy')

cell = openmc.Cell(name='baffle dummy SS')
cell.fill = mats['SS']
cell.region = +surfs['baffle east']
univs['baffle east dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle east water')
cell.fill = mats['H2O']
cell.region = -surfs['baffle east']
univs['baffle east dummy'].add_cell(cell)

lattice = openmc.RectLattice(name='baffle east')
lattice.lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
lattice.pitch = [lattice_pitch/2., lattice_pitch/2.]
lattice.universes = [
    [univs['water pin'], univs['baffle east dummy']],
    [univs['water pin'], univs['baffle east dummy']]]

univs['baffle east'] = openmc.Universe(name='baffle east')

cell = openmc.Cell(name='baffle east')
cell.fill = lattice
univs['baffle east'].add_cell(cell)


# WEST BAFFLE

univs['baffle west dummy'] = openmc.Universe(name='baffle west dummy')

cell = openmc.Cell(name='baffle dummy SS')
cell.fill = mats['H2O']
cell.region = +surfs['baffle west']
univs['baffle west dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle west water')
cell.fill = mats['SS']
cell.region = -surfs['baffle west']
univs['baffle west dummy'].add_cell(cell)

lattice = openmc.RectLattice(name='baffle west')
lattice.lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
lattice.pitch = [lattice_pitch/2., lattice_pitch/2.]
lattice.universes = [
    [univs['baffle west dummy'], univs['water pin']],
    [univs['baffle west dummy'], univs['water pin']]]

univs['baffle west'] = openmc.Universe(name='baffle west')

cell = openmc.Cell(name='baffle west')
cell.fill = lattice
univs['baffle west'].add_cell(cell)


# NORTHWEST BAFFLE

univs['baffle northwest dummy'] = openmc.Universe(name='baffle northwest dummy')

cell = openmc.Cell(name='baffle northwest dummy 1')
cell.fill = mats['H2O']
cell.region = +surfs['baffle west'] & -surfs['baffle north']
univs['baffle northwest dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle northwest dummy 2')
cell.fill = mats['SS']
cell.region = +surfs['baffle west'] & +surfs['baffle north']
univs['baffle northwest dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle northwest dummy 3')
cell.fill = mats['SS']
cell.region = -surfs['baffle west']
univs['baffle northwest dummy'].add_cell(cell)

lattice = openmc.RectLattice(name='baffle northwest')
lattice.lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
lattice.pitch = [lattice_pitch/2., lattice_pitch/2.]
lattice.universes = [
    [univs['baffle northwest dummy'], univs['baffle north dummy']],
    [univs['baffle west dummy'],      univs['water pin']]]

univs['baffle northwest'] = openmc.Universe(name='baffle northwest')

cell = openmc.Cell(name='baffle northwest')
cell.fill = lattice
univs['baffle northwest'].add_cell(cell)


# NORTHEAST BAFFLE

univs['baffle northeast dummy'] = openmc.Universe(name='baffle northeast dummy')

cell = openmc.Cell(name='baffle northeast dummy 1')
cell.fill = mats['H2O']
cell.region = -surfs['baffle north'] & -surfs['baffle east']
univs['baffle northeast dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle northeast dummy 2')
cell.fill = mats['SS']
cell.region = +surfs['baffle north'] & -surfs['baffle east']
univs['baffle northeast dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle northeast dummy 3')
cell.fill = mats['SS']
cell.region = +surfs['baffle east']
univs['baffle northeast dummy'].add_cell(cell)

lattice = openmc.RectLattice(name='baffle northeast')
lattice.lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
lattice.pitch = [lattice_pitch/2., lattice_pitch/2.]
lattice.universes = [
    [univs['baffle north dummy'], univs['baffle northeast dummy']],
    [univs['water pin'],          univs['baffle east dummy']]]

univs['baffle northeast'] = openmc.Universe(name='baffle northeast')

cell = openmc.Cell(name='baffle northeast')
cell.fill = lattice
univs['baffle northeast'].add_cell(cell)


# SOUTHWEST BAFFLE

univs['baffle southwest dummy'] = openmc.Universe(name='baffle southwest dummy')

cell = openmc.Cell(name='baffle southwest dummy 1')
cell.fill = mats['H2O']
cell.region = +surfs['baffle south'] & +surfs['baffle west']
univs['baffle southwest dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle southwest dummy 2')
cell.fill = mats['SS']
cell.region = -surfs['baffle south'] & +surfs['baffle west']
univs['baffle southwest dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle southwest dummy 3')
cell.fill = mats['SS']
cell.region = -surfs['baffle west']
univs['baffle southwest dummy'].add_cell(cell)

lattice = openmc.RectLattice(name='baffle southwest')
lattice.lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
lattice.pitch = [lattice_pitch/2., lattice_pitch/2.]
lattice.universes = [
    [univs['baffle west dummy'],      univs['water pin']],
    [univs['baffle southwest dummy'], univs['baffle south dummy']]]

univs['baffle southwest'] = openmc.Universe(name='baffle southwest')

cell = openmc.Cell(name='baffle southwest')
cell.fill = lattice
univs['baffle southwest'].add_cell(cell)


# SOUTHEAST BAFFLE

univs['baffle southeast dummy'] = openmc.Universe(name='baffle southeast dummy')

cell = openmc.Cell(name='baffle southeast dummy 1')
cell.fill = mats['H2O']
cell.region = +surfs['baffle south'] & -surfs['baffle east']
univs['baffle southeast dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle southeast dummy 2')
cell.fill = mats['SS']
cell.region = -surfs['baffle south'] & -surfs['baffle east']
univs['baffle southeast dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle southeast dummy 3')
cell.fill = mats['SS']
cell.region = +surfs['baffle east']
univs['baffle southeast dummy'].add_cell(cell)

lattice = openmc.RectLattice(name='baffle southeast')
lattice.lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
lattice.pitch = [lattice_pitch/2., lattice_pitch/2.]
lattice.universes = [
    [univs['water pin'],          univs['baffle east dummy']],
    [univs['baffle south dummy'], univs['baffle southeast dummy']]]

univs['baffle southeast'] = openmc.Universe(name='baffle southeast')

cell = openmc.Cell(name='baffle southeast')
cell.fill = lattice
univs['baffle southeast'].add_cell(cell)


# NORTHWEST CORNER BAFFLE

univs['baffle northwest corner dummy'] = \
    openmc.Universe(name='baffle northwest corner dummy')

cell = openmc.Cell(name='baffle northwest corner dummy 1')
cell.fill = mats['H2O']
cell.region = -surfs['baffle west'] & -surfs['baffle north']
univs['baffle northwest corner dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle northwest corner dummy 2')
cell.fill = mats['H2O']
cell.region = +surfs['baffle west']
univs['baffle northwest corner dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle northwest corner dummy 3')
cell.fill = mats['SS']
cell.region = +surfs['baffle north'] & -surfs['baffle west']
univs['baffle northwest corner dummy'].add_cell(cell)

lattice = openmc.RectLattice(name='baffle northwest corner')
lattice.lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
lattice.pitch = [lattice_pitch/2., lattice_pitch/2.]
lattice.universes = [
    [univs['baffle northwest corner dummy'], univs['water pin']],
    [univs['water pin'],                     univs['water pin']]]

univs['baffle northwest corner'] = \
    openmc.Universe(name='baffle northwest corner')

cell = openmc.Cell(name='baffle northwest corner')
cell.fill = lattice
univs['baffle northwest corner'].add_cell(cell)


# NORTHEAST CORNER BAFFLE

univs['baffle northeast corner dummy'] = \
    openmc.Universe(name='baffle northeast corner dummy')

cell = openmc.Cell(name='baffle northeast corner dummy 1')
cell.fill = mats['H2O']
cell.region = +surfs['baffle east'] & -surfs['baffle north']
univs['baffle northeast corner dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle northeast corner dummy 2')
cell.fill = mats['H2O']
cell.region = -surfs['baffle east']
univs['baffle northeast corner dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle northeast corner dummy 3')
cell.fill = mats['SS']
cell.region = +surfs['baffle north'] & +surfs['baffle east']
univs['baffle northeast corner dummy'].add_cell(cell)

lattice = openmc.RectLattice(name='baffle northeast corner')
lattice.lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
lattice.pitch = [lattice_pitch/2., lattice_pitch/2.]
lattice.universes = [
    [univs['water pin'], univs['baffle northeast corner dummy']],
    [univs['water pin'], univs['water pin']]]

univs['baffle northeast corner'] = \
    openmc.Universe(name='baffle northeast corner')

cell = openmc.Cell(name='baffle northeast corner')
cell.fill = lattice
univs['baffle northeast corner'].add_cell(cell)


# SOUTHEAST CORNER BAFFLE

univs['baffle southeast corner dummy'] = \
    openmc.Universe(name='baffle southeast corner dummy')

cell = openmc.Cell(name='baffle southeast corner dummy 1')
cell.fill = mats['H2O']
cell.region = +surfs['baffle east'] & +surfs['baffle south']
univs['baffle southeast corner dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle southeast corner dummy 2')
cell.fill = mats['H2O']
cell.region = -surfs['baffle east']
univs['baffle southeast corner dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle southeast corner dummy 3')
cell.fill = mats['SS']
cell.region = -surfs['baffle south'] & +surfs['baffle east']
univs['baffle southeast corner dummy'].add_cell(cell)

lattice = openmc.RectLattice(name='baffle southeast corner')
lattice.lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
lattice.pitch = [lattice_pitch/2., lattice_pitch/2.]
lattice.universes = [
    [univs['water pin'], univs['water pin']],
    [univs['water pin'], univs['baffle southeast corner dummy']]]

univs['baffle southeast corner'] = \
    openmc.Universe(name='baffle southeast corner')

cell = openmc.Cell(name='baffle southeast corner')
cell.fill = lattice
univs['baffle southeast corner'].add_cell(cell)


# SOUTHWEST CORNER BAFFLE

univs['baffle southwest corner dummy'] = \
    openmc.Universe(name='baffle southwest corner dummy')

cell = openmc.Cell(name='baffle southwest corner dummy 1')
cell.fill = mats['H2O']
cell.region = -surfs['baffle west'] & +surfs['baffle south']
univs['baffle southwest corner dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle southwest corner dummy 2')
cell.fill = mats['H2O']
cell.region = +surfs['baffle west']
univs['baffle southwest corner dummy'].add_cell(cell)

cell = openmc.Cell(name='baffle southwest corner dummy 3')
cell.fill = mats['SS']
cell.region = -surfs['baffle south'] & -surfs['baffle west']
univs['baffle southwest corner dummy'].add_cell(cell)

lattice = openmc.RectLattice(name='baffle southwest corner')
lattice.lower_left = [-lattice_pitch/2., -lattice_pitch/2.]
lattice.pitch = [lattice_pitch/2., lattice_pitch/2.]
lattice.universes = [
    [univs['water pin'],                     univs['water pin']],
    [univs['baffle southwest corner dummy'], univs['water pin']]]

univs['baffle southwest corner'] = \
    openmc.Universe(name='baffle southwest corner')

cell = openmc.Cell(name='baffle southwest corner')
cell.fill = lattice
univs['baffle southwest corner'].add_cell(cell)
