import openmc

from materials import mats
from surfaces import surfs
from grids import grids

# FIXME: Put materials in a dictionary

def make_pin(name, surfaces, materials, grid=None):

    universe = openmc.Universe(name=name)

    # Create cell for interior of innermost ZCylinder
    cell_name = name + ' (0)'
    cell = openmc.Cell(name=cell_name)
    cell.fill = materials[0]
    cell.region = -surfaces[0]
    universe.add_cell(cell)

    # Create cells between two ZCylinders
    for i, (mat, surf) in enumerate(zip(materials[1:-1], surfaces[:-1])):
        cell_name = name + '({})'.format(i+1)
        cell = openmc.Cell(name=cell_name)
        cell.material = mat
        cell.region = +surf & -surfaces[i+1]
        universe.add_cell(cell)

    # Create cell for exterior of outermost ZCylinder
    cell_name = name + ' (last)'
    cell = openmc.Cell(name=cell_name)
    cell.material = materials[-1]
    cell.region = +surfaces[-1]
    universe.add_cell(cell)

    # Add spacer grid cells if specified
    if grid:
        inner_grid_name = 'inner {}'.format(grid)
        outer_grid_name = 'outer {}'.format(grid)

        # FIXME: Does this work???
        cells[name + ' (last)'].region += grids[inner_grid_name]
        cells[name + ' (grid)'].region = grids[outer_grid_name]
        universe.add_cell(cells[name + '(grid)'])

    return universe

cells = {}

cells['water pin'] = openmc.Cell(name='water pin 1')
cells['water pin'].fill = mats['H2O']
cells['water pin'].region = -surfs['dummy outer']

water_univ = openmc.Universe(name='Empty water pin cell universe')
water_univ.add_cell(cells['water pin 1'])

# FIXME: Is this a good idea???
univs = {}


# GUIDE TUBE PIN CELLS

univs['GT empty'] = make_pin(
    'GT empty', [surfs['GT IR'], surfs['GT OR']],
    [mats['H2O'], mats['Zr'], mats['H2O']])
univs['GT empty grid (top/bottom)'] = make_pin(
    'GT empty grid (top/bottom)', [surfs['GT IR'], surfs['GT OR']],
    [mats['H2O'], mats['Zr'], mats['H2O']], grid='(top/bottom)')
univs['GT empty grid (intermediate)'] = make_pin(
    'GT empty grid (intermediate)', [surfs['GT IR'], surfs['GT OR']],
    [mats['H2O'], mats['Zr'], mats['H2O']], grid='(intermediate)')
univs['GT empty nozzle'] = make_pin(
    'GT empty nozzle', [surfs['GT IR'], surfs['GT OR']],
    [mats['H2O'], mats['Zr'], mats['H2O']])

univs['GTd empty'] = make_pin(
    'GT empty at dashpot', [surfs['GT dashpot IR'], surfs['GT dashpot OR']],
    [mats['H2O'], mats['Zr'], mats['H2O']])
univs['GTd empty grid (top/bottom)'] = make_pin(
    'GT empty at dashpot grid (top/bottom)',
    [surfs['GT dashpot IR'], surfs['GT dashpot OR']],
    [mats['H2O'], mats['Zr'], mats['H2O']], grid='(top/bottom)')
univs['GTd empty grid (intermediate)'] = make_pin(
    'GT empty at dashpot grid (intermediate)',
    [surfs['GT dashpot IR'], surfs['GT dashpot OR']],
    [mats['H2O'], mats['Zr'], mats['H2O']], grid='(intermediate)')
univs['GTd empty nozzle'] = make_pin(
    'GT empty nozzle', [surfs['GT dashpot IR'], surfs['GT dashpot OR']],
    [mats['H2O'], mats['Zr'], mats['H2O']])

# FIXME: Stack all axial pieces of guide tube together


# INSTRUMENT TUBE PIN CELL

univs['IT'] = make_pin(
    'IT', [surfs['IT IR'], surfs['IT OR'], surfs['GT IR'], surfs['GT OR']],
    [mats['Air'], mats['Zr'], mats['H2O'], mats['Zr'], mats['H2O']])
univs['IT grid (top/bottom)'] = make_pin(
    'IT grid (top/bottom)',
    [surfs['IT IR'], surfs['IT OR'], surfs['GT IR'], surfs['GT OR']],
    [mats['Air'], mats['Zr'], mats['H2O'], mats['Zr'], mats['H2O']],
    grid='top/bottom')
univs['IT grid (intermediate)'] = make_pin(
    'IT grid (intermediate)',
    [surfs['IT IR'], surfs['IT OR'], surfs['GT IR'], surfs['GT OR']],
    [mats['Air'], mats['Zr'], mats['H2O'], mats['Zr'], mats['H2O']],
    grid='intermediate')

univs['IT nozzle'] = make_pin(
    'IT nozzle',
    [surfs['IT IR'], surfs['IT OR'], surfs['GT IR'], surfs['GT OR']],
    [mats['Air'], mats['Zr'], mats['H2O'], mats['Zr'], mats['SS']])
univs['IT dashpot'] = make_pin(
    'IT dashpot', [surfs['IT IR'], surfs['IT OR']],
    [mats['Air'], mats['Zr'], mats['H2O']])


# CONTROL ROD PIN CELLS

univs['CR'] = make_pin(
    'CR', [surfs['CP OR'], surfs['CR IR'], surfs['GT IR'], surfs['GT OR']],
    [mats['AIC'], mats['Air'], mats['SS'], mats['H2O'], mats['Zr'], mats['H2O']])
univs['CR grid (top/bottom)'] = make_pin(
    'CR grid (top/bottom)', [surfs['CP OR'], surfs['CR IR'], surfs['GT IR'], surfs['GT OR']],
    [mats['AIC'], mats['Air'], mats['SS'], mats['H2O'], mats['Zr'], mats['H2O']],
    grid='(top/bottom)')
univs['CR grid (intermediate)'] = make_pin(
    'CR grid (intermediate)',
    [surfs['CP OR'], surfs['CR IR'], surfs['GT IR'], surfs['GT OR']],
    [mats['AIC'], mats['Air'], mats['SS'], mats['H2O'], mats['Zr'], mats['H2O']],
    grid='(intermediate)')
univs['CR nozzle'] = make_pin(
    'CR nozzle', [surfs['CP OR'], surfs['CR IR'], surfs['CR OR']],
    [mats['AIC'], mats['Air'], mats['SS'], mats['H2O']])

univs['CR blank'] = make_pin(
    'CR blank',
    [surfs['CP OR'], surfs['CR IR'], surfs['CR OR'], surfs['GT IR'], surfs['GT OR']],
    [mats['SS'], mats['Air'], mats['SS'], mats['H2O'], mats['Zr'], mats['H2O']])
univs['CR blank grid (top/bottom)'] = make_pin(
    'CR blank grid (top/bottom)',
    [surfs['CP OR'], surfs['CR IR'], surfs['CR OR'], surfs['GT IR'], surfs['GT OR']],
    [mats['SS'], mats['Air'], mats['SS'], mats['H2O'], mats['Zr'], mats['H2O']],
    grid='top/bottom')
univs['CR blank grid (intermediate)'] = make_pin(
    'CR blank grid (intermediate)',
    [surfs['CP OR'], surfs['CR IR'], surfs['CR OR'], surfs['GT IR'], surfs['GT OR']],
    [mats['SS'], mats['Air'], mats['SS'], mats['H2O'], mats['Zr'], mats['H2O']],
    grid='intermediate')
univs['CR blank nozzle'] = make_pin(
    'CR blank nozzle', [surfs['CP OR'], surfs['CR IR'], surfs['CR OR']],
    [mats['SS'], mats['Air'], mats['SS'], mats['H2O']])
univs['CR blank bare'] = make_pin(
    'CR blank bare', [surfs['CP OR'], surfs['CR IR'], surfs['CR OR']],
    [mats['SS'], mats['Air'], mats['SS'], mats['H2O']])
univs['CR bare'] = make_pin(
    'CR bare', [surfs['CP OR'], surfs['CR IR'], surfs['CR OR']],
    [mats['AIC'], mats['Air'], mats['SS'], mats['H2O']])
