import openmc
from openmc.data import atomic_weight, atomic_mass

# FIXME: Write docstrings

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
    a_O = (1.0 - wUpUO2) * MUO2 / atomic_mass('O16')

    return a_U234, a_U235, a_U238, a_U, a_O

mats = {}

# Create He gas material for fuel pin gap
mats['He'] = openmc.Material(name='Helium')
mats['He'].temperature = 300
mats['He'].set_density('g/cc', 0.0015981)
mats['He'].add_element('He', 1.0, 'ao')

# Create air material for instrument tubes
mats['Air'] = openmc.Material(name='Air')
mats['Air'].temperature = 300
mats['Air'].set_density('g/cc', 0.00616)
mats['Air'].add_element('O', 0.2095, 'ao')
mats['Air'].add_element('N', 0.7809, 'ao')
mats['Air'].add_element('Ar', 0.00933, 'ao')
mats['Air'].add_element('C', 0.00027, 'ao')

# Create inconel 718 material
mats['In'] = openmc.Material(name='Inconel')
mats['In'].temperature = 300
mats['In'].set_density('g/cc', 8.2)
mats['In'].add_element('Si', 0.0035, 'wo')
mats['In'].add_element('Cr', 0.1896, 'wo')
mats['In'].add_element('Mn', 0.0087, 'wo')
mats['In'].add_element('Fe', 0.2863, 'wo')
mats['In'].add_element('Ni', 0.5119, 'wo')

# Create stainless steel material
mats['SS'] = openmc.Material(name='SS304')
mats['SS'].temperature = 300
mats['SS'].set_density('g/cc', 8.03)
mats['SS'].add_element('Si', 0.0060, 'wo')
mats['SS'].add_element('Cr', 0.1900, 'wo')
mats['SS'].add_element('Mn', 0.0200, 'wo')
mats['SS'].add_element('Fe', 0.6840, 'wo')
mats['SS'].add_element('Ni', 0.1000, 'wo')

# Create carbon steel material
mats['CS'] = openmc.Material(name='Carbon Steel')
mats['CS'].temperature = 300
mats['CS'].set_density('g/cc', 7.8)
mats['CS'].add_element('C', 0.00270, 'wo')
mats['CS'].add_element('Mn', 0.00750, 'wo')
mats['CS'].add_element('P', 0.00025, 'wo')
mats['CS'].add_element('S', 0.00025, 'wo')
mats['CS'].add_element('Si', 0.00400, 'wo')
mats['CS'].add_element('Ni', 0.00750, 'wo')
mats['CS'].add_element('Cr', 0.00350, 'wo')
mats['CS'].add_element('Mo', 0.00625, 'wo')
mats['CS'].add_element('V', 0.00050, 'wo')
mats['CS'].add_element('Nb', 0.00010, 'wo')
mats['CS'].add_element('Cu', 0.00200, 'wo')
mats['CS'].add_element('Ca', 0.00015, 'wo')
mats['CS'].add_element('B', 0.00003, 'wo')
mats['CS'].add_element('Ti', 0.00015, 'wo')
mats['CS'].add_element('Al', 0.00025, 'wo')
mats['CS'].add_element('Fe', 0.96487, 'wo')

# Create zircaloy 4 material
mats['Zr'] = openmc.Material(name='Zircaloy-4')
mats['Zr'].temperature = 300
mats['Zr'].set_density('g/cc', 6.55)
mats['Zr'].add_element('O', 0.00125, 'wo')
mats['Zr'].add_element('Cr', 0.0010, 'wo')
mats['Zr'].add_element('Fe', 0.0021, 'wo')
mats['Zr'].add_element('Zr', 0.98115, 'wo')
mats['Zr'].add_element('Sn', 0.0145, 'wo')

# Create Ag-In-Cd control rod material
mats['AIC'] = openmc.Material(name='aic_rod')
mats['AIC'].temperature = 300
mats['AIC'].set_density('g/cc', 10.16)
mats['AIC'].add_element('Ag', 0.80, 'wo')
mats['AIC'].add_element('In', 0.15, 'wo')


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
mats['H2O'] = openmc.Material(name='Borated Water')
mats['H2O'].temperature = 300
mats['H2O'].set_density('g/cc', rho_Bh2o)
mats['H2O'].add_element('B', aB_Bh2o, 'ao')
mats['H2O'].add_element('H', ah_Bh2o, 'ao')
mats['H2O'].add_element('O', aho_Bh2o, 'ao')
mats['H2O'].add_s_alpha_beta(name='lwtr')


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
mats['BSG'] = openmc.Material(name='Borosilicate Glass')
mats['BSG'].temperature = 300
mats['BSG'].set_density('g/cc', 2.26)
mats['BSG'].add_element('O', aO_bsg, 'ao')
mats['BSG'].add_element('Si', aSi_bsg, 'ao')
mats['BSG'].add_element('Al', aAl_bsg, 'ao')
mats['BSG'].add_nuclide('B10', aB10_B, 'ao')
mats['BSG'].add_nuclide('B11', aB11_B, 'ao')


########## Enriched UO2 Fuel #################

# Create 1.6% enriched UO2 fuel material
a_U234, a_U235, a_U238, a_U, a_O = get_fuel_aos(0.0161006)
mats['UO2 1.6'] = openmc.Material(name='1.6\% Enr. UO2 Fuel')
mats['UO2 1.6'].temperature = 300
mats['UO2 1.6'].set_density('g/cc', 10.31341)
mats['UO2 1.6'].add_element('O', a_O, 'ao')
mats['UO2 1.6'].add_element('U', a_U, 'ao', enrichment=0.0161006)

# Create 2.4% enriched UO2 fuel material
a_U234, a_U235, a_U238, a_U, a_O = get_fuel_aos(0.0239993)
mats['UO2 2.4'] = openmc.Material(name='2.4\% Enr. UO2 Fuel')
mats['UO2 2.4'].temperature = 300
mats['UO2 2.4'].set_density('g/cc', 10.29748)
mats['UO2 2.4'].add_element('O', a_O, 'ao')
mats['UO2 2.4'].add_element('U', a_U, 'ao', enrichment=0.0239993)

# Create 3.1% enriched UO2 fuel material
a_U234, a_U235, a_U238, a_U, a_O = get_fuel_aos(0.0310221)
mats['UO2 3.1'] = openmc.Material(name='3.1\% Enr. UO2 Fuel')
mats['UO2 3.1'].temperature = 300
mats['UO2 3.1'].set_density('g/cc', 10.30166)
mats['UO2 3.1'].add_element('O', a_O, 'ao')
mats['UO2 3.1'].add_element('U', a_U, 'ao', enrichment=0.0310221)