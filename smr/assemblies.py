import openmc

from surfaces import surfs


def make_assembly(name, mats, universes, lower_left, width):

    # FIXME: Add a docstring
    # FIXME: Make this general with a loop over axial sections

    # Instantiate the lattice
    lattice = openmc.RectLattice(name=name)
    lattice.lower_left = [lower_left, lower_left]
    lattice.width = [width, width]
    lattice.universes = universes

    # Create rectangular prism cylinder for lattice grid box
    lat_grid_box = (surfs['lat grid box outer'] &
                    openmc.Complement(surfs['lat grid box inner']))

    # Add lattice to bounding cell
    univ_name = name + ' lattice'
    universe = openmc.Universe(name=univ_name)
    cell = openmc.Cell(name=univ_name)
    cell.fill = lattice
    cell.region = surfs['lat box inner']
    universe.add_cell(cell)

    # Make bottom axial cell for outside of assembly (without sleeve)
    cell = openmc.Cell(name=univ_name + ' axial (0)')
    cell.material = mats['H2O']
    cell.region = lat_grid_box & -surfs['grid1bot']
    universe.add_cell(cell)

    # Make axial cell for outside of assembly (with sleeve)
    cell = openmc.Cell(name=univ_name + ' axial (1)')
    cell.material = mats['SS']
    cell.region = lat_grid_box & +surfs['grid1bot'] & -surfs['grid1top']
    universe.add_cell(cell)

    # Make axial cell for outside of assembly (without sleeve)
    cell = openmc.Cell(name=univ_name + ' axial (2)')
    cell.material = mats['H2O']
    cell.region = lat_grid_box & +surfs['grid1top'] & -surfs['grid2bot']
    universe.add_cell(cell)

    # Make axial cell for outside of assembly (with sleeve)
    cell = openmc.Cell(name=univ_name + ' axial (3)')
    cell.material = mats['Zr']
    cell.region = lat_grid_box & +surfs['grid2bot'] & -surfs['grid2top']
    universe.add_cell(cell)

    # Make axial cell for outside of assembly (without sleeve)
    cell = openmc.Cell(name=univ_name + ' axial (4)')
    cell.material = mats['H2O']
    cell.region = lat_grid_box & +surfs['grid2top'] & -surfs['grid3bot']
    universe.add_cell(cell)

    # Make axial cell for outside of assembly (with sleeve)
    cell = openmc.Cell(name=univ_name + ' axial (5)')
    cell.material = mats['Zr']
    cell.region = lat_grid_box & +surfs['grid3bot'] & -surfs['grid3top']
    universe.add_cell(cell)

    # Make axial cell for outside of assembly (without sleeve)
    cell = openmc.Cell(name=univ_name + ' axial (6)')
    cell.material = mats['H2O']
    cell.region = lat_grid_box & +surfs['grid3top'] & -surfs['grid4bot']
    universe.add_cell(cell)

    # Make axial cell for outside of assembly (with sleeve)
    cell = openmc.Cell(name=univ_name + ' axial (7)')
    cell.material = mats['SS']
    cell.region = lat_grid_box & +surfs['grid4bot'] & -surfs['grid4top']
    universe.add_cell(cell)

    # Make top axial cell for outside of assembly (without sleeve)
    cell = openmc.Cell(name=univ_name + ' axial (last)')
    cell.material = mats['H2O']
    cell.region = lat_grid_box & +surfs['grid4top']
    universe.add_cell(cell)

    return universe

