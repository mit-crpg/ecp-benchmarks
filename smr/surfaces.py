import copy
import math

import openmc

# FIXME: Add back parameters for pin cell radial surfaces
# FIXME: Cleanup parameters
# FIXME: Add docstring explanation


# Notation
# GT: Guide Tube
# BA: Burnable Absorber
# CP: Control Poison
# FR: Fuel Rod
# IR: Inner Radius
# OR: Outer Radius
# IT: Instrument Tube
# FA: Fuel Assembly
# RPV: Reactor Pressure Vessel

# Parameters
rod_grid_side_tb  = 1.24416
rod_grid_side_i   = 1.21962

## lattice parameters
pin_pitch         = 1.25984
lattice_pitch     = 21.50364
grid_strap_side   = 21.47270

## radial paramters
core_barrel_IR    = 85.0
core_barrel_OR    = 90.0
neutron_shield_OR = 92.0
baffle_width      = 2.2225
rpv_IR            = 120.0
rpv_OR            = 135.0

## axial paramters
lowest_extent        =      0.000  #
highest_extent       =    255.444  # arbitrary amount of water above core
bottom_support_plate =     20.000  # arbitrary amount of water below core
top_support_plate    =     25.000  # guessed
bottom_lower_nozzle  =     25.000  # same as topSupportPlate
top_lower_nozzle     =     35.160  # approx from seabrook NDR of 4.088in for lower nozzle height
bottom_fuel_rod      =     35.160  # same as top_lower_nozzle
top_lower_thimble    =     36.007  # approx as 1/3 of inch, this is exact seabrook NDR value for bottom thimble
bottom_fuel_stack    =     36.007  # same as topLowerThimble
active_core_height   =    182.880  # provided by D***
top_active_core      =    218.887  # bottomFuelStack + activeCoreHeight
bot_burn_abs         =     41.087  # approx from seabrook NDR of 1.987in for space between bot of BAs and bot of active fuel

# grid z planes (heights 1.65 top/bottom, 2.25 intermediate)
grid1_center          =     39.974  # bottomFuelStack + 1.562in
grid1_bot             =     37.879  # grid1Center - 1.65/2
grid1_top             =     42.070  # grid1Center + 1.65/2
grid2_center          =    102.021  # bottomFuelStack + 25.990in
grid2_bot             =     99.164  # grid2Center - 2.25/2
grid2_top             =    104.879  # grid2Center + 2.25/2
grid3_center          =    154.218  # bottomFuelStack + 46.540in
grid3_bot             =    151.361  # grid3Center - 2.25/2
grid3_top             =    157.076  # grid3Center + 2.25/2
grid4_center          =    206.415  # bottomFuelStack + 67.090in
grid4_bot             =    203.558  # grid4Center - 2.25/2
grid4_top             =    209.273  # grid4Center + 2.25/2

# control rod step heights
step0H               =     45.079  # chosen to match the step size calculated for intervals between other grids
step36H              =    102.021  # grid2Center
step69H              =    154.218  # grid3Center
step102H             =    206.415  # grid4Center
step228H             =    249.122  # set using calculated step width (27*stepWidth + step102H)
step_width            =    1.58173  # calculated from grid center planes

bank_bot  = 405.713
bank_step = 228
bank_top  = 766.348

top_fuel_rod        =    223.272
top_plenum          =    221.223
bottom_upper_nozzle =    226.617
top_upper_nozzle    =    235.444

neutron_shield_NWbot_SEtop = math.tan(math.pi/3)
neutron_shield_NWtop_SEbot = math.tan(math.pi/6)
neutron_shield_NEbot_SWtop = math.tan(-math.pi/3)
neutron_shield_NEtop_SWbot = math.tan(-math.pi/6)


surfs = {}

surfs['pellet OR'] = openmc.ZCylinder(R=0.39218)
surfs['plenum spring OR'] = openmc.ZCylinder(
    R=0.06459, name='FR Plenum Spring OR')
surfs['clad IR'] = openmc.ZCylinder(
    R=0.40005, name='Clad IR')
surfs['clad OR'] = openmc.ZCylinder(
    R=0.45720, name='Clad OR')
surfs['GT IR'] = openmc.ZCylinder(
    R=0.56134, name='GT IR (above dashpot)')
surfs['GT OR'] = openmc.ZCylinder(
    R=0.60198, name='GT OR (above dashpot)')
surfs['GT dashpot IR'] = openmc.ZCylinder(
    R=0.50419, name='GT IR (at dashpot)')
surfs['GT dashpot OR'] = openmc.ZCylinder(
    R=0.54610, name='GT OR (at dashpot)')
surfs['CP OR'] = openmc.ZCylinder(
    R=0.43310, name='Control Poison OR')
surfs['CR IR'] = openmc.ZCylinder(
    R=0.43688, name='CR Clad IR')
surfs['CR OR'] = openmc.ZCylinder(
    R=0.48387, name='CR Clad OR')
surfs['BA IR 1'] = openmc.ZCylinder(
    R=0.21400, name='BA IR 1')
surfs['BA IR 2'] = openmc.ZCylinder(
    R=0.23051, name='BA IR 2')
surfs['BA IR 3'] = openmc.ZCylinder(
    R=0.24130, name='BA IR 3')
surfs['BA IR 4'] = openmc.ZCylinder(
    R=0.42672, name='BA IR 4')
surfs['BA IR 5'] = openmc.ZCylinder(
    R=0.43688, name='BA IR 5')
surfs['BA IR 6'] = openmc.ZCylinder(
    R=0.48387, name='BA IR 6')
surfs['BA IR 7'] = openmc.ZCylinder(
    R=0.56134, name='BA IR 7')
surfs['BA IR 8'] = openmc.ZCylinder(
    R=0.60198, name='BA IR 8')
surfs['IT IR'] = copy.deepcopy(surfs['BA IR 5'])
surfs['IT OR'] = copy.deepcopy(surfs['BA IR 6'])

# Rectangular prisms for grid spacers
surfs['rod grid box (top/bottom)'] = \
    openmc.get_rectangular_prism(rod_grid_side_tb, rod_grid_side_tb)
surfs['rod grid box (intermediate)'] = \
    openmc.get_rectangular_prism(rod_grid_side_i, rod_grid_side_i)

# Rectangular prisms for lattice grid sleeves
surfs['lat grid box inner'] = \
    openmc.get_rectangular_prism(17.*pin_pitch, 17.*pin_pitch)
surfs['lat grid box outer'] = \
    openmc.get_rectangular_prism(grid_strap_side, grid_strap_side)

surfs['lowest extent'] = openmc.ZPlane(
    z0=lowest_extent, name='lowest extent')
surfs['bot support plate'] = openmc.ZPlane(
    z0=bottom_support_plate, name='bot support plate')
surfs['top support plate'] = openmc.ZPlane(
    z0=top_support_plate, name='top support plate')
surfs['bottom FR'] = openmc.ZPlane(z0=bottom_fuel_rod, name='bottom FR')
surfs['top lower nozzle'] = copy.deepcopy(surfs['bottom FR'])
surfs['bot lower nozzle'] = copy.deepcopy(surfs['top support plate'])

# axial surfaces
surfs['bot active core'] = openmc.ZPlane(
    z0=bottom_fuel_stack, name='bot active core')
surfs['top active core'] = openmc.ZPlane(
    z0=top_active_core, name='top active core')

surfs['top lower thimble'] = copy.deepcopy(surfs['bot active core'])
surfs['BA bot'] = openmc.ZPlane(
    z0=bot_burn_abs, name='bottom of BA')

surfs['grid1bot'] = openmc.ZPlane(
    z0=grid1_bot, name='bottom grid 1')
surfs['grid1top'] = openmc.ZPlane(
    z0=grid1_top, name='top of grid 1')
surfs['dashpot top'] = openmc.ZPlane(
    z0=step0H, name='top dashpot')
surfs['grid2bot'] = openmc.ZPlane(
    z0=grid2_bot, name='bottom grid 2')
surfs['grid2top'] = openmc.ZPlane(
    z0=grid2_top, name='top grid 2')
surfs['grid3bot'] = openmc.ZPlane(
    z0=grid3_bot, name='bottom of grid 3')
surfs['grid3top'] = openmc.ZPlane(
    z0=grid3_top, name='top of grid 3')
surfs['grid4bot'] = openmc.ZPlane(
    z0=grid4_bot, name='bottom of grid 4')
surfs['grid4top'] = openmc.ZPlane(
    z0=grid4_top, name='top grid 4')

surfs['top pin plenum'] = openmc.ZPlane(
    z0=top_plenum, name='top pin plenum')
surfs['top FR'] = openmc.ZPlane(
    z0=top_fuel_rod, name='top FR')
surfs['bot upper nozzle'] = openmc.ZPlane(
    z0=bottom_upper_nozzle, name='bottom upper nozzle')
surfs['top upper nozzle'] = openmc.ZPlane(
    z0=top_upper_nozzle, name='top upper nozzle')
surfs['highest extent'] = openmc.ZPlane(
    z0=highest_extent, name='highest extent')

# Control rod bank surfaces for ARO configuration
for bank in ['A','B','C','D','E',]:
    surfs['bankS{} top'.format(bank)] = openmc.ZPlane(
        z0=step228H+step_width*228, name='CR bankS{} top'.format(bank))
    surfs['bankS{} bot'.format(bank)] = openmc.ZPlane(
        z0=step228H, name='CR bankS{} bottom'.format(bank))

surfs['bankA top'] = openmc.ZPlane(
    z0=bank_top, name='CR bank A top')
surfs['bankA bot'] = openmc.ZPlane(
    z0=bank_bot, name='CR bank A bottom')
surfs['bankB top'] = openmc.ZPlane(
    z0=bank_top, name='CR bank B top')
surfs['bankB bot'] = openmc.ZPlane(
    z0=bank_bot, name='CR bank B bottom')
surfs['bankC top'] = openmc.ZPlane(
    z0=bank_top, name='CR bank C top')
surfs['bankC bot'] = openmc.ZPlane(
    z0=bank_bot, name='CR bank C bottom')
surfs['bankD top'] = openmc.ZPlane(
    z0=bank_top, name='CR bank D top')
surfs['bankD bot'] = openmc.ZPlane(
    z0=bank_bot, name='CR bank D bottom')

# outer radial surfaces
surfs['core barrel IR'] = openmc.ZCylinder(
    R=core_barrel_IR, name='core barrel IR')
surfs['core barrel OR'] = openmc.ZCylinder(
    R=core_barrel_OR, name='core barrel OR')
surfs['neutron shield OR'] = openmc.ZCylinder(
    R=neutron_shield_OR, name='neutron shield OR')

# neutron shield planes
surfs['neutron shield NWbot SEtop'] = openmc.Plane(
    A=1., B=neutron_shield_NWbot_SEtop, C=0., D=0.,
    name='neutron shield NWbot SEtop')
surfs['neutron shield NWtop SEbot'] = openmc.Plane(
    A=1., B=neutron_shield_NWtop_SEbot, C=0., D=0.,
    name='neutron shield NWtop SEbot')
surfs['neutron shield NEbot SWtop'] = openmc.Plane(
    A=1., B=neutron_shield_NEbot_SWtop, C=0., D=0.,
    name='neutron shield NEbot SWtop')
surfs['neutron shield NEtop SWbot'] = openmc.Plane(
    A=1., B=neutron_shield_NEtop_SWbot, C=0., D=0.,
    name='neutron shield NEtop SWbot')

# outer radial surfaces
surfs['RPV IR'] = openmc.ZCylinder(
    R=rpv_IR, name='RPV IR')
surfs['RPV OR'] = openmc.ZCylinder(
    R=rpv_OR, name='RPV OR', boundary_type='vacuum')

# outer axial surfaces
surfs['upper bound'] = openmc.ZPlane(
    z0=highest_extent, name='upper problem boundary', boundary_type='vacuum')
surfs['lower bound'] = openmc.ZPlane(
    z0=lowest_extent, name='lower problem boundary', boundary_type='vacuum')

# baffle surfaces
surfs['baffle north'] = openmc.YPlane(
    y0=(lattice_pitch/4. - baffle_width), name='baffle north')
surfs['baffle south'] = openmc.YPlane(
    y0=(baffle_width - lattice_pitch/4.), name='baffle south')
surfs['baffle east'] = openmc.XPlane(
    x0=(lattice_pitch/4. - baffle_width), name='baffle east')
surfs['baffle west'] = openmc.XPlane(
    x0=(baffle_width - lattice_pitch/4), name='baffle west')