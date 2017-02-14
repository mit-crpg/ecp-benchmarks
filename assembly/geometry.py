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
        root_cell.add_surface(surface=min_x, halfspace=+1)
        root_cell.add_surface(surface=max_x, halfspace=-1)
        root_cell.add_surface(surface=min_y, halfspace=+1)
        root_cell.add_surface(surface=max_y, halfspace=-1)
        root_cell.add_surface(surface=min_z, halfspace=+1)
        root_cell.add_surface(surface=max_z, halfspace=-1)

        # Create a root Universe
        root_univ = openmc.Universe(universe_id=0, name='root universe')
        root_univ.add_cell(root_cell)

        # Create a Geometry
        fuel_assembly = openmc.Geometry()
        fuel_assembly.root_universe = root_univ

    return fuel_assembly


# Instantiate a BEAVRS object
beavrs = BEAVRS()

# Extract fuel assembly of interest from BEAVRS model
assm_name = 'Fuel 1.6% enr instr no BAs'
openmc_geometry = find_assembly(assm_name)
