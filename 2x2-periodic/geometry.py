import openmc
from beavrs.builder import BEAVRS


def find_assembly(assembly_name, wrap_geometry=True):
    """Find a fuel assembly with some string name in the BEAVRS OpenMC model.

    This method extracts the fuel assembly and wraps it in an OpenMC Geometry.
    The returned geometry has reflective boundary conditions along all
    boundaries. The z-axis is bounded between z=200 and z=210 cm.

    Parameters
    ----------
    assembly_name : str
        The name of the fuel assembly lattice
    wrap_geometry : bool
        If false, the fuel assembly Lattice is returned. If true, the fuel
        assembly Lattice is wrapped in an OpenMC Geometry and returned (default).

    Returns
    -------
    fuel_assembly
        The OpenMC Lattice or Geometry for the assembly or None if not found

    """

    # Get OpenMC Lattices for the fuel assembly
    fuel_assembly = \
        beavrs.openmc_geometry.get_lattices_by_name(assembly_name)[0]

    # Wrap lattice in a Geometry if requested by the user
    if wrap_geometry:

        # Create a root Cell
        root_cell = openmc.Cell(name='root cell')
        root_cell.fill = fuel_assembly

        # Make mixed reflective / vacuum boundaries
        min_x = openmc.XPlane(x0=-10.70864, boundary_type='reflective')
        max_x = openmc.XPlane(x0=+10.70864, boundary_type='reflective')
        min_y = openmc.YPlane(y0=-10.70864, boundary_type='reflective')
        max_y = openmc.YPlane(y0=+10.70864, boundary_type='reflective')
        max_z = openmc.ZPlane(z0=197.5, boundary_type='reflective')
        min_z = openmc.ZPlane(z0=192.5, boundary_type='reflective')

        # Add boundaries to the root Cell
        root_cell.region = \
            +min_x & -max_x & +min_y & -max_y & +min_z & -max_z

        # Create a root Universe
        root_univ = openmc.Universe(universe_id=0, name='root universe')
        root_univ.add_cell(root_cell)

        # Create a Geometry
        fuel_assembly = openmc.Geometry(root_univ)

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
    openmc.Geometry
        A 2x2 fuel assembly OpenMC Geometry

    """

    fuel_assembly1 = find_assembly(assembly1_name, wrap_geometry=False)
    fuel_assembly2 = find_assembly(assembly2_name, wrap_geometry=False)

    # Find the water material
    all_cells = beavrs.main_universe.get_all_cells()
    for cell_uuid, cell in all_cells.items():
        if cell.fill_type == 'material' and cell.fill.name == 'Borated Water':
            water = cell.fill

    # Create a Cell/Universe around the first fuel assembly
    fuel_cell1 = openmc.Cell(name='assm1 cell')
    fuel_cell1.fill = fuel_assembly1
    fuel_univ1 = openmc.Universe(name='assm1 universe')
    fuel_univ1.add_cell(fuel_cell1)

    # Create a Cell/Universe around the second fuel assembly
    fuel_cell2 = openmc.Cell(name='assm2 cell')
    fuel_cell2.fill = fuel_assembly2
    fuel_univ2 = openmc.Universe(name='assm2 universe')
    fuel_univ2.add_cell(fuel_cell2)

    # Create a 3x3 lattice two fuel assemblies surrounded by a water reflector
    two_by_two_lattice = openmc.RectLattice(name='reflector')
    two_by_two_lattice.lower_left = [-21.41728, -21.41728, -500.]
    two_by_two_lattice.pitch = [21.41728, 21.41728, 1000.]
    two_by_two_lattice.universes = [[[fuel_univ1, fuel_univ2],
                                    [fuel_univ2, fuel_univ1]]]

    # Create a Geometry around the reflected lattice
    root_cell = openmc.Cell(name='root cell')
    root_cell.fill = two_by_two_lattice

    # Make mixed reflective / vacuum boundaries
    min_x = openmc.XPlane(x0=-21.41728, boundary_type='periodic')
    max_x = openmc.XPlane(x0=+21.41728, boundary_type='periodic')
    min_y = openmc.YPlane(y0=-21.41728, boundary_type='periodic')
    max_y = openmc.YPlane(y0=+21.41728, boundary_type='periodic')
    min_z = openmc.ZPlane(z0=192.5, boundary_type='reflective')
    max_z = openmc.ZPlane(z0=197.5, boundary_type='reflective')

    # Add boundaries to the root Cell
    root_cell.region = +min_x & -max_x & +min_y & -max_y & +min_z & -max_z

    # Create a root Universe for this fuel assembly
    root_univ = openmc.Universe(universe_id=0, name='root universe')
    root_univ.add_cell(root_cell)

    # Create an OpenMC Geometry for this fuel assembly
    two_by_two = openmc.Geometry(root_univ)

    return two_by_two


#### Create OpenMC "materials.xml" and "geometry.xml" files

# Instantiate a BEAVRS object
beavrs = BEAVRS()

# Write all BEAVRS materials to materials.xml file
beavrs.write_openmc_materials()

# Extract fuel assemblies of interest from BEAVRS model
openmc_geometry = build_two_by_two('Fuel 1.6% enr instr no BAs',
                                   'Fuel 3.1% enr instr 20')
