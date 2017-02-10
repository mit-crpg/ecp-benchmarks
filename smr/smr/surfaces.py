"""Instantiate the OpenMC Surfaces needed by the core model.

The geometric parameters defining the core model are tabulated here.
The geometric specifications are loosely based upon NuScale's Small
Modular Pressurized Water Reactor concept as detailed here in their
NRC design certification documentation:

https://www.nrc.gov/docs/ML1618/ML16187A017.pdf
https://www.nrc.gov/docs/ML1700/ML17007A001.pdf
"""

import copy
from math import tan, pi

import openmc


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

# pin cell parameters
pellet_OR          = 0.405765
clad_IR            = 0.41402
clad_OR            = 0.47498
rod_grid_side_tb   = 1.24416
rod_grid_side_i    = 1.21962
guide_tube_IR      = 0.5715
guide_tube_OR      = 0.61214
guide_tube_dash_IR = 0.54019
guide_tube_dash_OR = 0.61214
control_poison_OR  = 0.43310
control_rod_IR     = 0.43688
control_rod_OR     = 0.48387
burn_abs_r1        = 0.21400
burn_abs_r2        = 0.23051
burn_abs_r3        = 0.24130
burn_abs_r4        = 0.42672
burn_abs_r5        = 0.43688
burn_abs_r6        = 0.48387
burn_abs_r7        = 0.56134
burn_abs_r8        = 0.60198
instr_tube_IR      = 0.5715
instr_tube_OR      = 0.61214
plenum_spring_OR   = 0.06459

# grid spacer parameters
rod_grid_side_tb   = 1.24416
rod_grid_side_i    = 1.21962

# lattice parameters
pin_pitch          = 1.25984
lattice_pitch      = 21.50364
grid_strap_side    = 21.47270

# core radial paramters
core_barrel_IR     = 85.0
core_barrel_OR     = 90.0
neutron_shield_OR  = 92.0
baffle_width       = 2.2225
rpv_IR             = 120.0
rpv_OR             = 135.0

# axial paramters
lowest_extent        =      0.000
bottom_support_plate =     20.000
top_support_plate    =     25.000
bottom_lower_nozzle  =     25.000
top_lower_nozzle     =     35.160
bottom_fuel_rod      =     35.160
top_lower_thimble    =     36.007
bottom_fuel_stack    =     36.007
bot_burn_abs         =     41.087
active_core_height   =    182.880
top_active_core      =    218.887
top_plenum           =    221.223
top_fuel_rod         =    223.272
bottom_upper_nozzle  =    226.617
top_upper_nozzle     =    235.444
highest_extent       =    255.444

# grid z planes
grid1_bot             =    37.879
grid1_top             =    42.070
grid2_bot             =    99.164
grid2_top             =   104.879
grid3_bot             =   151.361
grid3_top             =   157.076
grid4_bot             =   203.558
grid4_top             =   209.273

# control rod step heights
step0H                =    45.079
step102H              =   206.415
step228H              =   249.122
step_width            =     1.58173
bank_bot              =   405.713
bank_step             =   228.
bank_top              =   766.348

neutron_shield_NWbot_SEtop = tan(pi/3)
neutron_shield_NWtop_SEbot = tan(pi/6)
neutron_shield_NEbot_SWtop = tan(-pi/3)
neutron_shield_NEtop_SWbot = tan(-pi/6)


surfs = {}

surfs['pellet OR'] = openmc.ZCylinder(
    R=pellet_OR, name='Pellet OR')
surfs['plenum spring OR'] = openmc.ZCylinder(
    R=plenum_spring_OR, name='FR Plenum Spring OR')
surfs['clad IR'] = openmc.ZCylinder(
    R=clad_IR, name='Clad IR')
surfs['clad OR'] = openmc.ZCylinder(
    R=clad_OR, name='Clad OR')
surfs['GT IR'] = openmc.ZCylinder(
    R=guide_tube_IR, name='GT IR (above dashpot)')
surfs['GT OR'] = openmc.ZCylinder(
    R=guide_tube_OR, name='GT OR (above dashpot)')
surfs['GT dashpot IR'] = openmc.ZCylinder(
    R=guide_tube_dash_IR, name='GT IR (at dashpot)')
surfs['GT dashpot OR'] = openmc.ZCylinder(
    R=guide_tube_dash_OR, name='GT OR (at dashpot)')
surfs['CP OR'] = openmc.ZCylinder(
    R=control_poison_OR, name='Control Poison OR')
surfs['CR IR'] = openmc.ZCylinder(
    R=control_rod_IR, name='CR Clad IR')
surfs['CR OR'] = openmc.ZCylinder(
    R=control_rod_OR, name='CR Clad OR')
surfs['BA IR 1'] = openmc.ZCylinder(
    R=burn_abs_r1, name='BA IR 1')
surfs['BA IR 2'] = openmc.ZCylinder(
    R=burn_abs_r2, name='BA IR 2')
surfs['BA IR 3'] = openmc.ZCylinder(
    R=burn_abs_r3, name='BA IR 3')
surfs['BA IR 4'] = openmc.ZCylinder(
    R=burn_abs_r4, name='BA IR 4')
surfs['BA IR 5'] = openmc.ZCylinder(
    R=burn_abs_r5, name='BA IR 5')
surfs['BA IR 6'] = openmc.ZCylinder(
    R=burn_abs_r6, name='BA IR 6')
surfs['BA IR 7'] = openmc.ZCylinder(
    R=burn_abs_r7, name='BA IR 7')
surfs['BA IR 8'] = openmc.ZCylinder(
    R=burn_abs_r8, name='BA IR 8')
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
surfs['baffle south'] = openmc.YPlane(
    y0=(lattice_pitch/4. - baffle_width), name='baffle north')
surfs['baffle north'] = openmc.YPlane(
    y0=(baffle_width - lattice_pitch/4.), name='baffle south')
surfs['baffle west'] = openmc.XPlane(
    x0=(lattice_pitch/4. - baffle_width), name='baffle east')
surfs['baffle east'] = openmc.XPlane(
    x0=(baffle_width - lattice_pitch/4), name='baffle west')