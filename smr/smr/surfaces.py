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

INCHES = 2.54

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

# fuel rod parameters
pellet_OR          = 0.3195*INCHES/2  # DC, Table 4.1-2
clad_IR            = 0.326*INCHES/2   # DC, Table 4.1-2
clad_OR            = 0.374*INCHES/2   # DC, Table 4.1-2
active_fuel_length = 78.74*INCHES     # DC, Figure 4.2-10
plenum_length      = 5.311*INCHES     # DC, Figure 4.2-10
fuel_rod_length    = 85.00*INCHES     # Table 4.1-2
lower_end_cap      = 0.575*INCHES     # ML17007A001, Table 3-2

# pin cell parameters
guide_tube_IR      = 0.450*INCHES/2  # DC, Table 4.1-2
guide_tube_OR      = 0.482*INCHES/2  # DC, Table 4.1-2
guide_tube_dash_IR = 0.397*INCHES/2  # DC, Table 4.1-2
guide_tube_dash_OR = guide_tube_OR
boron_carbide_OR   = 0.333*INCHES/2  # DC, Table 4.1-3
ag_in_cd_OR        = 0.336*INCHES/2  # DC, Table 4.1-3
control_rod_IR     = 0.344*INCHES/2  # DC, Table 4.1-3
control_rod_OR     = 0.381*INCHES/2  # DC, Table 4.1-3
burn_abs_r1        = 0.21400
burn_abs_r2        = 0.23051
burn_abs_r3        = 0.24130
burn_abs_r4        = 0.42672
burn_abs_r5        = 0.43688
burn_abs_r6        = 0.48387
burn_abs_r7        = 0.56134
burn_abs_r8        = 0.60198
instr_tube_IR      = 0.450*INCHES/2  # ML17007A001, Table 3-1
instr_tube_OR      = 0.482*INCHES/2  # ML17007A001, Table 3-1
plenum_spring_OR   = 0.06459  # Estimate, actual is ECI

# grid spacer parameters
rod_grid_side    = 1.24416
spacer_height = 1.750*INCHES  # DC, Figure 4.2-7

# assembly parameters
assembly_length = 95.89*INCHES  # DC, Table 4.1-2
pin_pitch          = 0.496*INCHES  # DC, Table 4.1-2
lattice_pitch      = 8.466*INCHES  # DC, Table 4.1-2
grid_strap_side    = 21.47270
top_nozzle_height   = 3.551*INCHES  # DC, Figure 4.2-2
top_nozzle_width    = 8.406*INCHES  # DC, Figure 4.2-2

# core radial parameters
core_barrel_IR     = 74*INCHES/2  # DC, Table 4.1-2
core_barrel_OR     = 78*INCHES/2  # DC, Table 4.1-2
neutron_shield_OR  = core_barrel_OR + 2.0
baffle_width       = 2.2225
rpv_IR             = 120.0  # Estimate?
rpv_OR             = 135.0  # Estimate?

# axial parameters
lowest_extent        =      0.000
bottom_support_plate =     20.000
top_support_plate    =     25.000
bottom_lower_nozzle  =     25.000
top_lower_nozzle     =     35.160
bottom_fuel_rod      =     35.160
top_lower_thimble    =     36.007
bottom_fuel_stack    =     36.007
bot_burn_abs         =     41.087
active_core_height   =    200.
top_active_core      =    236.007
top_plenum           =    238.343
top_fuel_rod         =    240.392
bottom_upper_nozzle  =    243.737
top_upper_nozzle     =    252.564
highest_extent       =    272.564

# The grid spacer locations are eyeball estimated from Figure 3-1 in NuScale's
# FA design certification doc. This assumes 6cm and 2cm spacings between the
# bottom and top of the fuel rods and the bottom and top grid spacers.
grid1_bot             =     39.7845
grid1_top             =     44.2295
grid2_bot             =     86.67325
grid2_top             =     91.11825
grid3_bot             =    133.562
grid3_top             =    138.007
grid4_bot             =    180.45075
grid4_top             =    184.89575
grid5_bot             =    227.3395
grid5_top             =    231.7845

# control rod step heights - taken from BEAVRS, use with caution for NuScale
step0H                =    45.079
step102H              =   206.415
step248H              =   269.122
step_width            =     1.58173
bank_bot              =   405.713
bank_step             =   248.
bank_top              =   786.348

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
    R=boron_carbide_OR, name='Control Poison OR')
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
surfs['rod grid box'] = \
    openmc.get_rectangular_prism(rod_grid_side, rod_grid_side)

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
surfs['grid5bot'] = openmc.ZPlane(
    z0=grid5_bot, name='bottom of grid 5')
surfs['grid5top'] = openmc.ZPlane(
    z0=grid5_top, name='top grid 5')

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
        z0=step248H+step_width*228, name='CR bankS{} top'.format(bank))
    surfs['bankS{} bot'.format(bank)] = openmc.ZPlane(
        z0=step248H, name='CR bankS{} bottom'.format(bank))

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
