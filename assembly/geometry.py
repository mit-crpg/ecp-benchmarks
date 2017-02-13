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


# Instantiate a BEAVRS object
beavrs = BEAVRS(nndc_xs=True)

# Extract fuel assembly of interest from BEAVRS model
assm_name = 'Fuel 1.6% enr instr no BAs'
opencg_geometry = find_assembly(assm_name)
openmc_geometry = opencg_compatible.get_openmc_geometry(opencg_geometry)
