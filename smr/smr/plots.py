"""Instantiate OpenMC Plots to visualize the core model."""

import openmc

from .surfaces import lowest_extent, highest_extent, lattice_pitch, rpv_OR
from .materials import mats


# color specifications
col_spec = {mats['H2O'].id:     [198, 226, 255],  # light blue
            mats['In'].id:      [101, 101, 101],  # dgray
            mats['CS'].id:      [  0,   0,   0],        # carbons black
            mats['Zr'].id:      [201, 201, 201],  # gray
            mats['SS'].id:      [  0,   0,   0],        # black
            mats['Air'].id:     [255, 255, 255],  # white
            mats['He'].id:      [255, 218, 185],  # light orange
            mats['BSG'].id:     [  0, 255,   0],      # green
            mats['AIC'].id:     [255,   0,   0],      # bright red
            mats['UO2 1.6'].id: [142,  35,  35],    # light red
            mats['UO2 2.4'].id: [255, 215,   0],    # gold
            mats['UO2 3.1'].id: [  0,   0, 128]}      # dark blue


# Create a collection of plots
plots = openmc.Plots()

plot = openmc.Plot(name='radial slice ')
plot.basis = 'xy'
plot.color = 'mat'
plot.origin = [0., 0., (highest_extent-lowest_extent)/2.]
plot.width = [25*lattice_pitch/2, 25*lattice_pitch/2.]
plot.filename = 'radial_xy_slice'
plot.col_spec = col_spec
plot.background = [255, 255, 255]
plot.pixels = [1000, 1000]
plots += [plot]

plot = openmc.Plot(name='axial slice')
plot.basis = 'xz'
plot.color = 'mat'
plot.origin = [0., 0., (highest_extent-lowest_extent)/2.]
plot.width = [rpv_OR*2., (highest_extent-lowest_extent)]
plot.filename = 'axial_xz_slice'
plot.col_spec = col_spec
plot.background = [255, 255, 255]
plot.pixels = [1000, 1000]
plots += [plot]

plot = openmc.Plot(name='assembly grid spacer')
plot.basis = 'xy'
plot.color = 'mat'
plot.origin = [0., 0., 102.021]
plot.width = [lattice_pitch*1.5, lattice_pitch*1.5]
plot.filename = 'assm_grid_spacer'
plot.col_spec = col_spec
plot.background = [255, 255, 255]
plot.pixels = [1000, 1000]
plots += [plot]

plot = openmc.Plot(name='assembly no spacer')
plot.basis = 'xy'
plot.color = 'mat'
plot.origin = [0., 0., 90.]
plot.width = [lattice_pitch*1.5, lattice_pitch*1.5]
plot.filename = 'assm_no_spacer'
plot.col_spec = col_spec
plot.background = [255, 255, 255]
plot.pixels = [1000, 1000]
plots += [plot]
