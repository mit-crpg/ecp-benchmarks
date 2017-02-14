import opencg
import openmc.opencg_compatible as opencg_compatible
from beavrs.builder import BEAVRS


def find_assembly(assembly_name, wrap_geometry=True):
    """Find a fuel assembly with some string name in the BEAVRS OpenCG model.

    This method extracts the fuel assembly and wraps it in an OpenCG Geometry.
    The returned geometry has reflective boundary conditions along all
    boundaries. The z-axis is bounded between z=200 and z=210 cm.

    Parameters
    ----------
    assembly_name : str
        The name of the fuel assembly lattice
    wrap_geometry : bool
        If false, the fuel assembly Lattice is returned. If true, the fuel
        assembly Lattice is wrapped in an OpenCG Geometry and returned (default).

    Returns
    -------
    fuel_assembly
        The OpenCG Lattice or Geometry for the assembly or None if not found

    """

    # Get all OpenCG Universes
    all_univ = beavrs.main_universe.get_all_universes()

    # Iterate over all Universes
    fuel_assembly = None
    for univ_id, univ in all_univ.items():
        if univ.name == assembly_name:
            fuel_assembly = univ

    # Wrap lattice in a Geometry if requested by the user
    if wrap_geometry:

        # Create a root Cell
        root_cell = opencg.Cell(name='root cell')
        root_cell.fill = fuel_assembly

        # Make mixed reflective / vacuum boundaries
        min_x = opencg.XPlane(x0=root_cell.fill.min_x, boundary='reflective')
        max_x = opencg.XPlane(x0=root_cell.fill.max_x, boundary='reflective')
        min_y = opencg.YPlane(y0=root_cell.fill.min_y, boundary='reflective')
        max_y = opencg.YPlane(y0=root_cell.fill.max_y, boundary='reflective')
        max_z = opencg.ZPlane(z0=197.5, boundary='reflective')
        min_z = opencg.ZPlane(z0=192.5, boundary='reflective')

        # Add boundaries to the root Cell
        root_cell.add_surface(surface=min_x, halfspace=+1)
        root_cell.add_surface(surface=max_x, halfspace=-1)
        root_cell.add_surface(surface=min_y, halfspace=+1)
        root_cell.add_surface(surface=max_y, halfspace=-1)
        root_cell.add_surface(surface=min_z, halfspace=+1)
        root_cell.add_surface(surface=max_z, halfspace=-1)

        # Create a root Universe
        root_univ = opencg.Universe(universe_id=0, name='root universe')
        root_univ.add_cell(root_cell)

        # Create a Geometry
        fuel_assembly = opencg.Geometry()
        fuel_assembly.root_universe = root_univ

    return fuel_assembly


def build_two_by_two(assembly1_name, assembly2_name):
    """Build a 2x2 fuel assembly geometry.

    This routine puts reflective boundary conditions along all boundaries.

    Parameters
    ----------
    assembly1_name : str
        The BEAVRS fuel assembly to place in the bottom right and top left
    assembly2_name : str
        The BEAVRS fuel assembly to place in the bottom left and top right

    Returns
    -------
    opencg.Geometry
        A 2x2 fuel assembly OpenCG Geometry

    """

    fuel_assembly1 = find_assembly(assembly1_name, wrap_geometry=False)
    fuel_assembly2 = find_assembly(assembly2_name, wrap_geometry=False)

    # Find the water material
    all_cells = beavrs.main_universe.get_all_cells()
    for cell_uuid, cell in all_cells.items():
        if cell.type == 'material' and cell.fill.name == 'water':
            water = cell.fill

    # Create a Cell/Universe around the first fuel assembly
    fuel_cell1 = opencg.Cell(name='assm1 cell')
    fuel_cell1.fill = fuel_assembly1
    fuel_univ1 = opencg.Universe(name='assm1 universe')
    fuel_univ1.add_cell(fuel_cell1)

    # Create a Cell/Universe around the second fuel assembly
    fuel_cell2 = opencg.Cell(name='assm2 cell')
    fuel_cell2.fill = fuel_assembly2
    fuel_univ2 = opencg.Universe(name='assm2 universe')
    fuel_univ2.add_cell(fuel_cell2)

    # Create a 3x3 lattice two fuel assemblies surrounded by a water reflector
    two_by_two_lattice = opencg.Lattice(name='reflector')
    lat_width = fuel_assembly1.max_x - fuel_assembly1.min_x
    two_by_two_lattice.width = [lat_width, lat_width, 1000.]
    two_by_two_lattice.offset = [0., 0., 0.]
    two_by_two_lattice.dimension = [2, 2, 1]
    two_by_two_lattice.universes = [[fuel_univ1, fuel_univ2],
                                   [fuel_univ2, fuel_univ1]]

    # Create a Geometry around the reflected lattice
    root_cell = opencg.Cell(name='root cell')
    root_cell.fill = two_by_two_lattice

    # Make mixed reflective / vacuum boundaries
    min_x = opencg.XPlane(x0=root_cell.fill.min_x, boundary='periodic')
    max_x = opencg.XPlane(x0=root_cell.fill.max_x, boundary='periodic')
    min_y = opencg.YPlane(y0=root_cell.fill.min_y, boundary='periodic')
    max_y = opencg.YPlane(y0=root_cell.fill.max_y, boundary='periodic')
    min_z = opencg.ZPlane(z0=192.5, boundary='reflective')
    max_z = opencg.ZPlane(z0=197.5, boundary='reflective')

    # Add boundaries to the root Cell
    root_cell.add_surface(surface=min_x, halfspace=+1)
    root_cell.add_surface(surface=max_x, halfspace=-1)
    root_cell.add_surface(surface=min_y, halfspace=+1)
    root_cell.add_surface(surface=max_y, halfspace=-1)
    root_cell.add_surface(surface=min_z, halfspace=+1)
    root_cell.add_surface(surface=max_z, halfspace=-1)

    # Create a root Universe for this fuel assembly
    root_univ = opencg.Universe(universe_id=0, name='root universe')
    root_univ.add_cell(root_cell)

    # Create an OpenCG Geometry for this fuel assembly
    two_by_two = opencg.Geometry()
    two_by_two.root_universe = root_univ

    return two_by_two


#### Create OpenMC "materials.xml" and "geometry.xml" files

# Instantiate a BEAVRS object
beavrs = BEAVRS()

# Write all BEAVRS materials to materials.xml file
beavrs.write_openmc_materials()

# Extract fuel assemblies of interest from BEAVRS model
opencg_geometry = build_two_by_two('Fuel 1.6% enr instr no BAs',
                                   'Fuel 3.1% enr instr 20')
openmc_geometry = opencg_compatible.get_openmc_geometry(opencg_geometry)
