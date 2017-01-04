"""Creates a 2D fuel pin cell with reflective BCs."""

import numpy as np

import opencg
import openmc
import openmc.opencg_compatible as opencg_compatible
from beavrs.builder import BEAVRS


def find_pin(pin_name, wrap_geometry=True):
    """Find a fuel pin with some string name in the BEAVRS OpenCG model.

    This method extracts the pin cell and wraps it in an OpenCG Geometry.
    The returned geometry has reflective boundary conditions along the x and y
    boundaries. The z-axis left unbounded.

    Parameters
    ----------
    pin_name : str
        The name of the fuel pin universe
    wrap_geometry : bool
        If false, the pin cell Universe is returned. If true, the pin cell
        Universe is wrapped in an OpenCG Geometry and returned (default).

    Returns
    -------
    opencg.Universe
        The OpenCG Universe or Geometry for this fuel pin or None if not found

    """

    # Get all OpenCG Universes
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
        min_x = opencg.XPlane(x0=-pin_pitch, boundary='reflective')
        max_x = opencg.XPlane(x0=pin_pitch, boundary='reflective')
        min_y = opencg.YPlane(y0=-pin_pitch, boundary='reflective')
        max_y = opencg.YPlane(y0=pin_pitch, boundary='reflective')

        # Create a root Cell
        root_cell = opencg.Cell(name='root cell')
        root_cell.fill = fuel_pin

        # Add boundaries to the root Cell
        root_cell.add_surface(surface=min_x, halfspace=+1)
        root_cell.add_surface(surface=max_x, halfspace=-1)
        root_cell.add_surface(surface=min_y, halfspace=+1)
        root_cell.add_surface(surface=max_y, halfspace=-1)

        # Create a root Universe
        root_univ = opencg.Universe(universe_id=0, name='root universe')
        root_univ.add_cell(root_cell)

        # Create a Geometry
        fuel_pin = opencg.Geometry()
        fuel_pin.root_universe = root_univ

    return fuel_pin


#### Create OpenMC "materials.xml" and "geometry.xml" files

# User-specified enrichment of 1.6, 2.4 or 3.1 percent
enrichment = 1.6

# Instantiate a BEAVRS object
beavrs = BEAVRS(nndc_xs=True)

# Write all BEAVRS materials to materials.xml file
beavrs.write_openmc_materials()

# Extract fuel pin of interest from BEAVRS model
pin_name = 'Fuel rod active region - {}% enr'.format(enrichment)
pin_geometry = find_pin(pin_name)
openmc_geometry = opencg_compatible.get_openmc_geometry(pin_geometry)
openmc_geometry.export_to_xml()


#### Create OpenMC "settings.xml" file

# Query the user on whether to use multipole cross sections
multipole = input('Use multipole cross sections? (y/n): ').lower()
multipole = True if multipole == 'y' else False

# Construct uniform initial source distribution over fissionable zones
lower_left = pin_geometry.bounds[:2] + [-10.]
upper_right = pin_geometry.bounds[3:5] + [10.]
source = openmc.source.Source(space=openmc.stats.Box(lower_left, upper_right))
source.space.only_fissionable = True

settings_file = openmc.Settings()
settings_file.batches = 10
settings_file.inactive = 5
settings_file.particles = 10000
settings_file.ptables = True
settings_file.output = {'tallies': False}
settings_file.source = source
settings_file.sourcepoint_write = False

if multipole:
    settings_file.temperature = {'multipole': True, 'tolerance': 1000}

settings_file.export_to_xml()


#### Create OpenMC "plots.xml" file

# Initialize the BEAVRS color mapping scheme
beavrs.write_openmc_plots()

# Create a plot colored by materials
plot = openmc.Plot()
bounds = pin_geometry.bounds
plot.width = [pin_geometry.max_x - pin_geometry.min_x,
              pin_geometry.max_y - pin_geometry.min_y]
plot.origin = [bounds[0] + (bounds[3] - bounds[0]) / 2.,
               bounds[1] + (bounds[4] - bounds[1]) / 2.,
               bounds[2] + (bounds[5] - bounds[2]) / 2.]
plot.color = 'mat'
plot.filename = 'fuel-pin'
plot.col_spec = beavrs.plots.colspec_mat
plot.pixels = [1000, 1000]

plot_file = openmc.Plots([plot])
plot_file.export_to_xml()


#### Create OpenMC MGXS library and "tallies.xml" file

# CASMO 70-group structure
energy_groups = openmc.mgxs.EnergyGroups()
energy_groups.group_edges = np.array([
    0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.042, 0.05, 0.058, 0.067,
    0.08, 0.1, 0.14, 0.18, 0.22, 0.25, 0.28, 0.3, 0.32, 0.35, 0.4, 0.5, 0.625,
    0.78, 0.85, 0.91, 0.95, 0.972, 0.996, 1.02, 1.045, 1.071, 1.097, 1.123,
    1.15, 1.3, 1.5, 1.855, 2.1, 2.6, 3.3, 4., 9.877, 15.968, 27.7, 48.052,
    75.501, 148.73, 367.26001, 906.90002, 1.4251e3, 2.2395e3, 3.5191e3, 5.53e3,
    9.118e3, 15.03e3, 24.78e3, 40.85e3, 67.34e3, 111.e3, 183e3, 302.5e3, 500e3,
    821e3, 1.353e6, 2.231e6, 3.679e6, 6.0655e6, 2e7])

# Initialize a 70-group MGXS library
mgxs_lib = openmc.mgxs.Library(openmc_geometry, by_nuclide=True)
mgxs_lib.energy_groups = energy_groups
mgxs_lib.mgxs_types = ['total', 'nu-fission', 'nu-scatter matrix', 'chi']
mgxs_lib.domain_type = 'material'
mgxs_lib.correction = None
mgxs_lib.build_library()

# Create a "tallies.xml" file for the MGXS Library
tallies_file = openmc.Tallies()
mgxs_lib.add_to_tallies_file(tallies_file, merge=True)
tallies_file.export_to_xml()
