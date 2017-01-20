from materials import *
from surfaces import surfs
from grids import grids

import openmc

# FIXME: Put materials in a dictionary

cells = {}

cells['water pin'] = openmc.Cell(name='water pin 1')
cells['water pin'].fill = mat_h2o
cells['water pin'].region = -surfs['dummy outer']

water_univ = openmc.Universe(name='Empty water pin cell universe')
water_univ.add_cell(cells['water pin 1'])



def make_pin(name, section, cells, surfaces, materials, grid=None):

    universe = openmc.Universe(name=name)

    # Create cell for interior of innermost ZCylinder
    cell_name = name + ' (0)'
    cells[cell_name] = openmc.Cell(name=cell_name)
    cells[cell_name].fill = materials[0]
    cells[cell_name].region = -surfaces[0]
    universe.add_cell(cells[cell_name])

    # Create cells between two ZCylinders
    for i, (mat, surf) in enumerate(zip(materials[1:-1], surfaces[:-1])):
        cell_name = name + '({})'.format(i+1)
        cells[cell_name] = openmc.Cell(name=cell_name)
        cells[cell_name].material = mat
        cells[cell_name].region = +surf & -surfaces[i+1]
        universe.add_cell([cells[cell_name]])

    # Create cell for exterior of outermost ZCylinder
    cell_name = name + ' (last)'
    cells[cell_name] = openmc.Cell(name=cell_name)
    cells[cell_name].material = materials[-1]
    cells[cell_name].region = +surfaces[-1]
    universe.add_cell([cells[cell_name]])

    # Add spacer grid cells if specified
    if grid:
        inner_grid_name = 'inner {}'.format(grid)
        outer_grid_name = 'outer {}'.format(grid)

        # FIXME: Does this work???
        cells[name + ' (last)'].region += grids[inner_grid_name]
        cells[name + ' (grid)'].region = grids[outer_grid_name]
        universe.add_cell(cells[name + '(grid)'])