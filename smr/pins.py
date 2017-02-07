import openmc

from materials import mats
from surfaces import surfs
from grids import grids

# FIXME: Add docstrings, etc.
# FIXME: Assign names of cells, universes based on dict keys

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
        cell_name = name + ' ({})'.format(i+1)
        cell = openmc.Cell(name=cell_name)
        cell.fill = mat
        cell.region = +surf & -surfaces[i+1]
        universe.add_cell(cell)

    # Create cell for exterior of outermost ZCylinder
    cell_name = name + ' (last)'
    cell = openmc.Cell(name=cell_name)
    cell.fill = materials[-1]
    cell.region = +surfaces[-1]
    universe.add_cell(cell)

    # Add spacer grid cells if specified
    if grid:
        inner_grid_name = 'inner grid box {}'.format(grid)

        # FIXME: Does this work???
        cell.region = openmc.Intersection(cell.region, grids[inner_grid_name])

        cell_name = name + ' (grid)'
        cell = openmc.Cell(name=cell_name)
        cell.region = openmc.Complement(grids[inner_grid_name])

        if grid == 'top/bottom':
            cell.fill = mats['In']
        else:
            cell.fill = mats['Zr']

        universe.add_cell(cell)

    return universe


def make_stack(name, surfaces, universes):

    universe = openmc.Universe(name=name)

    # Create cell for interior of innermost ZCylinder
    cell_name = name + ' (0)'
    cell = openmc.Cell(name=cell_name)
    cell.fill = universes[0]
    cell.region = -surfaces[0]
    universe.add_cell(cell)

    # Create cells between two ZCylinders
    for i, (univ, surf) in enumerate(zip(universes[1:-1], surfaces[:-1])):
        cell_name = name + ' ({})'.format(i+1)
        cell = openmc.Cell(name=cell_name)
        cell.fill = univ
        cell.region = +surf & -surfaces[i+1]
        universe.add_cell(cell)

    # Create cell for exterior of outermost ZCylinder
    cell_name = name + ' (last)'
    cell = openmc.Cell(name=cell_name)
    cell.fill = universes[-1]
    cell.region = +surfaces[-1]
    universe.add_cell(cell)

    return universe


# FIXME: Is this a good idea???
univs = {}

cell = openmc.Cell(name='water pin 1')
cell.fill = mats['H2O']
cell.region = -surfs['dummy outer']
univs['water pin'] = openmc.Universe(name='Empty water pin cell universe')
univs['water pin'].add_cell(cell)

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

# Stack all axial pieces of guide tube together

stack_surfs = [
    surfs['bot support plate'],
    surfs['top support plate'],
    surfs['top lower nozzle'],
    surfs['top lower thimble'],
    surfs['grid1bot'],
    surfs['grid1top'],
    surfs['dashpot top'],
    surfs['grid2bot'],
    surfs['grid2top'],
    surfs['grid3bot'],
    surfs['grid3top'],
    surfs['grid4bot'],
    surfs['grid4top'],
    surfs['top active core'],
    surfs['top pin plenum'],
    surfs['top FR'],
    surfs['bot upper nozzle'],
    surfs['top upper nozzle']
]

univs['GT empty'] = make_stack(
    'GT empty', surfaces=stack_surfs,
    universes=[univs['water pin'],
               univs['water pin'],
               univs['water pin'],
               univs['GTd empty'],
               univs['GTd empty'],
               univs['GTd empty grid (top/bottom)'],
               univs['GTd empty'],
               univs['GT empty'],
               univs['GT empty grid (intermediate)'],
               univs['GT empty'],
               univs['GT empty grid (intermediate)'],
               univs['GT empty'],
               univs['GT empty'],
               univs['GT empty grid (top/bottom)'],
               univs['GT empty'],
               univs['GT empty'],
               univs['GT empty'],
               univs['water pin'],
               univs['water pin']])

univs['GT empty instr'] = make_stack(
    'GT empty instr', surfaces=stack_surfs,
    universes=[univs['water pin'],
               univs['water pin'],
               univs['water pin'],
               univs['GT empty'],
               univs['GT empty'],
               univs['GT empty grid (top/bottom)'],
               univs['GT empty'],
               univs['GT empty'],
               univs['GT empty grid (intermediate)'],
               univs['GT empty'],
               univs['GT empty grid (intermediate)'],
               univs['GT empty'],
               univs['GT empty'],
               univs['GT empty grid (top/bottom)'],
               univs['GT empty'],
               univs['GT empty'],
               univs['GT empty'],
               univs['water pin'],
               univs['water pin']])


# INSTRUMENT TUBE PIN CELL

univs['IT'] = make_pin(
    'IT', [surfs['IT IR'], surfs['IT OR'], surfs['GT IR'], surfs['GT OR']],
    [mats['Air'], mats['Zr'], mats['H2O'], mats['Zr'], mats['H2O']])
univs['IT grid (top/bottom)'] = make_pin(
    'IT grid (top/bottom)',
    [surfs['IT IR'], surfs['IT OR'], surfs['GT IR'], surfs['GT OR']],
    [mats['Air'], mats['Zr'], mats['H2O'], mats['Zr'], mats['H2O']],
    grid='(top/bottom)')
univs['IT grid (intermediate)'] = make_pin(
    'IT grid (intermediate)',
    [surfs['IT IR'], surfs['IT OR'], surfs['GT IR'], surfs['GT OR']],
    [mats['Air'], mats['Zr'], mats['H2O'], mats['Zr'], mats['H2O']],
    grid='(intermediate)')

univs['IT nozzle'] = make_pin(
    'IT nozzle',
    [surfs['IT IR'], surfs['IT OR'], surfs['GT IR'], surfs['GT OR']],
    [mats['Air'], mats['Zr'], mats['H2O'], mats['Zr'], mats['SS']])
univs['IT dashpot'] = make_pin(
    'IT dashpot', [surfs['IT IR'], surfs['IT OR']],
    [mats['Air'], mats['Zr'], mats['H2O']])

# Stack all axial pieces of instrument tube together

univs['IT stack'] = make_stack(
    'GT instr', surfaces=stack_surfs,
    universes=[univs['IT dashpot'],
               univs['IT dashpot'],
               univs['IT dashpot'],
               univs['IT'],
               univs['IT'],
               univs['IT grid (top/bottom)'],
               univs['IT'],
               univs['IT'],
               univs['IT grid (intermediate)'],
               univs['IT'],
               univs['IT grid (intermediate)'],
               univs['IT'],
               univs['IT'],
               univs['IT grid (top/bottom)'],
               univs['IT'],
               univs['IT'],
               univs['IT'],
               univs['IT dashpot'],
               univs['water pin']])


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
    grid='(top/bottom)')
univs['CR blank grid (intermediate)'] = make_pin(
    'CR blank grid (intermediate)',
    [surfs['CP OR'], surfs['CR IR'], surfs['CR OR'], surfs['GT IR'], surfs['GT OR']],
    [mats['SS'], mats['Air'], mats['SS'], mats['H2O'], mats['Zr'], mats['H2O']],
    grid='(intermediate)')
univs['CR blank nozzle'] = make_pin(
    'CR blank nozzle', [surfs['CP OR'], surfs['CR IR'], surfs['CR OR']],
    [mats['SS'], mats['Air'], mats['SS'], mats['H2O']])
univs['CR blank bare'] = make_pin(
    'CR blank bare', [surfs['CP OR'], surfs['CR IR'], surfs['CR OR']],
    [mats['SS'], mats['Air'], mats['SS'], mats['H2O']])
univs['CR bare'] = make_pin(
    'CR bare', [surfs['CP OR'], surfs['CR IR'], surfs['CR OR']],
    [mats['AIC'], mats['Air'], mats['SS'], mats['H2O']])

# Stack all axial pieces of control rod tubes together for each bank

banks = ['A','B','C','D','SA','SB','SC','SD','SE']

for b in banks:

    # no grid, no nozzle
    univs['GT CR bank {} dummy'.format(b)] = make_stack(
        'GT CR bank {} dummy'.format(b),
        surfaces=[surfs['bottom FR'],
                  surfs['dashpot top'],
                  surfs['bank{} bot'.format(b)],
                  surfs['bank{} top'.format(b)]],
        universes=[univs['water pin'],
                   univs['GTd empty'],
                   univs['GT empty'],
                   univs['CR'],
                   univs['CR blank']])

    # top/bottom grid
    univs['GT CR bank {} dummy grid (top/bottom)'.format(b)] = make_stack(
        'GT CR bank {} dummy grid (top/bottom)'.format(b),
        surfaces=[surfs['bottom FR'],
                  surfs['dashpot top'],
                  surfs['bank{} bot'.format(b)],
                  surfs['bank{} top'.format(b)]],
        universes=[univs['water pin'],
                   univs['GTd empty grid (top/bottom)'],
                   univs['GT empty grid (top/bottom)'],
                   univs['CR grid (top/bottom)'],
                   univs['CR blank grid (top/bottom)']])

    # intermediate grid
    univs['GT CR bank {} dummy grid (intermediate)'.format(b)] = make_stack(
        'GT CR bank {} dummy grid (intermediate)'.format(b),
        surfaces=[surfs['bottom FR'],
                  surfs['dashpot top'],
                  surfs['bank{} bot'.format(b)],
                  surfs['bank{} top'.format(b)]],
        universes=[univs['water pin'],
                   univs['GTd empty grid (intermediate)'],
                   univs['GT empty grid (intermediate)'],
                   univs['CR grid (intermediate)'],
                   univs['CR blank grid (intermediate)']])

    # nozzle
    univs['GT CR bank {} dummy nozzle'.format(b)] = make_stack(
        'GT CR bank {} dummy nozzle'.format(b),
        surfaces=[surfs['bottom FR'],
                  surfs['dashpot top'],
                  surfs['bank{} bot'.format(b)],
                  surfs['bank{} top'.format(b)]],
        universes=[univs['water pin'],
                   univs['GTd empty nozzle'],
                   univs['GT empty nozzle'],
                   univs['CR nozzle'],
                   univs['CR blank nozzle']])

    # bare
    univs['GT CR bank {} dummy bare'.format(b)] = make_stack(
        'GT CR bank {} dummy bare'.format(b),
        surfaces=[surfs['bottom FR'],
                  surfs['dashpot top'],
                  surfs['bank{} bot'.format(b)],
                  surfs['bank{} top'.format(b)]],
        universes=[univs['water pin'],
                   univs['GTd empty nozzle'],
                   univs['GT empty nozzle'],
                   univs['CR bare'],
                   univs['CR blank bare']])

    # final combination of all axial pieces for control rod bank "b"
    univs['GT CR bank {}'.format(b)] = make_stack(
        'GT CR bank {}'.format(b), stack_surfs,
        universes=[univs['water pin'],
                   univs['GT CR bank {} dummy nozzle'.format(b)],
                   univs['GT CR bank {} dummy nozzle'.format(b)],
                   univs['GT CR bank {} dummy'.format(b)],
                   univs['GT CR bank {} dummy'.format(b)],
                   univs['GT CR bank {} dummy grid (top/bottom)'.format(b)],
                   univs['GT CR bank {} dummy'.format(b)],
                   univs['GT CR bank {} dummy'.format(b)],
                   univs['GT CR bank {} dummy grid (intermediate)'.format(b)],
                   univs['GT CR bank {} dummy'.format(b)],
                   univs['GT CR bank {} dummy grid (intermediate)'.format(b)],
                   univs['GT CR bank {} dummy'.format(b)],
                   univs['GT CR bank {} dummy'.format(b)],
                   univs['GT CR bank {} dummy grid (top/bottom)'.format(b)],
                   univs['GT CR bank {} dummy'.format(b)],
                   univs['GT CR bank {} dummy'.format(b)],
                   univs['GT CR bank {} dummy'.format(b)],
                   univs['GT CR bank {} dummy bare'.format(b)],
                   univs['GT CR bank {} dummy bare'.format(b)]])


# BURNABLE ABSORBER PIN CELLS

univs['BA'] = make_pin(
    'BA',
    surfaces=[surfs['BA IR 1'],
              surfs['BA IR 2'],
              surfs['BA IR 3'],
              surfs['BA IR 4'],
              surfs['BA IR 5'],
              surfs['BA IR 6'],
              surfs['BA IR 7'],
              surfs['BA IR 8']],
    materials=[mats['Air'],
               mats['SS'],
               mats['Air'],
               mats['BSG'],
               mats['Air'],
               mats['SS'],
               mats['H2O'],
               mats['Zr'],
               mats['H2O']])

univs['BA grid (top/bottom)'] = make_pin(
    'BA grid (top/bottom)',
    surfaces=[surfs['BA IR 1'],
              surfs['BA IR 2'],
              surfs['BA IR 3'],
              surfs['BA IR 4'],
              surfs['BA IR 5'],
              surfs['BA IR 6'],
              surfs['BA IR 7'],
              surfs['BA IR 8']],
    materials=[mats['Air'],
               mats['SS'],
               mats['Air'],
               mats['BSG'],
               mats['Air'],
               mats['SS'],
               mats['H2O'],
               mats['Zr'],
               mats['H2O']],
    grid='(top/bottom)')

univs['BA grid (intermediate)'] = make_pin(
    'BA grid (intermediate)',
    surfaces=[surfs['BA IR 1'],
              surfs['BA IR 2'],
              surfs['BA IR 3'],
              surfs['BA IR 4'],
              surfs['BA IR 5'],
              surfs['BA IR 6'],
              surfs['BA IR 7'],
              surfs['BA IR 8']],
    materials=[mats['Air'],
               mats['SS'],
               mats['Air'],
               mats['BSG'],
               mats['Air'],
               mats['SS'],
               mats['H2O'],
               mats['Zr'],
               mats['H2O']],
    grid='(intermediate)')

univs['BA dashpot'] = make_pin(
    'BA dashpot',
    surfaces=[surfs['BA IR 1'],
              surfs['BA IR 2'],
              surfs['BA IR 3'],
              surfs['BA IR 4'],
              surfs['BA IR 5'],
              surfs['BA IR 6'],
              surfs['GT dashpot IR'],
              surfs['GT dashpot OR']],
    materials=[mats['Air'],
               mats['SS'],
               mats['Air'],
               mats['BSG'],
               mats['Air'],
               mats['SS'],
               mats['H2O'],
               mats['Zr'],
               mats['H2O']])

univs['BA dashpot grid (top/bottom)'] = make_pin(
    'BA dashpot grid (top/bottom)',
    surfaces=[surfs['BA IR 1'],
              surfs['BA IR 2'],
              surfs['BA IR 3'],
              surfs['BA IR 4'],
              surfs['BA IR 5'],
              surfs['BA IR 6'],
              surfs['GT dashpot IR'],
              surfs['GT dashpot OR']],
    materials=[mats['Air'],
               mats['SS'],
               mats['Air'],
               mats['BSG'],
               mats['Air'],
               mats['SS'],
               mats['H2O'],
               mats['Zr'],
               mats['H2O']],
    grid='(top/bottom)')

univs['BA dashpot grid (intermediate)'] = make_pin(
    'BA dashpot grid (intermediate)',
    surfaces=[surfs['BA IR 1'],
              surfs['BA IR 2'],
              surfs['BA IR 3'],
              surfs['BA IR 4'],
              surfs['BA IR 5'],
              surfs['BA IR 6'],
              surfs['GT dashpot IR'],
              surfs['GT dashpot OR']],
    materials=[mats['Air'],
               mats['SS'],
               mats['Air'],
               mats['BSG'],
               mats['Air'],
               mats['SS'],
               mats['H2O'],
               mats['Zr'],
               mats['H2O']],
    grid='(intermediate)')

univs['BA blank SS'] = make_pin(
    'BA blank SS',
    surfaces=[surfs['BA IR 6'],
              surfs['BA IR 7'],
              surfs['BA IR 8']],
    materials=[mats['SS'],
               mats['H2O'],
               mats['Zr'],
               mats['H2O']])

univs['BA blank SS bare'] = make_pin(
    'BA blank SS bare',
    surfaces=[surfs['BA IR 6']],
    materials=[mats['SS'],
               mats['H2O']])

stack_surfs_BA = [
    surfs['bot support plate'],
    surfs['top support plate'],
    surfs['top lower nozzle'],
    surfs['top lower thimble'],
    surfs['grid1bot'],
    surfs['BA bot'],
    surfs['grid1top'],
    surfs['dashpot top'],
    surfs['grid2bot'],
    surfs['grid2top'],
    surfs['grid3bot'],
    surfs['grid3top'],
    surfs['grid4bot'],
    surfs['grid4top'],
    surfs['top active core'],
    surfs['top pin plenum'],
    surfs['top FR'],
    surfs['bot upper nozzle'],
    surfs['top upper nozzle']]

# Stack all axial pieces of control rod tubes together for each bank

univs['BA stack'] = make_stack(
    'BA stack', stack_surfs_BA,
    universes=[univs['water pin'],
               univs['water pin'],
               univs['water pin'],
               univs['GTd empty'],
               univs['GTd empty'],
               univs['GTd empty grid (top/bottom)'],
               univs['BA dashpot grid (top/bottom)'],
               univs['BA dashpot'],
               univs['BA'],
               univs['BA grid (intermediate)'],
               univs['BA'],
               univs['BA grid (intermediate)'],
               univs['BA'],
               univs['BA blank SS'],
               univs['BA blank SS'],
               univs['BA blank SS'],
               univs['BA blank SS'],
               univs['BA blank SS'],
               univs['BA blank SS bare']])


# FUEL PIN CELLS

univs['SS pin'] = make_pin(
    'SS pin',
    surfaces=[surfs['clad OR']],
    materials=[mats['SS'],
               mats['H2O']])

univs['end plug'] = make_pin(
    'end plug',
    surfaces=[surfs['clad OR']],
    materials=[mats['Zr'],
               mats['H2O']])

univs['pin plenum'] = make_pin(
    'pin plenum',
    surfaces=[surfs['plenum spring OR'],
              surfs['clad IR'],
              surfs['clad OR']],
    materials=[mats['In'],
               mats['He'],
               mats['Zr'],
               mats['H2O']])

univs['pin plenum grid (top/bottom)'] = make_pin(
    'pin plenum grid (top/bottom)',
    surfaces=[surfs['plenum spring OR'],
              surfs['clad IR'],
              surfs['clad OR']],
    materials=[mats['In'],
               mats['He'],
               mats['Zr'],
               mats['H2O']],
    grid='(top/bottom)')


# 1.6% ENRICHED FUEL PIN CELL

univs['Fuel (1.6\%)'] = make_pin(
    'Fuel (1.6\%)',
    surfaces=[surfs['pellet OR'],
              surfs['clad IR'],
              surfs['clad OR']],
    materials=[mats['UO2 1.6'],
               mats['He'],
               mats['Zr'],
               mats['H2O']])

univs['Fuel (1.6\%) grid (top/bottom)'] = make_pin(
    'Fuel (1.6\%) grid (top/bottom)',
    surfaces=[surfs['pellet OR'],
              surfs['clad IR'],
              surfs['clad OR']],
    materials=[mats['UO2 1.6'],
               mats['He'],
               mats['Zr'],
               mats['H2O']],
    grid='(top/bottom)')

univs['Fuel (1.6\%) grid (intermediate)'] = make_pin(
    'Fuel (1.6\%) grid (intermediate)',
    surfaces=[surfs['pellet OR'],
              surfs['clad IR'],
              surfs['clad OR']],
    materials=[mats['UO2 1.6'],
               mats['He'],
               mats['Zr'],
               mats['H2O']],
    grid='(intermediate)')

# Stack all axial pieces of 1.6% enriched fuel pin cell

univs['Fuel (1.6\%) stack'] = make_stack(
    'Fuel (1.6\%) stack',
    surfaces=stack_surfs,
    universes=[univs['water pin'],
               univs['SS pin'],
               univs['SS pin'],
               univs['end plug'],
               univs['Fuel (1.6\%)'],
               univs['Fuel (1.6\%) grid (top/bottom)'],
               univs['Fuel (1.6\%)'],
               univs['Fuel (1.6\%)'],
               univs['Fuel (1.6\%) grid (intermediate)'],
               univs['Fuel (1.6\%)'],
               univs['Fuel (1.6\%) grid (intermediate)'],
               univs['Fuel (1.6\%)'],
               univs['pin plenum'],
               univs['pin plenum grid (top/bottom)'],
               univs['pin plenum'],
               univs['end plug'],
               univs['water pin'],
               univs['SS pin'],
               univs['water pin']])


# 2.4% ENRICHED FUEL PIN CELL

univs['Fuel (2.4\%)'] = make_pin(
    'Fuel (2.4\%)',
    surfaces=[surfs['pellet OR'],
              surfs['clad IR'],
              surfs['clad OR']],
    materials=[mats['UO2 2.4'],
               mats['He'],
               mats['Zr'],
               mats['H2O']])

univs['Fuel (2.4\%) grid (top/bottom)'] = make_pin(
    'Fuel (2.4\%) grid (top/bottom)',
    surfaces=[surfs['pellet OR'],
              surfs['clad IR'],
              surfs['clad OR']],
    materials=[mats['UO2 2.4'],
               mats['He'],
               mats['Zr'],
               mats['H2O']],
    grid='(top/bottom)')

univs['Fuel (2.4\%) grid (intermediate)'] = make_pin(
    'Fuel (2.4\%) grid (intermediate)',
    surfaces=[surfs['pellet OR'],
              surfs['clad IR'],
              surfs['clad OR']],
    materials=[mats['UO2 2.4'],
               mats['He'],
               mats['Zr'],
               mats['H2O']],
    grid='(intermediate)')

# Stack all axial pieces of 2.4% enriched fuel pin cell

univs['Fuel (2.4\%) stack'] = make_stack(
    'Fuel (2.4\%) stack',
    surfaces=stack_surfs,
    universes=[univs['water pin'],
               univs['SS pin'],
               univs['SS pin'],
               univs['end plug'],
               univs['Fuel (2.4\%)'],
               univs['Fuel (2.4\%) grid (top/bottom)'],
               univs['Fuel (2.4\%)'],
               univs['Fuel (2.4\%)'],
               univs['Fuel (2.4\%) grid (intermediate)'],
               univs['Fuel (2.4\%)'],
               univs['Fuel (2.4\%) grid (intermediate)'],
               univs['Fuel (2.4\%)'],
               univs['pin plenum'],
               univs['pin plenum grid (top/bottom)'],
               univs['pin plenum'],
               univs['end plug'],
               univs['water pin'],
               univs['SS pin'],
               univs['water pin']])


# 3.1% ENRICHED FUEL PIN CELL

univs['Fuel (3.1\%)'] = make_pin(
    'Fuel (3.1\%)',
    surfaces=[surfs['pellet OR'],
              surfs['clad IR'],
              surfs['clad OR']],
    materials=[mats['UO2 3.1'],
               mats['He'],
               mats['Zr'],
               mats['H2O']])

univs['Fuel (3.1\%) grid (top/bottom)'] = make_pin(
    'Fuel (3.1\%) grid (top/bottom)',
    surfaces=[surfs['pellet OR'],
              surfs['clad IR'],
              surfs['clad OR']],
    materials=[mats['UO2 3.1'],
               mats['He'],
               mats['Zr'],
               mats['H2O']],
    grid='(top/bottom)')

univs['Fuel (3.1\%) grid (intermediate)'] = make_pin(
    'Fuel (3.1\%) grid (intermediate)',
    surfaces=[surfs['pellet OR'],
              surfs['clad IR'],
              surfs['clad OR']],
    materials=[mats['UO2 3.1'],
               mats['He'],
               mats['Zr'],
               mats['H2O']],
    grid='(intermediate)')

# Stack all axial pieces of 3.1% enriched fuel pin cell

univs['Fuel (3.1\%) stack'] = make_stack(
    'Fuel (3.1\%) stack',
    surfaces=stack_surfs,
    universes=[univs['water pin'],
               univs['SS pin'],
               univs['SS pin'],
               univs['end plug'],
               univs['Fuel (3.1\%)'],
               univs['Fuel (3.1\%) grid (top/bottom)'],
               univs['Fuel (3.1\%)'],
               univs['Fuel (3.1\%)'],
               univs['Fuel (3.1\%) grid (intermediate)'],
               univs['Fuel (3.1\%)'],
               univs['Fuel (3.1\%) grid (intermediate)'],
               univs['Fuel (3.1\%)'],
               univs['pin plenum'],
               univs['pin plenum grid (top/bottom)'],
               univs['pin plenum'],
               univs['end plug'],
               univs['water pin'],
               univs['SS pin'],
               univs['water pin']])