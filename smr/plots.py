import openmc

from surfaces import lowest_extent, highest_extent, lattice_pitch,\
    top_lower_nozzle, top_upper_nozzle, bottom_support_plate, top_fuel_rod
from materials import mats


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

plot = openmc.Plot(name='radial core map 1')
plot.basis = 'xy'
plot.color = 'mat'
plot.origin = [0., 0., (highest_extent-lowest_extent)/2.]
plot.width = [19*lattice_pitch/2, 19*lattice_pitch/2.]
plot.filename = 'radial_core_map1'
plot.col_spec = col_spec
plot.background = [255, 255, 255]
plot.pixels = [1000, 1000]
plots += [plot]

plot = openmc.Plot(name='radial core map 2')
plot.basis = 'xy'
plot.color = 'mat'
plot.origin = [0., 0., 40.]
plot.width = [19*lattice_pitch/2, 19*lattice_pitch/2.]
plot.filename = 'radial_core_map2'
plot.col_spec = col_spec
plot.background = [255, 255, 255]
plot.pixels = [1000, 1000]
plots += [plot]

plot = openmc.Plot(name='radial core map 3')
plot.basis = 'xy'
plot.color = 'mat'
plot.origin = [0., 0., 210.]
plot.width = [19*lattice_pitch/2, 19*lattice_pitch/2.]
plot.filename = 'radial_core_map3'
plot.col_spec = col_spec
plot.background = [255, 255, 255]
plot.pixels = [1000, 1000]
plots += [plot]

plot = openmc.Plot(name='row 8 axial')
plot.basis = 'xz'
plot.color = 'mat'
plot.origin = [0., 0., (highest_extent-lowest_extent)/2.]
plot.width = [(highest_extent-lowest_extent)/2.] * 2
plot.filename = 'row_8_mats_axial'
plot.col_spec = col_spec
plot.background = [255, 255, 255]
plot.pixels = [600, 600]
plots += [plot]

plot = openmc.Plot(name='mats J8 ax bot')
plot.basis = 'xz'
plot.color = 'mat'
plot.origin = [0., lattice_pitch, top_lower_nozzle]
plot.width = [lattice_pitch, 2.1*(top_lower_nozzle-bottom_support_plate)]
plot.filename = 'J8_mats_ax_bot'
plot.col_spec = col_spec
plot.background = [255, 255, 255]
plot.pixels = [400, int(400*2.1*(top_lower_nozzle-bottom_support_plate)/lattice_pitch)]
plots += [plot]

plot = openmc.Plot(name='mats J8 nozzle')
plot.basis = 'xy'
plot.color = 'mat'
plot.width = [lattice_pitch, lattice_pitch]
plot.origin = [0., lattice_pitch, bottom_support_plate]
plot.filename = 'J8_mats_nozzle'
plot.col_spec = col_spec
plot.background = [255, 255, 255]
plot.pixels = [400, 400]
plots += [plot]

plot = openmc.Plot(name='mats H8 axial top')
plot.basis = 'xy'
plot.color = 'mat'
plot.origin = [0., 0., top_fuel_rod]
plot.width = [lattice_pitch, 5*(top_upper_nozzle-top_fuel_rod)]
plot.filename = 'H8_mats_ax_top'
plot.col_spec = col_spec
plot.background = [255, 255, 255]
plot.pixels = [400, int(400*2.1*(top_upper_nozzle-top_fuel_rod)/lattice_pitch)]
plots += [plot]