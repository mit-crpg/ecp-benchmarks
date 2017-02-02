import openmc

from surfaces import surfs

def make_assembly(name, latts, univs, surfs, mats, universes,
                  lower_left, width, grid_surfs=None, sleeve_mats=None):


    # Instantiate the lattice
    latts[name] = openmc.RectLattice(name=name)
    latts[name].lower_left = [lower_left, lower_left]
    latts[name].width = [width, width]
    latts[name].universes = univs

    # Add lattice to bounding cell
    univ_name = name + ' lattice'
    univs[univ_name] = openmc.Universe(name=univ_name)
    cell = openmc.Cell(name=univ_name)
    cell.fill = latts[name]
    cell.region = (-surfs['lat box xtop'] &
                   +surfs['lat box xbot'] &
                   -surfs['lat box ytop'] &
                   +surfs['lat box ybot'])


    # Make axial cells for outside of assembly
    cell = openmc.Cell(name=univ_name + ' axial 1')
    cell.material = mats['H2O']
    cell.region = ((-surfs['lat box ybot'] & -surfs['grid1bot']) ^
                   (+surfs['lat box ytop'] & -surfs['grid1bot']) ^
                   (+surfs['lat box xtop'] & -surfs['lat box ytop'] &
                    ))


grid_surfaces = [surfs['grid1bot'],
                 surfs['grid1top'],
                 surfs['grid2bot'],
                 surfs['grid2top'],
                 surfs['grid3bot'],
                 surfs['grid3top'],
                 surfs['grid4bot'],
                 surfs['grid4top']]

latts = {}
