"""Creates a 2D fuel pin cell with reflective BCs."""

import numpy as np

import openmc
from beavrs.builder import BEAVRS


def find_pin(pin_name, wrap_geometry=True):
    """Find a fuel pin with some string name in the BEAVRS OpenMC model.

    This method extracts the pin cell and wraps it in an OpenMC Geometry.
    The returned geometry has reflective boundary conditions along the x and y
    boundaries. The z-axis left unbounded.

    Parameters
    ----------
    pin_name : str
        The name of the fuel pin universe
    wrap_geometry : bool
        If false, the pin cell Universe is returned. If true, the pin cell
        Universe is wrapped in an OpenMC Geometry and returned (default).

    Returns
    -------
    openmc.Universe
        The OpenMC Universe or Geometry for this fuel pin or None if not found

    """

    # Get all OpenMC Universes
    all_univ = beavrs.main_universe.get_all_universes()

    # Iterate over all Universes
    fuel_pin = None
    for univ_id, univ in all_univ.items():
        if univ._name == pin_name:
            fuel_pin = univ

    # Wrap pin cell Universe in a Geometry if requested by the user
    if wrap_geometry:

        # Make reflective boundaries
        pin_pitch = 0.62992
        min_x = openmc.XPlane(x0=-pin_pitch, boundary_type='reflective')
        max_x = openmc.XPlane(x0=pin_pitch, boundary_type='reflective')
        min_y = openmc.YPlane(y0=-pin_pitch, boundary_type='reflective')
        max_y = openmc.YPlane(y0=pin_pitch, boundary_type='reflective')

        # Create a root Cell
        root_cell = openmc.Cell(name='root cell')
        root_cell.fill = fuel_pin

        # Add boundaries to the root Cell
        root_cell.add_surface(surface=min_x, halfspace=+1)
        root_cell.add_surface(surface=max_x, halfspace=-1)
        root_cell.add_surface(surface=min_y, halfspace=+1)
        root_cell.add_surface(surface=max_y, halfspace=-1)

        # Create a root Universe
        root_univ = openmc.Universe(universe_id=0, name='root universe')
        root_univ.add_cell(root_cell)

        # Create a Geometry
        fuel_pin = openmc.Geometry()
        fuel_pin.root_universe = root_univ

    return fuel_pin


# User-specified enrichment of 1.6, 2.4 or 3.1 percent
enrichment = 1.6

# Instantiate a BEAVRS object
beavrs = BEAVRS()

# Extract fuel pin of interest from BEAVRS model
pin_name = 'Fuel rod active region - {}% enr'.format(enrichment)
openmc_geometry = find_pin(pin_name)
