#!/usr/bin/env python

"""
PWR OpenMC Model Generator

Allows for tweaking of specifications for the PWR OpenMC model, producing:
  geometry.xml
  materials.xml
  settings.xml
  plot.xml
  tallies.xml

"""

from __future__ import division

from templates2 import *

############## Geometry paramters ##############

def init_data():
  """All model parameters set here

  Materials, surfaces, cells, and lattices are defined here and automatically written
  to the proper files later.  Dictionary keys need to match those in the templates.

  The order each item is written is the order of appearance as written below

  Notes about core construction:
    The entire axial extent for each pincell is constructed in universes, and then added to fuel assembly lattices
    The fuel assembly lattices are then added to one master core lattice


  """


  ################## lattices ##################

  assemblyCells = {} # convenience dictionary holds which cells point to which assembly type

  # commonly needed universes
  gtu = cells['GT empty stack']['univ']
  gti = cells['GT empty stack instr']['univ']
  bas = cells['burn abs stack']['univ']
  ins = cells['GT instr stack']['univ']
  crA = cells['GT CR bank A']['univ']
  crB = cells['GT CR bank B']['univ']
  crC = cells['GT CR bank C']['univ']
  crD = cells['GT CR bank D']['univ']
  crSA = cells['GT CR bank SA']['univ']
  crSB = cells['GT CR bank SB']['univ']
  crSC = cells['GT CR bank SC']['univ']
  crSD = cells['GT CR bank SD']['univ']
  crSE = cells['GT CR bank SE']['univ']

  ################## Main Core Lattices ##################

  latts['Main Core'] =          { 'order':   inc_order(lo),
                                  'comm':    comm_t.format("Main Core Lattice"),
                                  'id':      new_id(univIDs),
                                  'type':    'rectangular',
                                  'dim':     19,
                                  'lleft':   -19*latticePitch/2,
                                  'width':   latticePitch,
                                  'univs':   coreLattice_t.format(
dummy = cells['water pin']['univ'],

G___5 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
H___5 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
J___5 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
F___6 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
G___6 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
H___6 = cells['Fuel 3.1 w/o + 16BA lattice']['univ'],
J___6 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
K___6 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
E___7 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
F___7 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
G___7 = cells['Fuel 3.1 w/o + 16BA lattice']['univ'],
H___7 = cells['Fuel 2.4 w/o + CRD lattice']['univ'],
J___7 = cells['Fuel 3.1 w/o + 16BA lattice']['univ'],
K___7 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
L___7 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
E___8 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
F___8 = cells['Fuel 3.1 w/o + 16BA lattice']['univ'],
G___8 = cells['Fuel 2.4 w/o + CRD lattice']['univ'],
H___8 = cells['Fuel 1.6 w/o + instr lattice']['univ'],
J___8 = cells['Fuel 2.4 w/o + CRD lattice']['univ'],
K___8 = cells['Fuel 3.1 w/o + 16BA lattice']['univ'],
L___8 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
E___9 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
F___9 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
G___9 = cells['Fuel 3.1 w/o + 16BA lattice']['univ'],
H___9 = cells['Fuel 2.4 w/o + CRD lattice']['univ'],
J___9 = cells['Fuel 3.1 w/o + 16BA lattice']['univ'],
K___9 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
L___9 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
F__10 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
G__10 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
H__10 = cells['Fuel 3.1 w/o + 16BA lattice']['univ'],
J__10 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
K__10 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
G__11 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
H__11 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
J__11 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
**baffle)}


  ################## universe 0 cells ##################

  # the axial pincell universes contained in the lattices include the nozzles and bot support plate
  cells['inside core barrel'] ={ 'order':  inc_order(co),
                                'section': comm_t.format("Main universe cells"),
                                'comm':    comm_t.format("inside core barrel"),
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'fill':    latts['Main Core']['id'],
                                'surfs':  '-{0} {1} -{2}'.format(surfs['core barrel IR']['id'],
                                                                 surfs['lower bound']['id'],
                                                                 surfs['upper bound']['id'])}
  cells['core barrel'] =      { 'order':   inc_order(co),
                                'comm':    comm_t.format("core barrel"),
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['SS304']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} {2} -{3}'.format(surfs['core barrel IR']['id'],surfs['core barrel OR']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}
                                                                     
  cells['shield panel NW'] =   { 'order':   inc_order(co),
                                'comm':    comm_t.format("neutron shield panel NW"),
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['SS304']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} {2} -{3} {4} -{5}'.format(surfs['core barrel OR']['id'],surfs['neut shield OR']['id'],
                                                                     surfs['neut shield NWbot SEtop']['id'],surfs['neut shield NWtop SEbot']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}
  cells['shield panel N'] =   { 'order':   inc_order(co),
                                'comm':    "",
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['water-nominal']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} {2} -{3} {4} -{5}'.format(surfs['core barrel OR']['id'],surfs['neut shield OR']['id'],
                                                                     surfs['neut shield NWtop SEbot']['id'],surfs['neut shield NEtop SWbot']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}
  cells['shield panel SE'] = { 'order':   inc_order(co),
                                'comm':    comm_t.format("neutron shield panel SE"),
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['SS304']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} -{2} {3} {4} -{5}'.format(surfs['core barrel OR']['id'],surfs['neut shield OR']['id'],
                                                                     surfs['neut shield NWbot SEtop']['id'],surfs['neut shield NWtop SEbot']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}
  cells['shield panel E'] =   { 'order':   inc_order(co),
                                'comm':    "",
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['water-nominal']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} {2} {3} {4} -{5}'.format(surfs['core barrel OR']['id'],surfs['neut shield OR']['id'],
                                                                     surfs['neut shield NWbot SEtop']['id'],surfs['neut shield NEbot SWtop']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}
  cells['shield panel NE'] =  { 'order':   inc_order(co),
                                'comm':    comm_t.format("neutron shield panel NE"),
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['SS304']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} {2} -{3} {4} -{5}'.format(surfs['core barrel OR']['id'],surfs['neut shield OR']['id'],
                                                                     surfs['neut shield NEbot SWtop']['id'],surfs['neut shield NEtop SWbot']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}
  cells['shield panel S'] =   { 'order':   inc_order(co),
                                'comm':    "",
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['water-nominal']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} -{2} {3} {4} -{5}'.format(surfs['core barrel OR']['id'],surfs['neut shield OR']['id'],
                                                                     surfs['neut shield NWtop SEbot']['id'],surfs['neut shield NEtop SWbot']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}
  cells['shield panel SW'] =  { 'order':   inc_order(co),
                                'comm':    comm_t.format("neutron shield panel SW"),
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['SS304']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} -{2} {3} {4} -{5}'.format(surfs['core barrel OR']['id'],surfs['neut shield OR']['id'],
                                                                     surfs['neut shield NEbot SWtop']['id'],surfs['neut shield NEtop SWbot']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}
  cells['shield panel W'] =   { 'order':   inc_order(co),
                                'comm':    "",
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['water-nominal']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} -{2} -{3} {4} -{5}'.format(surfs['core barrel OR']['id'],surfs['neut shield OR']['id'],
                                                                     surfs['neut shield NWbot SEtop']['id'],surfs['neut shield NEbot SWtop']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}                                                                     
                                                                   
                                                                     
  cells['downcomer'] =        { 'order':   inc_order(co),
                                'comm':    comm_t.format("downcomer"),
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['water-nominal']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} {2} -{3}'.format(surfs['neut shield OR']['id'],surfs['RPV IR']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}
  cells['rpv'] =              { 'order':   inc_order(co),
                                'comm':    comm_t.format("pressure vessel"),
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['carbon steel']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} {2} -{3}'.format(surfs['RPV IR']['id'],surfs['RPV OR']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}

  



  # plot parameters
  plots = {}
  
  colSpecMat = {  mats['water-nominal']['id']: "198 226 255",  # water:  light blue
                  mats['inconel']['id'] : "101 101 101",       # inconel dgray
                  mats['carbon steel']['id'] : "0 0 0",        # carbons black
                  mats['zirc']['id']:  "201 201 201",          # zirc:   gray
                  mats['SS304']['id']:  "0 0 0",               # ss304:  black
                  mats['air']['id']:  "255 255 255",           # air:    white
                  mats['helium']['id']:  "255 218 185",        # helium: light orange
                  mats['borosilicate']['id']: "0 255 0",       # BR:     green
                  mats['control rod']['id']: "255 0 0",        # CR:     bright red
                  mats['UO2 1.6']['id']: "142 35 35",          # 1.6:    light red
                  mats['UO2 2.4']['id']: "255 215 0",          # 2.4:    gold
                  mats['UO2 3.1']['id']: "0 0 128",            # 3.1:    dark blue
               }
  
  plots["row 8 axial"] ={ 'id':     new_id(plotIDs),
                              'fname':  'row_8_mats_axial',
                              'type':   'slice', 
                              'col':    'mat',
                              'background': '255 255 255',
                              'origin': '0.0 0.0 {0}'.format((highestExtent-lowestExtent)/2),
                              'width':  '{0} {0}'.format(highestExtent-lowestExtent),
                              'basis':  'xz',
                              'pixels': '6000 6000',
                              'spec':   colSpecMat,}
  plots["mats J8 ax bot"] = { 'id':     new_id(plotIDs),
                               'fname':  'J8_mats_ax_bot',
                               'type':   'slice', 
                               'col':    'mat',
                               'background': '255 255 255',
                               'origin': '{x} {y} {z}'.format(x=0.0,y=latticePitch,z=topLowerNozzle),
                               'width':  '{x} {z}'.format(x=latticePitch,z=2.1*(topLowerNozzle-bottomSupportPlate)),
                               'basis':  'xz',
                               'pixels': '{x} {z}'.format(x=4000,z=int(4000*2.1*(topLowerNozzle-bottomSupportPlate)/latticePitch)),
                               'spec':   colSpecMat,}
  plots["mats J8 ax top"] = { 'id':     new_id(plotIDs),
                               'fname':  'J8_mats_ax_top',
                               'type':   'slice', 
                               'col':    'mat',
                               'background': '255 255 255',
                               'origin': '{x} {y} {z}'.format(x=0.0,y=latticePitch,z=topFuelRod),
                               'width':  '{x} {z}'.format(x=latticePitch,z=2.1*(topUpperNozzle - topFuelRod)),
                               'basis':  'xz',
                               'pixels': '{x} {z}'.format(x=4000,z=int(4000*2.1*(topLowerNozzle-bottomSupportPlate)/latticePitch)),
                               'spec':   colSpecMat,}
  plots["mats J8 nozzle"] = { 'id':     new_id(plotIDs),
                               'fname':  'J8_mats_nozzle',
                               'type':   'slice',
                               'col':    'mat',
                               'background': '255 255 255',
                               'origin': '{x} {y} {z}'.format(x=0.0,y=latticePitch,z=bottomSupportPlate+2.0),
                               'width':  '{x} {y}'.format(x=latticePitch,y=latticePitch),
                               'basis':  'xy',
                               'pixels': '{x} {y}'.format(x=4000,y=4000),
                               'spec':   colSpecMat,}
  plots["mats H8 ax top"] = { 'id':     new_id(plotIDs),
                               'fname':  'H8_mats_ax_top',
                               'type':   'slice', 
                               'col':    'mat',
                               'background': '255 255 255',
                               'origin': '{x} {y} {z}'.format(x=0.0,y=0.0,z=topFuelRod),
                               'width':  '{x} {z}'.format(x=latticePitch,z=5*(topUpperNozzle - topFuelRod)),
                               'basis':  'xz',
                               'pixels': '{x} {z}'.format(x=4000,z=int(4000*2.1*(topLowerNozzle-bottomSupportPlate)/latticePitch)),
                               'spec':   colSpecMat,}


  # settings parameters
  entrX = 15*17
  entrY = 15*17
  entrZ = 100
  xbot = -8*latticePitch/2
  ybot = -8*latticePitch/2
  zbot = bottomFuelStack
  xtop = 8*latticePitch/2
  ytop = 8*latticePitch/2
  ztop = topActiveCore
  if core_D == '2-D':
    entrZ = 1
    zbot = twoDlower
    ztop = twoDhigher 
  sett = { 
            'xslib':        '/home/shared/mcnpdata/binary/cross_sections.xml',
#            'xslib':        '/home/nhorelik/xsdata/cross_sections.xml',
            'batches':      350,
            'inactive':     250,
            'particles':    int(4e4),
            'verbosity':    7,
            'entrX':        entrX, 
            'entrY':        entrY,
            'entrZ':        entrZ,
            'xbot':   xbot, 'ybot':  ybot, 'zbot': zbot,
            'xtop':   xtop, 'ytop':  ytop, 'ztop': ztop}



  tallies = {}

  meshDim = 15*17
  meshLleft = -15*latticePitch/2
  tallies['testmesh'] = {'ttype': 'mesh',
                      'id': 1,
                      'type': 'rectangular',
                      'origin': '0.0 0.0',
                      'width': '{0} {0}'.format(-meshLleft*2/meshDim),
                      'lleft': '{0} {0}'.format(meshLleft),
                      'dimension': '{0} {0}'.format(meshDim)}
  tallies['test'] = { 'ttype': 'tally',
                      'id': 1,
                      'mesh':tallies['testmesh']['id'],
                      'scores':'nu-fission'}

  return mats,surfs,cells,latts,sett,plots,tallies


def main():

  mats,surfs,cells,latts,sett,plots,tallies,cmfd = init_data()

  write_materials(mats,"materials.xml")
  write_geometry(surfs,cells,latts,"geometry.xml")
  write_settings(sett,"settings.xml")
  write_plots(plots,"plots.xml")
  write_tallies(tallies,"tallies.xml")
  write_cmfd(cmfd,"cmfd.xml")


if __name__ == "__main__":
  main()
