import re

import openmc
from openmc.data import atomic_weight, atomic_mass



# Parameters


########## Borated Water #################

boron_ppm = 975

# Density of clean water at 2250 psia T=560F NIST
h2o_dens = 0.73986

# Weight percent of natural boron in borated water
wB_Bh2o = boron_ppm * 1.0e-6

# Borated water density
rho_Bh2o = h2o_dens / (1 - wB_Bh2o)

# Compute weight percent of clean water in borated water
wh2o_Bh2o = 1.0 - wB_Bh2o

# Compute molecular mass of clean water
M_h2o = 2. * atomic_weight('H') + atomic_weight('O')

# Compute molecular mass of borated water
M_Bh2o = 1. / (wB_Bh2o / atomic_weight('B') + wh2o_Bh2o / M_h2o)

# Compute atom fractions of boron and water
aB_Bh2o = wB_Bh2o * M_Bh2o / atomic_weight('B')
ah2o_Bh2o = wh2o_Bh2o * M_Bh2o / M_h2o

# Compute atom fractions of hydrogen, oxygen
ah_Bh2o = 2.0 * ah2o_Bh2o
aho_Bh2o = ah2o_Bh2o

# Create borated water for coolant / moderator
mat_h2o = openmc.Material(name='Borated Water')
mat_h2o.temperature = 300
mat_h2o.set_density('g/cc', rho_Bh2o)
mat_h2o.add_element('B', aB_Bh2o, 'ao')
mat_h2o.add_element('H', ah_Bh2o, 'ao')
mat_h2o.add_element('O', aho_Bh2o, 'ao')
mat_h2o.add_s_alpha_beta(name='lwtr', xs='15t')

# Create He gas material for fuel pin gap
mat_he = openmc.Material(hame='Helium')
mat_he.temperature = 300
mat_he.set_density('g/cc', 0.0015981)
mat_he.add_element('He', 1.0, 'ao')

# Create air material for instrument tubes
mat_air = openmc.Material(name='Air')
mat_air.temperature = 300
mat_air.set_density('g/cc', 000616)
mat_air.add_element('O', 0.2095, 'ao')
mat_air.add_element('N', 0.7809, 'ao')
mat_air.add_element('Ar', 0.00933, 'ao')
mat_air.add_element('C', 0.00027, 'ao')

# Create inconel 718 material
mat_in = openmc.Material(name='Inconel')
mat_in.temperature = 300
mat_in.set_density('g/cc', 8.2)
mat_in.add_lement('Si', 0.0035, 'wo')
mat_in.add_element('Cr', 0.1896, 'wo')
mat_in.add_element('Mn', 0.0087, 'wo')
mat_in.add_element('Fe', 0.2863, 'wo')
mat_in.add_element('Ni', 0.5119, 'wo')

# Create stainless steel material
mat_ss = openmc.Material(name='SS304')
mat_ss.temperature = 300
mat_ss.set_density('g/cc', 8.03)
mat_ss.add_element('Si', 0.0060, 'wo')
mat_ss.add_element('Cr', 0.1900, 'wo')
mat_ss.add_element('Mn', 0.0200, 'wo')
mat_ss.add_element('Fe', 0.6840, 'wo')
mat_ss.add_element('Ni', 0.1000, 'wo')

# Create carbon steel material
mat_cs = openmc.Material(name='Carbon Steel')
mat_cs.temperature = 300
mat_cs.set_density('g/cc', 7.8)
mat_cs.add_element('C', 0.00270, 'wo')
mat_cs.add_element('Mn', 0.00750, 'wo')
mat_cs.add_element('P', 0.00025, 'wo')
mat_cs.add_element('S', 0.00025, 'wo')
mat_cs.add_element('Si', 0.00400, 'wo')
mat_cs.add_element('Ni', 0.00750, 'wo')
mat_cs.add_element('Cr', 0.00350, 'wo')
mat_cs.add_element('Mo', 0.00625, 'wo')
mat_cs.add_element('V', 0.00050, 'wo')
mat_cs.add_element('Nb', 0.00010, 'wo')
mat_cs.add_element('Cu', 0.00200, 'wo')
mat_cs.add_element('Ca', 0.00015, 'wo')
mat_cs.add_element('B', 0.00003, 'wo')
mat_cs.add_element('Ti', 0.00015, 'wo')
mat_cs.add_element('Al', 0.00025, 'wo')
mat_cs.add_element('Fe', 0.96487, 'wo')

# Create zircaloy 4 material
mat_zr = openmc.Material(name='Zircaloy-4')
mat_zr.temperature = 300
mat_zr.set_density('g/cc', 6.55)
mat_zr.add_element('O', 0.00125, 'wo')
mat_zr.add_element('Cr', 0.0010, 'wo')
mat_zr.add_element('Fe', 0.0021, 'wo')
mat_zr.add_element('Zr', 0.98115, 'wo')
mat_zr.add_element('Sn', 0.0145, 'wo')

# Create Ag-In-Cd control rod material
mat_aic = openmc.Material(name='aic_rod')
mat_aic.temperature = 300
mat_aic.set_density('g/cc', 10.16)
mat_aic.add_element('Ag', 0.80, 'wo')
mat_aic.add_element('In', 0.15, 'wo')
mat_aic.add_element('Cd', 0.05, 'wo')


########## Borosilicate Glass #################

# CASMO weight fractions
wO_bsg = 0.5481
wAl_bsg = 0.0344
wSi_bsg = 0.3787
wB10_bsg = 0.0071
wB11_bsg = 0.0317

# Molar mass of borosilicate glass
M_bsg = 1.0 / (wO_bsg / atomic_weight('O') + wAl_bsg / atomic_weight('Al') +
               wSi_bsg /atomic_weight('Si') + wB10_bsg / atomic_mass('B10') +
               wB11_bsg / atomic_mass('B11'))

# Compute atom fractions for borosilicate glass
aO_bsg = wO_bsg * M_bsg / atomic_weight('O')
aAl_bsg = wAl_bsg * M_bsg / atomic_weight('Al')
aSi_bsg = wSi_bsg * M_bsg / atomic_weight('Si')
aB10_bsg = wB10_bsg * M_bsg / atomic_mass('B11')
aB11_bsg = wB11_bsg * M_bsg / atomic_mass('B10')
aB_bsg = aB10_bsg + aB11_bsg

# Compute atom fractions for boron
aB10_B = aB10_bsg / (aB10_bsg + aB11_bsg)
aB11_B = 1.0 - aB10_B

# Create borosilicate glass material
mat_bsg = openmc.Material(name='Borosilicate Glass')
mat_bsg.temperature = 300
mat_bsg.set_density('g/cc', 2.26)
mat_bsg.add_element('O', aO_bsg, 'ao')
mat_bsg.add_element('Si', aSi_bsg, 'ao')
mat_bsg.add_element('Al', aAl_bsg, 'ao')
mat_bsg.add_nuclide('B10', aB10_B, 'ao')
mat_bsg.add_nuclide('B11', aB11_B, 'ao')



########## Enriched UO2 Fuel #################

# Create 1.6% enriched UO2 fuel material
a_U234, a_U235, a_U238, a_U, a_O = get_fuel_aos(0.0161006)
mat_fuel16 = openmc.Material(name='1.6\% Enr. UO2 Fuel')
mat_fuel16.temperature = 300
mat_fuel16.set_density('g/cc', 10.31341)
mat_fuel16.add_element('O', a_O, 'ao')
mat_fuel16.add_element('U', a_U, 'ao', enrichment=0.0161006)

# Create 2.4% enriched UO2 fuel material
a_U234, a_U235, a_U238, a_U, a_O = get_fuel_aos(0.0239993)
mat_fuel16 = openmc.Material(name='2.4\% Enr. UO2 Fuel')
mat_fuel16.temperature = 300
mat_fuel16.set_density('g/cc', 10.29748)
mat_fuel16.add_element('O', a_O, 'ao')
mat_fuel16.add_element('U', a_U, 'ao', enrichment=0.0239993)

# Create 3.1% enriched UO2 fuel material
a_U234, a_U235, a_U238, a_U. a_O = get_fuel_aos(0.0310221)
mat_fuel16 = openmc.Material(name='3.1\% Enr. UO2 Fuel')
mat_fuel16.temperature = 300
mat_fuel16.set_density('g/cc', 10.30166)
mat_fuel16.add_element('O', a_O, 'ao')
mat_fuel16.add_element('U', a_U, 'ao', enrichment=0.0310221)


def get_fuel_aos(enr_U235):

    # Calculate molar mass of Uranium
    enr_U234 = 0.008 * enr_U235
    enr_U238 = 1.0 - (enr_U234 + enr_U235)
    MU = 1.0 / (enr_U234 / atomic_mass('U234') +
                enr_U235 / atomic_mass('U235') +
                enr_U238 / atomic_mass('U238'))

    # Determine molar mass of UO2
    MUO2 = MU + 2.0 * atomic_weight('O')

    # Compute weight percent of U in UO2
    wUpUO2 = MU/MUO2

    # Calculate Uranium isotopic atom fractions
    a_U234 = wUpUO2 * enr_U234 * MUO2 / atomic_mass('U234')
    a_U235 = wUpUO2 * enr_U235 * MUO2 / atomic_mass('U234')
    a_U238 = wUpUO2 * enr_U238 * MUO2 / atomic_mass('U234')

    # Calculate Uranium atom fraction
    a_U = wUpUO2 * MUO2 / MU

    # Calculate Oxygen atom fraction
    a_O = (1.0 - wUpUO2) * MUO2 / atomic_mass('O')

    return a_U234, a_U235, a_U238, a_U, a_O