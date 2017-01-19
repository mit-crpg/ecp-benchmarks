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

############## Material paramters ##############

h2oDens = 0.73986
nominalBoronPPM = 975

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


  ################## materials ##################

  mo = {'n': 0}
  mats = {}

  from boron_ppm import Water

  h2o = Water()

  borwatmats = h2o.get_water_mats(h2oDens,nominalBoronPPM)

  ################## cells ##################

  # (if not a fill cell, set 'fill': None.  if not None, 'mat' is ignored)

  co = {'n': 0}
  cells = {}
  cells['water pin'] =          { 'order':   inc_order(co),
                                  'section': comm_t.format("Empty water pincell universe"),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'mat':     mats['water-nominal']['id'],
                                  'fill':    None,
                                  'surfs':  '-{0}'.format(surfs['dummy outer']['id'])}
  cells['water pin 2'] =        { 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    cells['water pin']['univ'],
                                  'mat':     mats['water-nominal']['id'],
                                  'fill':    None,
                                  'surfs':  '{0}'.format(surfs['dummy outer']['id'])}

  # GUIDE TUBE PIN CELLS
  
  
  make_pin('GT empty',"Guide tube pincell universes",co,cells,new_id(univIDs),cellIDs,
            [surfs['guide tube IR']['id'],
             surfs['guide tube OR']['id']],
            [(mats['water-nominal']['id'],"empty guide tube"),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),])
  make_pin('GT empty grid_tb',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['guide tube IR']['id'],
             surfs['guide tube OR']['id'],],
            [(mats['water-nominal']['id'],"empty guide tube with top/bottom grid"),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),],
            grid=True, surfs=surfs, gridMat=mats['inconel']['id'], gridType='tb')
  make_pin('GT empty grid_i',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['guide tube IR']['id'],
             surfs['guide tube OR']['id'],],
            [(mats['water-nominal']['id'],"empty guide tube with intermediate grid"),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),],
            grid=True, surfs=surfs, gridMat=mats['zirc']['id'], gridType='i')
  make_pin('GT empty nozzle',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['guide tube IR']['id'],
             surfs['guide tube OR']['id'],],
            [(mats['water-nominal']['id'],"empty guide tube SS304 penetration"),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),])
  make_pin('GTd empty',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['GT dashpot IR']['id'],
             surfs['GT dashpot OR']['id'],],
            [(mats['water-nominal']['id'],"empty guide tube at dashpot"),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),])
  make_pin('GTd empty grid_tb',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['GT dashpot IR']['id'],
             surfs['GT dashpot OR']['id'],],
            [(mats['water-nominal']['id'],"empty guide tube at dashpot with top/bottom grid"),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),],
            grid=True, surfs=surfs, gridMat=mats['inconel']['id'], gridType='tb')
  make_pin('GTd empty grid_i',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['GT dashpot IR']['id'],
             surfs['GT dashpot OR']['id'],],
            [(mats['water-nominal']['id'],"empty guide tube at dashpot with intermediate grid"),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),],
            grid=True, surfs=surfs, gridMat=mats['zirc']['id'], gridType='i')
  make_pin('GTd empty nozzle',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['GT dashpot IR']['id'],
             surfs['GT dashpot OR']['id'],],
            [(mats['water-nominal']['id'],"empty GTd SS304 penetration"),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),])


  # final combination of all axial pieces for empty guide tube
  stackSurfs = [surfs['bot support plate']['id'],
                surfs['top support plate']['id'],
                surfs['top lower nozzle']['id'],
                surfs['top lower thimble']['id'],
                surfs['grid1bot']['id'],
                surfs['grid1top']['id'],
                surfs['dashpot top']['id'],
                surfs['grid2bot']['id'],
                surfs['grid2top']['id'],
                surfs['grid3bot']['id'],
                surfs['grid3top']['id'],
                surfs['grid4bot']['id'],
                surfs['grid4top']['id'],
        #        surfs['grid5bot']['id'],
        #        surfs['grid5top']['id'],
        #        surfs['grid6bot']['id'],
        #        surfs['grid6top']['id'],
        #        surfs['grid7bot']['id'],
        #        surfs['grid7top']['id'],
                surfs['top active core']['id'],
        #        surfs['grid8bot']['id'],
        #        surfs['grid8top']['id'],
                surfs['top pin plenum']['id'],
                surfs['top fuel rod']['id'],
                surfs['bot upper nozzle']['id'],
                surfs['top upper nozzle']['id']]
  make_stack('GT empty stack',co,cells,new_id(univIDs),cellIDs,
            stackSurfs,
            [cells['water pin']['univ'],          # lower plenum
#            cells['GTd empty nozzle']['univ'],   # support plate
#            cells['GTd empty nozzle']['univ'],   # lower nozzle 
             cells['water pin']['univ'],          # support plate
             cells['water pin']['univ'],          # lower nozzle
             cells['GTd empty']['univ'],          # lower thimble
             cells['GTd empty']['univ'],          # dashpot
             cells['GTd empty grid_tb']['univ'],  # dashpot grid 1
             cells['GTd empty']['univ'],          # dashpot
             cells['GT empty']['univ'],           # reg
             cells['GT empty grid_i']['univ'],    # reg grid 2
             cells['GT empty']['univ'],           # reg
             cells['GT empty grid_i']['univ'],    # reg grid 3
             cells['GT empty']['univ'],           # reg
#             cells['GT empty grid_i']['univ'],    # reg grid 4
#             cells['GT empty']['univ'],           # reg
#             cells['GT empty grid_i']['univ'],    # reg grid 5
#             cells['GT empty']['univ'],           # reg
#             cells['GT empty grid_i']['univ'],    # reg grid 6
#             cells['GT empty']['univ'],           # reg
#             cells['GT empty grid_i']['univ'],    # reg grid 7
#             cells['GT empty']['univ'],           # reg
             cells['GT empty']['univ'],           # pin plenum
             cells['GT empty grid_tb']['univ'],   # pin plenum grid 8
             cells['GT empty']['univ'],           # pin plenum
             cells['GT empty']['univ'],           # upper fuel rod end plug
             cells['GT empty']['univ'],           # space between fuel rod and and upper nozzle
#            cells['GT empty nozzle']['univ'],    # upper nozzle
             cells['water pin']['univ'],          # upper nozzle
             cells['water pin']['univ']])         # upper plenum
  make_stack('GT empty stack instr',co,cells,new_id(univIDs),cellIDs,
            stackSurfs,
            [cells['water pin']['univ'],          # lower plenum
#            cells['GT empty nozzle']['univ'],   # support plate
#            cells['GT empty nozzle']['univ'],   # lower nozzle
             cells['water pin']['univ'],          # support plate
             cells['water pin']['univ'],          # lower nozzle
             cells['GT empty']['univ'],          # lower thimble
             cells['GT empty']['univ'],          # dashpot
             cells['GT empty grid_tb']['univ'],     # dashpot grid 1
             cells['GT empty']['univ'],          # dashpot
             cells['GT empty']['univ'],           # reg
             cells['GT empty grid_i']['univ'],      # reg grid 2
             cells['GT empty']['univ'],           # reg
             cells['GT empty grid_i']['univ'],      # reg grid 3
             cells['GT empty']['univ'],           # reg
#             cells['GT empty grid_i']['univ'],      # reg grid 4
#             cells['GT empty']['univ'],           # reg
#             cells['GT empty grid_i']['univ'],      # reg grid 5
#             cells['GT empty']['univ'],           # reg
#             cells['GT empty grid_i']['univ'],      # reg grid 6
#             cells['GT empty']['univ'],           # reg
#             cells['GT empty grid_i']['univ'],      # reg grid 7
#             cells['GT empty']['univ'],           # reg
             cells['GT empty']['univ'],           # pin plenum
             cells['GT empty grid_tb']['univ'],      # pin plenum grid 8
             cells['GT empty']['univ'],           # pin plenum
             cells['GT empty']['univ'],           # upper fuel rod end plug
             cells['GT empty']['univ'],           # space between fuel rod and and upper nozzle
             cells['water pin']['univ'],          # upper nozzle
#            cells['GT empty nozzle']['univ'],    # upper nozzle
             cells['water pin']['univ']])         # upper plenum

  # INSTRUMENT TUBE PIN CELL

  make_pin('GT instr',"Instrument tube pincell universes",co,cells,new_id(univIDs),cellIDs,
            [surfs['instr tube IR']['id'],
             surfs['instr tube OR']['id'],
             surfs['guide tube IR']['id'],
             surfs['guide tube OR']['id']],
            [(mats['air']['id'],"instr guide tube above dashpot"),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),])
  make_pin('GT instr grid_tb',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['instr tube IR']['id'],
             surfs['instr tube OR']['id'],
             surfs['guide tube IR']['id'],
             surfs['guide tube OR']['id'],],
            [(mats['air']['id'],"instr guide tube at dashpot with top/bottom grid"),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),],
            grid=True, surfs=surfs, gridMat=mats['inconel']['id'], gridType='tb')
  make_pin('GT instr grid_i',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['instr tube IR']['id'],
             surfs['instr tube OR']['id'],
             surfs['guide tube IR']['id'],
             surfs['guide tube OR']['id'],],
            [(mats['air']['id'],"instr guide tube at dashpot with intermediate grid"),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),],
            grid=True, surfs=surfs, gridMat=mats['zirc']['id'], gridType='i')
  make_pin('GT instr nozzle',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['instr tube IR']['id'],
             surfs['instr tube OR']['id'],
             surfs['guide tube IR']['id'],
             surfs['guide tube OR']['id'],],
            [(mats['air']['id'],"instr guide tube SS304 penetration"),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),
             (mats['zirc']['id'],""),
             (mats['SS304']['id'],""),])
  make_pin('bare instr',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['instr tube IR']['id'],
             surfs['instr tube OR']['id'],],
            [(mats['air']['id'],"instr guide tube at dashpot"),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),])


  # final combination of all axial pieces for instrument tube
  make_stack('GT instr stack',co,cells,new_id(univIDs),cellIDs,
            stackSurfs,
            [cells['bare instr']['univ'],        # lower plenum
#            cells['GT instr nozzle']['univ'],   # support plate
#            cells['GT instr nozzle']['univ'],   # lower nozzle
             cells['bare instr']['univ'],        # support plate
             cells['bare instr']['univ'],        # lower nozzle
             cells['GT instr']['univ'],          # lower thimble
             cells['GT instr']['univ'],          # dashpot
             cells['GT instr grid_tb']['univ'],  # dashpot grid 1
             cells['GT instr']['univ'],          # dashpot
             cells['GT instr']['univ'],          # reg
             cells['GT instr grid_i']['univ'],   # reg grid 2
             cells['GT instr']['univ'],          # reg
             cells['GT instr grid_i']['univ'],   # reg grid 3
             cells['GT instr']['univ'],          # reg
#             cells['GT instr grid_i']['univ'],   # reg grid 4
#             cells['GT instr']['univ'],          # reg
#             cells['GT instr grid_i']['univ'],   # reg grid 5
#             cells['GT instr']['univ'],          # reg
#             cells['GT instr grid_i']['univ'],   # reg grid 6
#             cells['GT instr']['univ'],          # reg
#             cells['GT instr grid_i']['univ'],   # reg grid 7
#             cells['GT instr']['univ'],          # reg
             cells['GT instr']['univ'],          # pin plenum
             cells['GT instr grid_tb']['univ'],  # pin plenum grid 8
             cells['GT instr']['univ'],          # pin plenum
             cells['GT instr']['univ'],          # upper fuel rod end plug
             cells['GT instr']['univ'],          # space between fuel rod and and upper nozzle
#            cells['GT instr nozzle']['univ'],   # upper nozzle
             cells['bare instr']['univ'],        # upper nozzle
             cells['water pin']['univ']])         # upper plenum


  # CONTROL ROD PIN CELLS

  make_pin('control rod',"Control rod bank pincell universes",co,cells,new_id(univIDs),cellIDs,
            [surfs['control poison OR']['id'],
             surfs['control rod IR']['id'],
             surfs['control rod OR']['id'],
             surfs['guide tube IR']['id'],
             surfs['guide tube OR']['id'],],
            [(mats['control rod']['id'],"guide tube above dashpot with control rod"),
             (mats['air']['id'],""),
             (mats['SS304']['id'],""),
             (mats['water-nominal']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),])
  make_pin('control rod grid_tb',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['control poison OR']['id'],
             surfs['control rod IR']['id'],
             surfs['control rod OR']['id'],
             surfs['guide tube IR']['id'],
             surfs['guide tube OR']['id'],],
            [(mats['control rod']['id'],"guide tube above dashpot with control rod, with top/bottom grid"),
             (mats['air']['id'],""),
             (mats['SS304']['id'],""),
             (mats['water-nominal']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),],
            grid=True, surfs=surfs, gridMat=mats['inconel']['id'], gridType='tb')
  make_pin('control rod grid_i',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['control poison OR']['id'],
             surfs['control rod IR']['id'],
             surfs['control rod OR']['id'],
             surfs['guide tube IR']['id'],
             surfs['guide tube OR']['id'],],
            [(mats['control rod']['id'],"guide tube above dashpot with control rod, with intermediate grid"),
             (mats['air']['id'],""),
             (mats['SS304']['id'],""),
             (mats['water-nominal']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),],
            grid=True, surfs=surfs, gridMat=mats['zirc']['id'], gridType='i')
  make_pin('control rod nozzle',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['control poison OR']['id'],
             surfs['control rod IR']['id'],
             surfs['control rod OR']['id'],],
            [(mats['control rod']['id'],"guide tube above dashpot with control rod, with nozzle"),
             (mats['air']['id'],""),
             (mats['SS304']['id'],""),
             (mats['water-nominal']['id'],""),])
  make_pin('control rod blank',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['control poison OR']['id'],
             surfs['control rod IR']['id'],
             surfs['control rod OR']['id'],
             surfs['guide tube IR']['id'],
             surfs['guide tube OR']['id'],],
            [(mats['SS304']['id'],"blank control rod above active region, above nozzle"),
             (mats['air']['id'],""),
             (mats['SS304']['id'],""),
             (mats['water-nominal']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),])
  make_pin('control rod blank grid_tb',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['control poison OR']['id'],
             surfs['control rod IR']['id'],
             surfs['control rod OR']['id'],
             surfs['guide tube IR']['id'],
             surfs['guide tube OR']['id'],],
            [(mats['SS304']['id'],"guide tube above dashpot with blank control rod, with top/bottom grid"),
             (mats['air']['id'],""),
             (mats['SS304']['id'],""),
             (mats['water-nominal']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),],
            grid=True, surfs=surfs, gridMat=mats['inconel']['id'], gridType='tb')
  make_pin('control rod blank grid_i',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['control poison OR']['id'],
             surfs['control rod IR']['id'],
             surfs['control rod OR']['id'],
             surfs['guide tube IR']['id'],
             surfs['guide tube OR']['id'],],
            [(mats['SS304']['id'],"guide tube above dashpot with blank control rod, with intermediate grid"),
             (mats['air']['id'],""),
             (mats['SS304']['id'],""),
             (mats['water-nominal']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),],
            grid=True, surfs=surfs, gridMat=mats['zirc']['id'], gridType='i')
  make_pin('control rod blank nozzle',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['control poison OR']['id'],
             surfs['control rod IR']['id'],
             surfs['control rod OR']['id'],],
            [(mats['SS304']['id'],"blank control rod above active region, within nozzle"),
             (mats['air']['id'],""),
             (mats['SS304']['id'],""),
             (mats['water-nominal']['id'],""),])
  make_pin('control rod blank bare',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['control poison OR']['id'],
             surfs['control rod IR']['id'],
             surfs['control rod OR']['id'],],
            [(mats['SS304']['id'],"blank control rod above active region, within nozzle"),
             (mats['air']['id'],""),
             (mats['SS304']['id'],""),
             (mats['water-nominal']['id'],""),])
  make_pin('control rod bare',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['control poison OR']['id'],
             surfs['control rod IR']['id'],
             surfs['control rod OR']['id'],],
            [(mats['control rod']['id'],"guide tube above dashpot with control rod"),
             (mats['air']['id'],""),
             (mats['SS304']['id'],""),
             (mats['water-nominal']['id'],""),])


  # for the control rods, we make the axial universe three times, once with the
  # grid everywhere, once without, and once with the nozzle everywhere. Then
  # we can alternate with them as appropriate in the final axial stack

  banks = ['A','B','C','D','SA','SB','SC','SD','SE']
  
  for b in banks:

    # no grid, no nozzle
    make_stack('dummy GT CR bank {0}'.format(b),co,cells,new_id(univIDs),cellIDs,
                [surfs['bot fuel rod']['id'],
                 surfs['dashpot top']['id'],
                 surfs['bank{0} bot'.format(b)]['id'],
                 surfs['bank{0} top'.format(b)]['id'],],
                [cells['water pin']['univ'],
                 cells['GTd empty']['univ'],
                 cells['GT empty']['univ'],
                 cells['control rod']['univ'],
                 cells['control rod blank']['univ'],])
                 
    # top/bottom grid
    make_stack('dummy GT CR bank {0} grid_tb'.format(b),co,cells,new_id(univIDs),cellIDs,
                [surfs['bot fuel rod']['id'],
                 surfs['dashpot top']['id'],
                 surfs['bank{0} bot'.format(b)]['id'],
                 surfs['bank{0} top'.format(b)]['id'],],
                [cells['water pin']['univ'],
                 cells['GTd empty grid_tb']['univ'],
                 cells['GT empty grid_tb']['univ'],
                 cells['control rod grid_tb']['univ'],
                 cells['control rod blank grid_tb']['univ'],])

    # intermediate grid
    make_stack('dummy GT CR bank {0} grid_i'.format(b),co,cells,new_id(univIDs),cellIDs,
                [surfs['bot fuel rod']['id'],
                 surfs['dashpot top']['id'],
                 surfs['bank{0} bot'.format(b)]['id'],
                 surfs['bank{0} top'.format(b)]['id'],],
                [cells['water pin']['univ'],
                 cells['GTd empty grid_i']['univ'],
                 cells['GT empty grid_i']['univ'],
                 cells['control rod grid_i']['univ'],
                 cells['control rod blank grid_i']['univ'],])
    
    # nozzle
    make_stack('dummy GT CR bank {0} nozzle'.format(b),co,cells,new_id(univIDs),cellIDs,
                [surfs['bot fuel rod']['id'],
                 surfs['dashpot top']['id'],
                 surfs['bank{0} bot'.format(b)]['id'],
                 surfs['bank{0} top'.format(b)]['id'],],
                [cells['water pin']['univ'],
                 cells['GTd empty nozzle']['univ'],
                 cells['GT empty nozzle']['univ'],
                 cells['control rod nozzle']['univ'],
                 cells['control rod blank nozzle']['univ'],])

    # bare 
    make_stack('dummy GT CR bank {0} bare'.format(b),co,cells,new_id(univIDs),cellIDs,
                [surfs['bot fuel rod']['id'],
                 surfs['dashpot top']['id'],
                 surfs['bank{0} bot'.format(b)]['id'],
                 surfs['bank{0} top'.format(b)]['id'],],
                [cells['water pin']['univ'],
                 cells['GTd empty nozzle']['univ'],
                 cells['GT empty nozzle']['univ'],
                 cells['control rod bare']['univ'],
                 cells['control rod blank bare']['univ'],])

    # final combination of all axial pieces for control rod bank b
    make_stack('GT CR bank {0}'.format(b),co,cells,new_id(univIDs),cellIDs,
              stackSurfs,
              [cells['water pin']['univ'],                          # lower plenum
               cells['dummy GT CR bank {0} nozzle'.format(b)]['univ'],    # support plate
               cells['dummy GT CR bank {0} nozzle'.format(b)]['univ'],    # lower nozzle
               cells['dummy GT CR bank {0}'.format(b)]['univ'],           # lower thimble
               cells['dummy GT CR bank {0}'.format(b)]['univ'],           # dashpot
               cells['dummy GT CR bank {0} grid_tb'.format(b)]['univ'],      # dashpot grid 1
               cells['dummy GT CR bank {0}'.format(b)]['univ'],           # dashpot
               cells['dummy GT CR bank {0}'.format(b)]['univ'],           # reg
               cells['dummy GT CR bank {0} grid_i'.format(b)]['univ'],      # reg grid 2
               cells['dummy GT CR bank {0}'.format(b)]['univ'],           # reg
               cells['dummy GT CR bank {0} grid_i'.format(b)]['univ'],      # reg grid 3
               cells['dummy GT CR bank {0}'.format(b)]['univ'],           # reg
#               cells['dummy GT CR bank {0} grid_i'.format(b)]['univ'],      # reg grid 4
#               cells['dummy GT CR bank {0}'.format(b)]['univ'],           # reg
#               cells['dummy GT CR bank {0} grid_i'.format(b)]['univ'],      # reg grid 5
#               cells['dummy GT CR bank {0}'.format(b)]['univ'],           # reg
#               cells['dummy GT CR bank {0} grid_i'.format(b)]['univ'],      # reg grid 6
#               cells['dummy GT CR bank {0}'.format(b)]['univ'],           # reg
#               cells['dummy GT CR bank {0} grid_i'.format(b)]['univ'],      # reg grid 7
#               cells['dummy GT CR bank {0}'.format(b)]['univ'],           # reg
               cells['dummy GT CR bank {0}'.format(b)]['univ'],           # pin plenum
               cells['dummy GT CR bank {0} grid_tb'.format(b)]['univ'],      # pin plenum grid 8
               cells['dummy GT CR bank {0}'.format(b)]['univ'],           # pin plenum
               cells['dummy GT CR bank {0}'.format(b)]['univ'],           # upper fuel rod end plug
               cells['dummy GT CR bank {0}'.format(b)]['univ'],           # space between fuel rod and and upper nozzle
#               cells['dummy GT CR bank {0} nozzle'.format(b)]['univ'],    # upper nozzle
               cells['dummy GT CR bank {0} bare'.format(b)]['univ'],    # upper nozzle
               cells['dummy GT CR bank {0} bare'.format(b)]['univ']])                       # upper plenum
  

  # BURNABLE ABSORBER PIN CELLS

  # These suckers don't go all the way down to the bottom of the fuel rods, but
  # they do extend into the dashpot, ending in the middle of grid 1.

  make_pin('burn abs',"Burnable absorber pincell universes",co,cells,new_id(univIDs),cellIDs,
            [surfs['burnabs rad 1']['id'],
             surfs['burnabs rad 2']['id'],
             surfs['burnabs rad 3']['id'],
             surfs['burnabs rad 4']['id'],
             surfs['burnabs rad 5']['id'],
             surfs['burnabs rad 6']['id'],
             surfs['burnabs rad 7']['id'],
             surfs['burnabs rad 8']['id'],],
            [(mats['air']['id'],"burnable absorber pin"),
             (mats['SS304']['id'],""),
             (mats['air']['id'],""),
             (mats['borosilicate']['id'],""),
             (mats['air']['id'],""),
             (mats['SS304']['id'],""),
             (mats['water-nominal']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),])
  make_pin('burn abs grid_tb',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['burnabs rad 1']['id'],
             surfs['burnabs rad 2']['id'],
             surfs['burnabs rad 3']['id'],
             surfs['burnabs rad 4']['id'],
             surfs['burnabs rad 5']['id'],
             surfs['burnabs rad 6']['id'],
             surfs['burnabs rad 7']['id'],
             surfs['burnabs rad 8']['id'],],
            [(mats['air']['id'],"burnable absorber pin top/bottom grid"),
             (mats['SS304']['id'],""),
             (mats['air']['id'],""),
             (mats['borosilicate']['id'],""),
             (mats['air']['id'],""),
             (mats['SS304']['id'],""),
             (mats['water-nominal']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),],
            grid=True, surfs=surfs, gridMat=mats['inconel']['id'], gridType='tb')
  make_pin('burn abs grid_i',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['burnabs rad 1']['id'],
             surfs['burnabs rad 2']['id'],
             surfs['burnabs rad 3']['id'],
             surfs['burnabs rad 4']['id'],
             surfs['burnabs rad 5']['id'],
             surfs['burnabs rad 6']['id'],
             surfs['burnabs rad 7']['id'],
             surfs['burnabs rad 8']['id'],],
            [(mats['air']['id'],"burnable absorber pin intermediate grid"),
             (mats['SS304']['id'],""),
             (mats['air']['id'],""),
             (mats['borosilicate']['id'],""),
             (mats['air']['id'],""),
             (mats['SS304']['id'],""),
             (mats['water-nominal']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),],
            grid=True, surfs=surfs, gridMat=mats['zirc']['id'], gridType='i')
  make_pin('burn abs dashpot',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['burnabs rad 1']['id'],
             surfs['burnabs rad 2']['id'],
             surfs['burnabs rad 3']['id'],
             surfs['burnabs rad 4']['id'],
             surfs['burnabs rad 5']['id'],
             surfs['burnabs rad 6']['id'],
             surfs['GT dashpot IR']['id'],
             surfs['GT dashpot OR']['id'],],
            [(mats['air']['id'],"burnable absorber pin dashpot"),
             (mats['SS304']['id'],""),
             (mats['air']['id'],""),
             (mats['borosilicate']['id'],""),
             (mats['air']['id'],""),
             (mats['SS304']['id'],""),
             (mats['water-nominal']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),])
  make_pin('burn abs dashpot grid_tb',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['burnabs rad 1']['id'],
             surfs['burnabs rad 2']['id'],
             surfs['burnabs rad 3']['id'],
             surfs['burnabs rad 4']['id'],
             surfs['burnabs rad 5']['id'],
             surfs['burnabs rad 6']['id'],
             surfs['GT dashpot IR']['id'],
             surfs['GT dashpot OR']['id'],],
            [(mats['air']['id'],"burnable absorber pin dashpot top/bottomgrid"),
             (mats['SS304']['id'],""),
             (mats['air']['id'],""),
             (mats['borosilicate']['id'],""),
             (mats['air']['id'],""),
             (mats['SS304']['id'],""),
             (mats['water-nominal']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),],
            grid=True, surfs=surfs, gridMat=mats['inconel']['id'], gridType='tb')
  make_pin('burn abs dashpot grid_i',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['burnabs rad 1']['id'],
             surfs['burnabs rad 2']['id'],
             surfs['burnabs rad 3']['id'],
             surfs['burnabs rad 4']['id'],
             surfs['burnabs rad 5']['id'],
             surfs['burnabs rad 6']['id'],
             surfs['GT dashpot IR']['id'],
             surfs['GT dashpot OR']['id'],],
            [(mats['air']['id'],"burnable absorber pin dashpot intermediate grid"),
             (mats['SS304']['id'],""),
             (mats['air']['id'],""),
             (mats['borosilicate']['id'],""),
             (mats['air']['id'],""),
             (mats['SS304']['id'],""),
             (mats['water-nominal']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),],
            grid=True, surfs=surfs, gridMat=mats['zirc']['id'], gridType='i')
  make_pin('blank burn abs ss',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['burnabs rad 6']['id'],
             surfs['burnabs rad 7']['id'],
             surfs['burnabs rad 8']['id']],
            [(mats['SS304']['id'],"blank burnable absorber pin above active poison, inside guide tube"),
             (mats['water-nominal']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),])
  make_pin('blank burn abs ss bare',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['burnabs rad 6']['id']],
            [(mats['SS304']['id'],"blank burnable absorber pin above active poison, inside nozzle"),
             (mats['water-nominal']['id'],""),])

  # final combination of all axial pieces burnable absorber rod
  stackSurfsBA = [surfs['bot support plate']['id'],
                  surfs['top support plate']['id'],
                  surfs['top lower nozzle']['id'],
                  surfs['top lower thimble']['id'],
                  surfs['grid1bot']['id'],
                  surfs['burn abs bot']['id'],
                  surfs['grid1top']['id'],
                  surfs['dashpot top']['id'],
                  surfs['grid2bot']['id'],
                  surfs['grid2top']['id'],
                  surfs['grid3bot']['id'],
                  surfs['grid3top']['id'],
                  surfs['top active core']['id'],
                  surfs['grid4bot']['id'],
                  surfs['grid4top']['id'],
         #         surfs['grid5bot']['id'],
         #         surfs['grid5top']['id'],
         #         surfs['grid6bot']['id'],
         #         surfs['grid6top']['id'],
         #         surfs['grid7bot']['id'],
         #         surfs['grid7top']['id'],
         #         surfs['top active core']['id'],
         #         surfs['grid8bot']['id'],
         #         surfs['grid8top']['id'],
                  surfs['top pin plenum']['id'],
                  surfs['top fuel rod']['id'],
                  surfs['bot upper nozzle']['id'],
                  surfs['top upper nozzle']['id']]
                
  make_stack('burn abs stack',co,cells,new_id(univIDs),cellIDs,
            stackSurfsBA,
            [cells['water pin']['univ'],          # lower plenum
             cells['water pin']['univ'],   # support plate
             cells['water pin']['univ'],   # lower nozzle
             cells['GTd empty']['univ'],          # lower thimble
             cells['GTd empty']['univ'],          # dashpot
             cells['GTd empty grid_tb']['univ'],     # dashpot grid 1
             cells['burn abs dashpot grid_tb']['univ'],     # dashpot grid 1
             cells['burn abs dashpot']['univ'],          # dashpot
             cells['burn abs']['univ'],           # reg
             cells['burn abs grid_i']['univ'],      # reg grid 2
             cells['burn abs']['univ'],           # reg
             cells['burn abs grid_i']['univ'],      # reg grid 3
             cells['burn abs']['univ'],           # reg
#             cells['burn abs grid_i']['univ'],      # reg grid 4
#             cells['burn abs']['univ'],           # reg
#             cells['burn abs grid_i']['univ'],      # reg grid 5
#             cells['burn abs']['univ'],           # reg
#             cells['burn abs grid_i']['univ'],      # reg grid 6
#             cells['burn abs']['univ'],           # reg
#             cells['burn abs grid_i']['univ'],      # reg grid 7
#             cells['burn abs']['univ'],           # reg
             cells['blank burn abs ss']['univ'],           # pin plenum
             cells['blank burn abs ss']['univ'],      # pin plenum grid 8
             cells['blank burn abs ss']['univ'],           # pin plenum
             cells['blank burn abs ss']['univ'],           # upper fuel rod end plug
             cells['blank burn abs ss']['univ'],         # space between fuel rod and and upper nozzle
             cells['blank burn abs ss bare']['univ'],         # upper nozzle
             cells['water pin']['univ']])        # upper plenum


  # FUEL PIN CELLS
  
  make_pin('SS pin',"Fuel pincells",co,cells,new_id(univIDs),cellIDs,
            [surfs['clad OR']['id'],],
            [(mats['SS304']['id'],"SS pin for lower thimble and SS penetrations"),
             (mats['water-nominal']['id'],""),])
  make_pin('end plug',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['clad OR']['id'],],
            [(mats['zirc']['id'],"end plug"),
             (mats['water-nominal']['id'],""),])
  make_pin('pin plenum',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['plenum spring OR']['id'],
             surfs['clad IR']['id'],
             surfs['clad OR']['id'],],
            [(mats['inconel']['id'],"pin plenum"),
             (mats['helium']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),])
  make_pin('pin plenum grid_tb',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['plenum spring OR']['id'],
             surfs['clad IR']['id'],
             surfs['clad OR']['id'],],
            [(mats['inconel']['id'],"pin plenum"),
             (mats['helium']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),],
            grid=True, surfs=surfs, gridMat=mats['inconel']['id'], gridType='tb')


  ## 1.6 w/o
  
  make_pin('Fuel 1.6 w/o',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['pellet OR']['id'],
             surfs['clad IR']['id'],
             surfs['clad OR']['id'],],
            [(mats['UO2 1.6']['id'],"UO2 Fuel 1.6 w/o"),
             (mats['helium']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),])
  make_pin('Fuel 1.6 w/o grid_tb',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['pellet OR']['id'],
             surfs['clad IR']['id'],
             surfs['clad OR']['id'],],
            [(mats['UO2 1.6']['id'],"UO2 Fuel 1.6 w/o with top/bottom grid"),
             (mats['helium']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),],
            grid=True, surfs=surfs, gridMat=mats['inconel']['id'], gridType='tb')
  make_pin('Fuel 1.6 w/o grid_i',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['pellet OR']['id'],
             surfs['clad IR']['id'],
             surfs['clad OR']['id'],],
            [(mats['UO2 1.6']['id'],"UO2 Fuel 1.6 w/o with intermediate grid"),
             (mats['helium']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),],
            grid=True, surfs=surfs, gridMat=mats['zirc']['id'], gridType='i')

  # final combination of all axial pieces for Fuel 1.6 w/o
  make_stack('Fuel 1.6 w/o stack',co,cells,new_id(univIDs),cellIDs,
            stackSurfs,
            [cells['water pin']['univ'],              # lower plenum
             cells['SS pin']['univ'],                 # support plate
             cells['SS pin']['univ'],                 # lower nozzle
             cells['end plug']['univ'],               # lower thimble
             cells['Fuel 1.6 w/o']['univ'],           # dashpot
             cells['Fuel 1.6 w/o grid_tb']['univ'],      # dashpot grid 1
             cells['Fuel 1.6 w/o']['univ'],           # dashpot
             cells['Fuel 1.6 w/o']['univ'],           # reg
             cells['Fuel 1.6 w/o grid_i']['univ'],      # reg grid 2
             cells['Fuel 1.6 w/o']['univ'],           # reg
             cells['Fuel 1.6 w/o grid_i']['univ'],      # reg grid 3
             cells['Fuel 1.6 w/o']['univ'],           # reg
#             cells['Fuel 1.6 w/o grid_i']['univ'],      # reg grid 4
#             cells['Fuel 1.6 w/o']['univ'],           # reg
#             cells['Fuel 1.6 w/o grid_i']['univ'],      # reg grid 5
#             cells['Fuel 1.6 w/o']['univ'],           # reg
#             cells['Fuel 1.6 w/o grid_i']['univ'],      # reg grid 6
#             cells['Fuel 1.6 w/o']['univ'],           # reg
#             cells['Fuel 1.6 w/o grid_i']['univ'],      # reg grid 7
#             cells['Fuel 1.6 w/o']['univ'],           # reg
             cells['pin plenum']['univ'],             # pin plenum
             cells['pin plenum grid_tb']['univ'],        # pin plenum grid 8
             cells['pin plenum']['univ'],             # pin plenum
             cells['end plug']['univ'],               # upper fuel rod end plug
             cells['water pin']['univ'],              # space between fuel rod and and upper nozzle
             cells['SS pin']['univ'],                 # upper nozzle
             cells['water pin']['univ']])             # upper plenum

  ## 2.4 w/o

  make_pin('Fuel 2.4 w/o',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['pellet OR']['id'],
             surfs['clad IR']['id'],
             surfs['clad OR']['id'],],
            [(mats['UO2 2.4']['id'],"UO2 Fuel 2.4 w/o"),
             (mats['helium']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),])
  make_pin('Fuel 2.4 w/o grid_tb',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['pellet OR']['id'],
             surfs['clad IR']['id'],
             surfs['clad OR']['id'],],
            [(mats['UO2 2.4']['id'],"UO2 Fuel 2.4 w/o with top/bottom grid"),
             (mats['helium']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),],
            grid=True, surfs=surfs, gridMat=mats['inconel']['id'], gridType='tb')
  make_pin('Fuel 2.4 w/o grid_i',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['pellet OR']['id'],
             surfs['clad IR']['id'],
             surfs['clad OR']['id'],],
            [(mats['UO2 2.4']['id'],"UO2 Fuel 2.4 w/o with intermediate grid"),
             (mats['helium']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),],
            grid=True, surfs=surfs, gridMat=mats['zirc']['id'], gridType='i')

  # final combination of all axial pieces for Fuel 2.4 w/o
  make_stack('Fuel 2.4 w/o stack',co,cells,new_id(univIDs),cellIDs,
            stackSurfs,
            [cells['water pin']['univ'],              # lower plenum
             cells['SS pin']['univ'],                 # support plate
             cells['SS pin']['univ'],                 # lower nozzle
             cells['end plug']['univ'],               # lower thimble
             cells['Fuel 2.4 w/o']['univ'],           # dashpot
             cells['Fuel 2.4 w/o grid_tb']['univ'],      # dashpot grid 1
             cells['Fuel 2.4 w/o']['univ'],           # dashpot
             cells['Fuel 2.4 w/o']['univ'],           # reg
             cells['Fuel 2.4 w/o grid_i']['univ'],      # reg grid 2
             cells['Fuel 2.4 w/o']['univ'],           # reg
             cells['Fuel 2.4 w/o grid_i']['univ'],      # reg grid 3
             cells['Fuel 2.4 w/o']['univ'],           # reg
#             cells['Fuel 2.4 w/o grid_i']['univ'],      # reg grid 4
#             cells['Fuel 2.4 w/o']['univ'],           # reg
#             cells['Fuel 2.4 w/o grid_i']['univ'],      # reg grid 5
#             cells['Fuel 2.4 w/o']['univ'],           # reg
#             cells['Fuel 2.4 w/o grid_i']['univ'],      # reg grid 6
#             cells['Fuel 2.4 w/o']['univ'],           # reg
#             cells['Fuel 2.4 w/o grid_i']['univ'],      # reg grid 7
#             cells['Fuel 2.4 w/o']['univ'],           # reg
             cells['pin plenum']['univ'],             # pin plenum
             cells['pin plenum grid_tb']['univ'],        # pin plenum grid 8
             cells['pin plenum']['univ'],             # pin plenum
             cells['end plug']['univ'],               # upper fuel rod end plug
             cells['water pin']['univ'],              # space between fuel rod and and upper nozzle
             cells['SS pin']['univ'],                 # upper nozzle
             cells['water pin']['univ']])             # upper plenum

  ## 3.1 w/o

  make_pin('Fuel 3.1 w/o',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['pellet OR']['id'],
             surfs['clad IR']['id'],
             surfs['clad OR']['id'],],
            [(mats['UO2 3.1']['id'],"UO2 Fuel 3.1 w/o"),
             (mats['helium']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),])
  make_pin('Fuel 3.1 w/o grid_tb',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['pellet OR']['id'],
             surfs['clad IR']['id'],
             surfs['clad OR']['id'],],
            [(mats['UO2 3.1']['id'],"UO2 Fuel 3.1 w/o with top/bottom grid"),
             (mats['helium']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),],
            grid=True, surfs=surfs, gridMat=mats['inconel']['id'], gridType='tb')
  make_pin('Fuel 3.1 w/o grid_i',"",co,cells,new_id(univIDs),cellIDs,
            [surfs['pellet OR']['id'],
             surfs['clad IR']['id'],
             surfs['clad OR']['id'],],
            [(mats['UO2 3.1']['id'],"UO2 Fuel 3.1 w/o with intermediate grid"),
             (mats['helium']['id'],""),
             (mats['zirc']['id'],""),
             (mats['water-nominal']['id'],""),],
            grid=True, surfs=surfs, gridMat=mats['zirc']['id'], gridType='i')

  # final combination of all axial pieces for Fuel 3.1 w/o
  make_stack('Fuel 3.1 w/o stack',co,cells,new_id(univIDs),cellIDs,
            stackSurfs,
            [cells['water pin']['univ'],              # lower plenum
             cells['SS pin']['univ'],                 # support plate
             cells['SS pin']['univ'],                 # lower nozzle
             cells['end plug']['univ'],               # lower thimble
             cells['Fuel 3.1 w/o']['univ'],           # dashpot
             cells['Fuel 3.1 w/o grid_tb']['univ'],      # dashpot grid 1
             cells['Fuel 3.1 w/o']['univ'],           # dashpot
             cells['Fuel 3.1 w/o']['univ'],           # reg
             cells['Fuel 3.1 w/o grid_i']['univ'],      # reg grid 2
             cells['Fuel 3.1 w/o']['univ'],           # reg
             cells['Fuel 3.1 w/o grid_i']['univ'],      # reg grid 3
             cells['Fuel 3.1 w/o']['univ'],           # reg
#             cells['Fuel 3.1 w/o grid_i']['univ'],      # reg grid 4
#             cells['Fuel 3.1 w/o']['univ'],           # reg
#             cells['Fuel 3.1 w/o grid_i']['univ'],      # reg grid 5
#             cells['Fuel 3.1 w/o']['univ'],           # reg
#             cells['Fuel 3.1 w/o grid_i']['univ'],      # reg grid 6
#             cells['Fuel 3.1 w/o']['univ'],           # reg
#             cells['Fuel 3.1 w/o grid_i']['univ'],      # reg grid 7
#             cells['Fuel 3.1 w/o']['univ'],           # reg
             cells['pin plenum']['univ'],             # pin plenum
             cells['pin plenum grid_tb']['univ'],        # pin plenum grid 8
             cells['pin plenum']['univ'],             # pin plenum
             cells['end plug']['univ'],               # upper fuel rod end plug
             cells['water pin']['univ'],              # space between fuel rod and and upper nozzle
             cells['SS pin']['univ'],                 # upper nozzle
             cells['water pin']['univ']])             # upper plenum


################## Baffle construction ##################


  lo = {'n': 0}
  latts = {}

  # baffle north

  surfs['baffle surf north'] =  { 'order':   inc_order(so),
                                  'section': comm_t.format("Baffle surfaces"),
                                  'comm':    comm_t.format("chosen for 2x2 baffle lattice, so w={0}".format(baffleWidth)),
                                  'id':      new_id(surfIDs),
                                  'type':    '"y-plane"',
                                  'coeffs':  '{0:0<8.5}'.format(latticePitch/4 - baffleWidth)}
  cells['baffle dummy north'] = { 'order':   inc_order(co),
                                  'section': comm_t.format("Baffle cells"),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'mat':     mats['SS304']['id'],
                                  'fill':    None,
                                  'surfs':  '{0}'.format(surfs['baffle surf north']['id'])}
  cells['baf dummy north 2'] =  { 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    cells['baffle dummy north']['univ'],
                                  'mat':     mats['water-nominal']['id'],
                                  'fill':    None,
                                  'surfs':  '-{0}'.format(surfs['baffle surf north']['id'])}
  latts['baffle north'] =       { 'order':   inc_order(lo),
                                  'comm':    comm_t.format("Baffle north"),
                                  'id':      new_id(univIDs),
                                  'type':    'rectangular',
                                  'dim':     2,
                                  'lleft':   -latticePitch/2,
                                  'width':   latticePitch/2,
                                  'univs':   """
{0:>3} {0:>3}
{1:>3} {1:>3}
""".format(cells['baffle dummy north']['univ'],cells['water pin']['univ'])}
  cells['baffle north'] =       { 'order':   inc_order(co),
                                  'comm':    comm_t.format("north baffle universe"),
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'fill':    latts['baffle north']['id'],
                                  'surfs':  '-{0}'.format(surfs['dummy outer']['id'])}

  # baffle south

  surfs['baffle surf south'] =  { 'order':   inc_order(so),
                                  'comm':    "",
                                  'id':      new_id(surfIDs),
                                  'type':    '"y-plane"',
                                  'coeffs':  '{0:0<8.6}'.format(baffleWidth - latticePitch/4)}
  cells['baffle dummy south'] = { 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'mat':     mats['water-nominal']['id'],
                                  'fill':    None,
                                  'surfs':  '{0}'.format(surfs['baffle surf south']['id'])}
  cells['baf dummy south 2'] =  { 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    cells['baffle dummy south']['univ'],
                                  'mat':     mats['SS304']['id'],
                                  'fill':    None,
                                  'surfs':  '-{0}'.format(surfs['baffle surf south']['id'])}
  latts['baffle south'] =       { 'order':   inc_order(lo),
                                  'comm':    comm_t.format("Baffle south"),
                                  'id':      new_id(univIDs),
                                  'type':    'rectangular',
                                  'dim':     2,
                                  'lleft':   -latticePitch/2,
                                  'width':   latticePitch/2,
                                  'univs':   """
{1:>3} {1:>3}
{0:>3} {0:>3}
""".format(cells['baffle dummy south']['univ'],cells['water pin']['univ'])}
  cells['baffle south'] =       { 'order':   inc_order(co),
                                  'comm':    comm_t.format("south baffle universe"),
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'fill':    latts['baffle south']['id'],
                                  'surfs':  '-{0}'.format(surfs['dummy outer']['id'])}

  # bafffle east

  surfs['baffle surf east'] =   { 'order':   inc_order(so),
                                  'comm':    "",
                                  'id':      new_id(surfIDs),
                                  'type':    '"x-plane"',
                                  'coeffs':  '{0:0<8.5}'.format(latticePitch/4 - baffleWidth)}
  cells['baffle dummy east'] =  { 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'mat':     mats['SS304']['id'],
                                  'fill':    None,
                                  'surfs':  '{0}'.format(surfs['baffle surf east']['id'])}
  cells['baf dummy east 2'] =   { 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    cells['baffle dummy east']['univ'],
                                  'mat':     mats['water-nominal']['id'],
                                  'fill':    None,
                                  'surfs':  '-{0}'.format(surfs['baffle surf east']['id'])}
  latts['baffle east'] =       { 'order':   inc_order(lo),
                                  'comm':    comm_t.format("Baffle east"),
                                  'id':      new_id(univIDs),
                                  'type':    'rectangular',
                                  'dim':     2,
                                  'lleft':   -latticePitch/2,
                                  'width':   latticePitch/2,
                                  'univs':   """
{1:>3} {0:>3}
{1:>3} {0:>3}
""".format(cells['baffle dummy east']['univ'],cells['water pin']['univ'])}
  cells['baffle east'] =       { 'order':   inc_order(co),
                                  'comm':    comm_t.format("east baffle universe"),
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'fill':    latts['baffle east']['id'],
                                  'surfs':  '-{0}'.format(surfs['dummy outer']['id'])}

  # baffle west

  surfs['baffle surf west'] =   { 'order':   inc_order(so),
                                  'comm':    "",
                                  'id':      new_id(surfIDs),
                                  'type':    '"x-plane"',
                                  'coeffs':  '{0:0<8.6}'.format(baffleWidth - latticePitch/4)}
  cells['baffle dummy west'] =  { 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'mat':     mats['water-nominal']['id'],
                                  'fill':    None,
                                  'surfs':  '{0}'.format(surfs['baffle surf west']['id'])}
  cells['baf dummy west 2'] =   { 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    cells['baffle dummy west']['univ'],
                                  'mat':     mats['SS304']['id'],
                                  'fill':    None,
                                  'surfs':  '-{0}'.format(surfs['baffle surf west']['id'])}
  latts['baffle west'] =       { 'order':   inc_order(lo),
                                  'comm':    comm_t.format("Baffle west"),
                                  'id':      new_id(univIDs),
                                  'type':    'rectangular',
                                  'dim':     2,
                                  'lleft':   -latticePitch/2,
                                  'width':   latticePitch/2,
                                  'univs':   """
{0:>3} {1:>3}
{0:>3} {1:>3}
""".format(cells['baffle dummy west']['univ'],cells['water pin']['univ'])}
  cells['baffle west'] =       { 'order':   inc_order(co),
                                  'comm':    comm_t.format("west baffle universe"),
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'fill':    latts['baffle west']['id'],
                                  'surfs':  '-{0}'.format(surfs['dummy outer']['id'])}


  # baffle NW edges

  cells['baf dummy edges NW'] = { 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'mat':     mats['water-nominal']['id'],
                                  'fill':    None,
                                  'surfs':  '{0} -{1}'.format(surfs['baffle surf west']['id'],surfs['baffle surf north']['id'])}
  cells['baf dmy edges NW 2'] = { 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    cells['baf dummy edges NW']['univ'],
                                  'mat':     mats['SS304']['id'],
                                  'fill':    None,
                                  'surfs':  '{0} {1}'.format(surfs['baffle surf west']['id'],surfs['baffle surf north']['id'])}
  cells['baf dmy edges NW 3'] = { 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    cells['baf dummy edges NW']['univ'],
                                  'mat':     mats['SS304']['id'],
                                  'fill':    None,
                                  'surfs':  '-{0}'.format(surfs['baffle surf west']['id'])}
  latts['baffle edges NW'] =    { 'order':   inc_order(lo),
                                  'comm':    comm_t.format("Baffle NW edges"),
                                  'id':      new_id(univIDs),
                                  'type':    'rectangular',
                                  'dim':     2,
                                  'lleft':   -latticePitch/2,
                                  'width':   latticePitch/2,
                                  'univs':   """
{0:>3} {1:>3}
{2:>3} {3:>3}
""".format(cells['baf dummy edges NW']['univ'],cells['baffle dummy north']['univ'],cells['baffle dummy west']['univ'],cells['water pin']['univ'])}
  cells['baffle edges NW'] =       { 'order':   inc_order(co),
                                  'comm':    comm_t.format("NW edges baffle universe"),
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'fill':    latts['baffle edges NW']['id'],
                                  'surfs':  '-{0}'.format(surfs['dummy outer']['id'])}


  # baffle NE edges

  cells['baf dummy edges NE'] = { 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'mat':     mats['water-nominal']['id'],
                                  'fill':    None,
                                  'surfs':  '-{0} -{1}'.format(surfs['baffle surf north']['id'],surfs['baffle surf east']['id'])}
  cells['baf dmy edges NE 2'] = { 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    cells['baf dummy edges NE']['univ'],
                                  'mat':     mats['SS304']['id'],
                                  'fill':    None,
                                  'surfs':  '{0} -{1}'.format(surfs['baffle surf north']['id'],surfs['baffle surf east']['id'])}
  cells['baf dmy edges NE 3'] = { 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    cells['baf dummy edges NE']['univ'],
                                  'mat':     mats['SS304']['id'],
                                  'fill':    None,
                                  'surfs':  '{0}'.format(surfs['baffle surf east']['id'])}
  latts['baffle edges NE'] =    { 'order':   inc_order(lo),
                                  'comm':    comm_t.format("Baffle NE edges"),
                                  'id':      new_id(univIDs),
                                  'type':    'rectangular',
                                  'dim':     2,
                                  'lleft':   -latticePitch/2,
                                  'width':   latticePitch/2,
                                  'univs':   """
{0:>3} {1:>3}
{2:>3} {3:>3}
""".format(cells['baffle dummy north']['univ'],cells['baf dummy edges NE']['univ'],cells['water pin']['univ'],cells['baffle dummy east']['univ'])}
  cells['baffle edges NE'] =       { 'order':   inc_order(co),
                                  'comm':    comm_t.format("NE edges baffle universe"),
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'fill':    latts['baffle edges NE']['id'],
                                  'surfs':  '-{0}'.format(surfs['dummy outer']['id'])}

  # baffle SW edges

  cells['baf dummy edges SW'] = { 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'mat':     mats['water-nominal']['id'],
                                  'fill':    None,
                                  'surfs':  '{0} {1}'.format(surfs['baffle surf south']['id'],surfs['baffle surf west']['id'])}
  cells['baf dmy edges SW 2'] = { 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    cells['baf dummy edges SW']['univ'],
                                  'mat':     mats['SS304']['id'],
                                  'fill':    None,
                                  'surfs':  '-{0} {1}'.format(surfs['baffle surf south']['id'],surfs['baffle surf west']['id'])}
  cells['baf dmy edges SW 3'] = { 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    cells['baf dummy edges SW']['univ'],
                                  'mat':     mats['SS304']['id'],
                                  'fill':    None,
                                  'surfs':  '-{0}'.format(surfs['baffle surf west']['id'])}
  latts['baffle edges SW'] =    { 'order':   inc_order(lo),
                                  'comm':    comm_t.format("Baffle SW edges"),
                                  'id':      new_id(univIDs),
                                  'type':    'rectangular',
                                  'dim':     2,
                                  'lleft':   -latticePitch/2,
                                  'width':   latticePitch/2,
                                  'univs':   """
{0:>3} {1:>3}
{2:>3} {3:>3}
""".format(cells['baffle dummy west']['univ'],cells['water pin']['univ'],cells['baf dummy edges SW']['univ'],cells['baffle dummy south']['univ'])}
  cells['baffle edges SW'] =       { 'order':   inc_order(co),
                                  'comm':    comm_t.format("NE edges baffle universe"),
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'fill':    latts['baffle edges SW']['id'],
                                  'surfs':  '-{0}'.format(surfs['dummy outer']['id'])}

  # baffle SE edges

  cells['baf dummy edges SE'] = { 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'mat':     mats['water-nominal']['id'],
                                  'fill':    None,
                                  'surfs':  '{0} -{1}'.format(surfs['baffle surf south']['id'],surfs['baffle surf east']['id'])}
  cells['baf dmy edges SE 2'] = { 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    cells['baf dummy edges SE']['univ'],
                                  'mat':     mats['SS304']['id'],
                                  'fill':    None,
                                  'surfs':  '-{0} -{1}'.format(surfs['baffle surf south']['id'],surfs['baffle surf east']['id'])}
  cells['baf dmy edges SE 3'] = { 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    cells['baf dummy edges SE']['univ'],
                                  'mat':     mats['SS304']['id'],
                                  'fill':    None,
                                  'surfs':  '{0}'.format(surfs['baffle surf east']['id'])}
  latts['baffle edges SE'] =    { 'order':   inc_order(lo),
                                  'comm':    comm_t.format("Baffle SE edges"),
                                  'id':      new_id(univIDs),
                                  'type':    'rectangular',
                                  'dim':     2,
                                  'lleft':   -latticePitch/2,
                                  'width':   latticePitch/2,
                                  'univs':   """
{0:>3} {1:>3}
{2:>3} {3:>3}
""".format(cells['water pin']['univ'],cells['baffle dummy east']['univ'],cells['baffle dummy south']['univ'],cells['baf dummy edges SE']['univ'])}
  cells['baffle edges SE'] =       { 'order':   inc_order(co),
                                  'comm':    comm_t.format("NE edges baffle universe"),
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'fill':    latts['baffle edges SE']['id'],
                                  'surfs':  '-{0}'.format(surfs['dummy outer']['id'])}

  # baffle NW corner

  cells['baf dummy corner NW'] ={ 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'mat':     mats['water-nominal']['id'],
                                  'fill':    None,
                                  'surfs':  '-{0} -{1}'.format(surfs['baffle surf west']['id'],surfs['baffle surf north']['id'])}
  cells['baf dmy corner NW 2'] ={ 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    cells['baf dummy corner NW']['univ'],
                                  'mat':     mats['water-nominal']['id'],
                                  'fill':    None,
                                  'surfs':  '{0}'.format(surfs['baffle surf west']['id'])}
  cells['baf dmy corner NW 3'] ={ 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    cells['baf dummy corner NW']['univ'],
                                  'mat':     mats['SS304']['id'],
                                  'fill':    None,
                                  'surfs':  '{0} -{1}'.format(surfs['baffle surf north']['id'],surfs['baffle surf west']['id'])}
  latts['baffle corner NW'] =   { 'order':   inc_order(lo),
                                  'comm':    comm_t.format("Baffle NW corner"),
                                  'id':      new_id(univIDs),
                                  'type':    'rectangular',
                                  'dim':     2,
                                  'lleft':   -latticePitch/2,
                                  'width':   latticePitch/2,
                                  'univs':   """
{0:>3} {1:>3}
{1:>3} {1:>3}
""".format(cells['baf dummy corner NW']['univ'],cells['water pin']['univ'])}
  cells['baffle corner NW'] =   { 'order':   inc_order(co),
                                  'comm':    comm_t.format("NW corner baffle universe"),
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'fill':    latts['baffle corner NW']['id'],
                                  'surfs':  '-{0}'.format(surfs['dummy outer']['id'])}

  # baffle NE corner

  cells['baf dummy corner NE'] ={ 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'mat':     mats['water-nominal']['id'],
                                  'fill':    None,
                                  'surfs':  '{0} -{1}'.format(surfs['baffle surf east']['id'],surfs['baffle surf north']['id'])}
  cells['baf dmy corner NE 2'] ={ 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    cells['baf dummy corner NE']['univ'],
                                  'mat':     mats['water-nominal']['id'],
                                  'fill':    None,
                                  'surfs':  '-{0}'.format(surfs['baffle surf east']['id'])}
  cells['baf dmy corner NE 3'] ={ 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    cells['baf dummy corner NE']['univ'],
                                  'mat':     mats['SS304']['id'],
                                  'fill':    None,
                                  'surfs':  '{0} {1}'.format(surfs['baffle surf north']['id'],surfs['baffle surf east']['id'])}
  latts['baffle corner NE'] =   { 'order':   inc_order(lo),
                                  'comm':    comm_t.format("Baffle NE corner"),
                                  'id':      new_id(univIDs),
                                  'type':    'rectangular',
                                  'dim':     2,
                                  'lleft':   -latticePitch/2,
                                  'width':   latticePitch/2,
                                  'univs':   """
{1:>3} {0:>3}
{1:>3} {1:>3}
""".format(cells['baf dummy corner NE']['univ'],cells['water pin']['univ'])}
  cells['baffle corner NE'] =   { 'order':   inc_order(co),
                                  'comm':    comm_t.format("NE corner baffle universe"),
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'fill':    latts['baffle corner NE']['id'],
                                  'surfs':  '-{0}'.format(surfs['dummy outer']['id'])}

  # baffle SE corner

  cells['baf dummy corner SE'] ={ 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'mat':     mats['water-nominal']['id'],
                                  'fill':    None,
                                  'surfs':  '{0} {1}'.format(surfs['baffle surf east']['id'],surfs['baffle surf south']['id'])}
  cells['baf dmy corner SE 2'] ={ 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    cells['baf dummy corner SE']['univ'],
                                  'mat':     mats['water-nominal']['id'],
                                  'fill':    None,
                                  'surfs':  '-{0}'.format(surfs['baffle surf east']['id'])}
  cells['baf dmy corner SE 3'] ={ 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    cells['baf dummy corner SE']['univ'],
                                  'mat':     mats['SS304']['id'],
                                  'fill':    None,
                                  'surfs':  '-{0} {1}'.format(surfs['baffle surf south']['id'],surfs['baffle surf east']['id'])}
  latts['baffle corner SE'] =   { 'order':   inc_order(lo),
                                  'comm':    comm_t.format("Baffle SE corner"),
                                  'id':      new_id(univIDs),
                                  'type':    'rectangular',
                                  'dim':     2,
                                  'lleft':   -latticePitch/2,
                                  'width':   latticePitch/2,
                                  'univs':   """
{1:>3} {1:>3}
{1:>3} {0:>3}
""".format(cells['baf dummy corner SE']['univ'],cells['water pin']['univ'])}
  cells['baffle corner SE'] =   { 'order':   inc_order(co),
                                  'comm':    comm_t.format("SE corner baffle universe"),
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'fill':    latts['baffle corner SE']['id'],
                                  'surfs':  '-{0}'.format(surfs['dummy outer']['id'])}

  # baffle SW corner

  cells['baf dummy corner SW'] ={ 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'mat':     mats['water-nominal']['id'],
                                  'fill':    None,
                                  'surfs':  '-{0} {1}'.format(surfs['baffle surf west']['id'],surfs['baffle surf south']['id'])}
  cells['baf dmy corner SW 2'] ={ 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    cells['baf dummy corner SW']['univ'],
                                  'mat':     mats['water-nominal']['id'],
                                  'fill':    None,
                                  'surfs':  '{0}'.format(surfs['baffle surf west']['id'])}
  cells['baf dmy corner SW 3'] ={ 'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    cells['baf dummy corner SW']['univ'],
                                  'mat':     mats['SS304']['id'],
                                  'fill':    None,
                                  'surfs':  '-{0} -{1}'.format(surfs['baffle surf south']['id'],surfs['baffle surf west']['id'])}
  latts['baffle corner SW'] =   { 'order':   inc_order(lo),
                                  'comm':    comm_t.format("Baffle SW corner"),
                                  'id':      new_id(univIDs),
                                  'type':    'rectangular',
                                  'dim':     2,
                                  'lleft':   -latticePitch/2,
                                  'width':   latticePitch/2,
                                  'univs':   """
{1:>3} {1:>3}
{0:>3} {1:>3}
""".format(cells['baf dummy corner SW']['univ'],cells['water pin']['univ'])}
  cells['baffle corner SW'] =   { 'order':   inc_order(co),
                                  'comm':    comm_t.format("SW corner baffle universe"),
                                  'id':      new_id(cellIDs),
                                  'univ':    new_id(univIDs),
                                  'fill':    latts['baffle corner SW']['id'],
                                  'surfs':  '-{0}'.format(surfs['dummy outer']['id'])}

  baffle = {}
  baffle['bafn_'] = cells['baffle south']['univ']
  baffle['bafs_'] = cells['baffle north']['univ']
  baffle['bafe_'] = cells['baffle west']['univ']
  baffle['bafw_'] = cells['baffle east']['univ']
  baffle['bafnw'] = cells['baffle corner SE']['univ']
  baffle['bafne'] = cells['baffle corner SW']['univ']
  baffle['bafsw'] = cells['baffle corner NE']['univ']
  baffle['bafse'] = cells['baffle corner NW']['univ']
  baffle['bfcnw'] = cells['baffle edges SE']['univ']
  baffle['bfcne'] = cells['baffle edges SW']['univ']
  baffle['bfcsw'] = cells['baffle edges NE']['univ']
  baffle['bfcse'] = cells['baffle edges NW']['univ']




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

  latDims = { 'dim':17, 'lleft':-17*pinPitch/2, 'width':pinPitch}

  ## 1.6 w/o assemblies

  for cent,comment1 in [(gti,""),(ins," + instr")]:

    if cent == gti:
      sss = "Core Lattice universes"
    else:
      sss = None

    # No BAs
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 1.6 w/o'+comment1,comm="Assembly 1.6 w/o no BAs"+comment1, sect=sss,
                                 univs=pinLattice_t.format(cells['Fuel 1.6 w/o stack']['univ'],
                                                    a=gtu,  b=gtu,  c=gtu,
                                            d=gtu,                          e=gtu,
                                            f=gtu,  g=gtu,  h=gtu,  i=gtu,  j=gtu,
                                            k=gtu,  l=gtu,  m=cent, n=gtu,  o=gtu,
                                            p=gtu,  q=gtu,  r=gtu,  s=gtu,  t=gtu,
                                            u=gtu,                          v=gtu,
                                                    w=gtu,  x=gtu,  y=gtu,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 1.6 w/o'+comment1] = newCells

    for bank,comment2 in [(crA,' + CRA'),(crB,' + CRB'),(crC,' + CRC'),(crD,' + CRD'),
                          (crSB,' + shutB'),(crSC,' + shutC'),(crSD,' + shutD'),(crSE,' + shutE')]:

      newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                    'Fuel 1.6 w/o'+comment1+comment2,comm="Assembly 1.6 w/o"+comment1+comment2,
                                   univs=pinLattice_t.format(cells['Fuel 1.6 w/o stack']['univ'],
                                                      a=bank,  b=bank,  c=bank,
                                              d=bank,                             e=bank,
                                              f=bank,  g=bank,  h=bank,  i=bank,  j=bank,
                                              k=bank,  l=bank,  m=cent,  n=bank,  o=bank,
                                              p=bank,  q=bank,  r=bank,  s=bank,  t=bank,
                                              u=bank,                             v=bank,
                                                      w=bank,  x=bank,  y=bank,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
      assemblyCells['Fuel 1.6 w/o'+comment1+comment2] = newCells



  ## 2.4 w/o assemblies

  for cen,comment1 in [(gti,""),(ins," + instr")]:

    # no BAs
    bank = gtu
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 2.4 w/o'+comment1,comm="Assembly 2.4 w/o no BAs"+comment1,
                                 univs=pinLattice_t.format(cells['Fuel 2.4 w/o stack']['univ'],
                                                    a=bank,  b=bank,  c=bank,
                                            d=bank,                             e=bank,
                                            f=bank,  g=bank,  h=bank,  i=bank,  j=bank,
                                            k=bank,  l=bank,  m=cen,   n=bank,  o=bank,
                                            p=bank,  q=bank,  r=bank,  s=bank,  t=bank,
                                            u=bank,                             v=bank,
                                                    w=bank,  x=bank,  y=bank,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 2.4 w/o'+comment1] = newCells

    # CRD
    bank = crD
    comment2 = ' + CRD'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 2.4 w/o'+comment1+comment2,comm="Assembly 2.4 w/o "+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 2.4 w/o stack']['univ'],
                                                    a=bank,  b=bank,  c=bank,
                                            d=bank,                             e=bank,
                                            f=bank,  g=bank,  h=bank,  i=bank,  j=bank,
                                            k=bank,  l=bank,  m=cen,   n=bank,  o=bank,
                                            p=bank,  q=bank,  r=bank,  s=bank,  t=bank,
                                            u=bank,                             v=bank,
                                                    w=bank,  x=bank,  y=bank,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 2.4 w/o'+comment1+comment2] = newCells

    # 12 BAs
    comment2 = ' + 12BA'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 2.4 w/o'+comment1+comment2,comm="Assembly 2.4 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 2.4 w/o stack']['univ'],
                                                    a=bas,  b=gtu,  c=bas,
                                            d=bas,                          e=bas,
                                            f=bas,  g=gtu,  h=gtu,  i=gtu,  j=bas,
                                            k=gtu,  l=gtu,  m=cen,  n=gtu,  o=gtu,
                                            p=bas,  q=gtu,  r=gtu,  s=gtu,  t=bas,
                                            u=bas,                          v=bas,
                                                    w=bas,  x=gtu,  y=bas,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 2.4 w/o'+comment1+comment2] = newCells

    # 16 BAs
    comment2 = ' + 16BA'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 2.4 w/o'+comment1+comment2,comm="Assembly 2.4 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 2.4 w/o stack']['univ'],
                                                    a=bas,  b=bas,  c=bas,
                                            d=bas,                          e=bas,
                                            f=bas,  g=gtu,  h=gtu,  i=gtu,  j=bas,
                                            k=bas,  l=gtu,  m=cen,  n=gtu,  o=bas,
                                            p=bas,  q=gtu,  r=gtu,  s=gtu,  t=bas,
                                            u=bas,                          v=bas,
                                                    w=bas,  x=bas,  y=bas,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 2.4 w/o'+comment1+comment2] = newCells
    
  ## 3.1 w/o assemblies

  for cen,comment1 in [(gti,""),(ins," + instr")]:

    # no BAs
    bank = gtu
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1,comm="Assembly 3.1 w/o no BAs"+comment1,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=bank,  b=bank,  c=bank,
                                            d=bank,                             e=bank,
                                            f=bank,  g=bank,  h=bank,  i=bank,  j=bank,
                                            k=bank,  l=bank,  m=cen,   n=bank,  o=bank,
                                            p=bank,  q=bank,  r=bank,  s=bank,  t=bank,
                                            u=bank,                             v=bank,
                                                    w=bank,  x=bank,  y=bank,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1] = newCells
    
    # shut
    bank = crSA
    comment2 = ' + shutA'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=bank,  b=bank,  c=bank,
                                            d=bank,                             e=bank,
                                            f=bank,  g=bank,  h=bank,  i=bank,  j=bank,
                                            k=bank,  l=bank,  m=cen,   n=bank,  o=bank,
                                            p=bank,  q=bank,  r=bank,  s=bank,  t=bank,
                                            u=bank,                             v=bank,
                                                    w=bank,  x=bank,  y=bank,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells
    
    # 20 BAs
    comment2 = ' + 20BA'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=bas,  b=bas,  c=bas,
                                            d=bas,                          e=bas,
                                            f=bas,  g=bas,  h=gtu,  i=bas,  j=bas,
                                            k=bas,  l=gtu,  m=cen,  n=gtu,  o=bas,
                                            p=bas,  q=bas,  r=gtu,  s=bas,  t=bas,
                                            u=bas,                          v=bas,
                                                    w=bas,  x=bas,  y=bas,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells

    # 16 BAs
    comment2 = ' + 16BA'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=bas,  b=bas,  c=bas,
                                            d=bas,                          e=bas,
                                            f=bas,  g=gtu,  h=gtu,  i=gtu,  j=bas,
                                            k=bas,  l=gtu,  m=cen,  n=gtu,  o=bas,
                                            p=bas,  q=gtu,  r=gtu,  s=gtu,  t=bas,
                                            u=bas,                          v=bas,
                                                    w=bas,  x=bas,  y=bas,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells
    
    # 15 BAs NW
    comment2 = ' + 15BANW'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=gtu,  b=gtu,  c=gtu,
                                            d=gtu,                          e=gtu,
                                            f=gtu,  g=bas,  h=bas,  i=bas,  j=bas,
                                            k=gtu,  l=bas,  m=cen,  n=bas,  o=bas,
                                            p=gtu,  q=bas,  r=bas,  s=bas,  t=bas,
                                            u=gtu,                          v=bas,
                                                    w=bas,  x=bas,  y=bas,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells

    # 15 BAs NE
    comment2 = ' + 15BANE'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=gtu,  b=gtu,  c=gtu,
                                            d=gtu,                          e=gtu,
                                            f=bas,  g=bas,  h=bas,  i=bas,  j=gtu,
                                            k=bas,  l=bas,  m=cen,  n=bas,  o=gtu,
                                            p=bas,  q=bas,  r=bas,  s=bas,  t=gtu,
                                            u=bas,                          v=gtu,
                                                    w=bas,  x=bas,  y=bas,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells
    
    # 15 BAs SW
    comment2 = ' + 15BASW'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=bas,  b=bas,  c=bas,
                                            d=gtu,                          e=bas,
                                            f=gtu,  g=bas,  h=bas,  i=bas,  j=bas,
                                            k=gtu,  l=bas,  m=cen,  n=bas,  o=bas,
                                            p=gtu,  q=bas,  r=bas,  s=bas,  t=bas,
                                            u=gtu,                          v=gtu,
                                                    w=gtu,  x=gtu,  y=gtu,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells
    
    # 15 BAs SE
    comment2 = ' + 15BASE'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=bas,  b=bas,  c=bas,
                                            d=bas,                          e=gtu,
                                            f=bas,  g=bas,  h=bas,  i=bas,  j=gtu,
                                            k=bas,  l=bas,  m=cen,  n=bas,  o=gtu,
                                            p=bas,  q=bas,  r=bas,  s=bas,  t=gtu,
                                            u=gtu,                          v=gtu,
                                                    w=gtu,  x=gtu,  y=gtu,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells
    
    # 6 BAs N
    comment2 = ' + 6BAN'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=gtu,  b=gtu,  c=gtu,
                                            d=gtu,                          e=gtu,
                                            f=gtu,  g=gtu,  h=gtu,  i=gtu,  j=gtu,
                                            k=gtu,  l=gtu,  m=cen,  n=gtu,  o=gtu,
                                            p=bas,  q=gtu,  r=gtu,  s=gtu,  t=bas,
                                            u=bas,                          v=bas,
                                                    w=bas,  x=gtu,  y=bas,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells
    
    # 6 BAs S
    comment2 = ' + 6BAS'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=bas,  b=gtu,  c=bas,
                                            d=bas,                          e=bas,
                                            f=bas,  g=gtu,  h=gtu,  i=gtu,  j=bas,
                                            k=gtu,  l=gtu,  m=cen,  n=gtu,  o=gtu,
                                            p=gtu,  q=gtu,  r=gtu,  s=gtu,  t=gtu,
                                            u=gtu,                          v=gtu,
                                                    w=gtu,  x=gtu,  y=gtu,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells

    # 6 BAs W
    comment2 = ' + 6BAW'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=gtu,  b=gtu,  c=bas,
                                            d=gtu,                          e=bas,
                                            f=gtu,  g=gtu,  h=gtu,  i=gtu,  j=bas,
                                            k=gtu,  l=gtu,  m=cen,  n=gtu,  o=gtu,
                                            p=gtu,  q=gtu,  r=gtu,  s=gtu,  t=bas,
                                            u=gtu,                          v=bas,
                                                    w=gtu,  x=gtu,  y=bas,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells
    
    # 6 BAs E
    comment2 = ' + 6BAE'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=bas,  b=gtu,  c=gtu,
                                            d=bas,                          e=gtu,
                                            f=bas,  g=gtu,  h=gtu,  i=gtu,  j=gtu,
                                            k=gtu,  l=gtu,  m=cen,  n=gtu,  o=gtu,
                                            p=bas,  q=gtu,  r=gtu,  s=gtu,  t=gtu,
                                            u=bas,                          v=gtu,
                                                    w=bas,  x=gtu,  y=gtu,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells

    

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
  
#  plots["main cells"] =     { 'id':     new_id(plotIDs),
#                              'fname':  'center_cells',
#                              'type':   'slice', 
#                              'col':    'cell',
#                              'background': '255 255 255',
#                              'origin': '0.0 0.0 {0}'.format((highestExtent-lowestExtent)/2),
#                              'width':  '{0} {0}'.format(coreBarrelIR*2+10),
#                              'basis':  'xy',
#                              'pixels': '3000 3000',}
# plots["main mats"] =      { 'id':     new_id(plotIDs),
#                             'fname':  'center_mats',
#                             'type':   'slice', 
#                             'col':    'mat',
#                             'background': '255 255 255',
#                             'origin': '0.0 0.0 {0}'.format((highestExtent-lowestExtent)/2),
#                             'width':  '{0} {0}'.format(rpvOR*2+10),
#                             'basis':  'xy',
#                             'pixels': '6000 6000',
#                             'spec':   colSpecMat,}
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
#  plots["grid5 mats H7"] =  { 'id':     new_id(plotIDs),
#                              'fname':  'H7_mats',
#                              'type':   'slice', 
#                              'col':    'mat',
#                              'background': '255 255 255',
#                              'origin': '{x} {y} {z}'.format(x=0.0,y=latticePitch,z=(highestExtent-lowestExtent)/2),
#                              'width':  '{0} {0}'.format(latticePitch),
#                              'basis':  'xy',
#                              'pixels': '5000 5000',
#                              'spec':   colSpecMat,}
#  plots["grid8 mats J14"] = { 'id':     new_id(plotIDs),
#                              'fname':  'grid8_mats_J14',
#                              'type':   'slice', 
#                              'col':    'mat',
#                              'background': '255 255 255',
#                              'origin': '{x} {y} {z}'.format(x=-latticePitch+latticePitch/3,y=-6*latticePitch+latticePitch/3,z=grid8Center),
#                              'width':  '{0} {0}'.format(latticePitch),
#                              'basis':  'xy',
#                              'pixels': '5000 5000',
#                              'spec':   colSpecMat,}
# plots["grid5 mats J14"] = { 'id':     new_id(plotIDs),
#                             'fname':  'grid5_mats_J14',
#                             'type':   'slice', 
#                             'col':    'mat',
#                             'background': '255 255 255',
#                             'origin': '{x} {y} {z}'.format(x=-latticePitch+latticePitch/3,y=-6*latticePitch+latticePitch/3,z=grid5Center),
#                             'width':  '{0} {0}'.format(latticePitch),
#                             'basis':  'xy',
#                             'pixels': '5000 5000',
#                             'spec':   colSpecMat,}
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

  # BA position plot
#  mask = []
#  colors = {}
#  mask.append(cells['burn abs']['id'])
#  mask.append(cells['burn abs1']['id'])
#  mask.append(cells['burn abs2']['id'])
#  mask.append(cells['burn abs3']['id'])
#  mask.append(cells['burn abs4']['id'])
#  mask.append(cells['burn abs5']['id'])
#  mask.append(cells['burn abs6']['id'])
#  colors[cells['burn abs']['id']] = "0 0 0"
#  colors[cells['burn abs1']['id']] = "0 0 0"
#  colors[cells['burn abs2']['id']] = "0 0 0"
#  colors[cells['burn abs3']['id']] = "0 0 0"
#  colors[cells['burn abs4']['id']] = "0 0 0"
#  colors[cells['burn abs5']['id']] = "0 0 0"
#  colors[cells['burn abs6']['id']] = "0 0 0"
#  for assembly,cellList in assemblyCells.items():
#    mask.append(cells[cellList[-1]]['id'])
#    mask.append(cells[cellList[-2]]['id'])
#    mask.append(cells[cellList[-3]]['id'])
#    mask.append(cells[cellList[-4]]['id'])
#    colors[cells[cellList[-1]]['id']] = "0 0 0"
#    colors[cells[cellList[-2]]['id']] = "0 0 0"
#    colors[cells[cellList[-3]]['id']] = "0 0 0"
#    colors[cells[cellList[-4]]['id']] = "0 0 0"
#  for cellName,cell in cells.items():
#    if 'baf' in cellName and 'mat' in cell:
#      if cell['mat'] == mats['SS304']['id']:
#        mask.append(cell['id'])
#        colors[cell['id']] = "0 0 0"

#  plots["ba pos"] =         { 'id':         new_id(plotIDs),
#                              'fname':      'ba_positions',
#                              'type':       'slice',
#                              'col':        'cell',
#                              'background': '255 255 255',
#                              'origin':     '0.0 0.0 {0}'.format((highestExtent-lowestExtent)/2),
#                              'width':      '{0} {0}'.format(rpvOR*2+10),
#                              'basis':      'xy',
#                              'pixels':     '6000 6000',
#                              'spec':       colors,
#                              'msk':        { 'maskrgb':  '255 255 255',
#                                              'comps':    '\n          '.join([str(m) for m in mask])},}

  # instr tube position plot
#  mask = []
#  mask.append(cells['GT instr']['id'])
#  mask.append(cells['GT instr1']['id'])
#  mask.append(cells['GT instr2']['id'])
#  for assembly,cellList in assemblyCells.items():
#    mask.append(cells[cellList[-1]]['id'])
#    mask.append(cells[cellList[-2]]['id'])
#    mask.append(cells[cellList[-3]]['id'])
#    mask.append(cells[cellList[-4]]['id'])
#  for cellName,cell in cells.items():
#    if 'baf' in cellName and 'mat' in cell:
#      if cell['mat'] == mats['SS304']['id']:
#        mask.append(cell['id'])

#  plots["instr pos"] =      { 'id':         new_id(plotIDs),
#                              'fname':      'instr_positions',
#                              'type':       'slice',
#                              'col':        'cell',
#                              'background': '255 255 255',
#                              'origin':     '0.0 0.0 {0}'.format((highestExtent-lowestExtent)/2),
#                              'width':      '{0} {0}'.format(rpvOR*2+10),
#                              'basis':      'xy',
#                              'pixels':     '6000 6000',
#                              'msk':        { 'maskrgb':  '255 255 255',
#                                              'comps':    '\n          '.join([str(m) for m in mask])},}


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


def make_pin(name,section,co,cells,univ,cellIDs,radSurfList,matList,
             grid=False, surfs=None, gridMat=None, gridType=None):
  """Populates the cells dictionary with a radial pincell universe
  
    name       - string, name of the cell as well as  outKeys = [name] the comment to be written
    section    - section comment - not written if left as ""
    co         - cells order dictionary
    cells      - cells dictionary
    univ       - new universe id number for this pincell
    cellIDs    - set of already used cell IDs
    radSurfList- list of surface IDs, from inside to outside
    matList    - list of tuples of material IDs and comments, from inside to outside.
                 length should be one more than radSurfList.
                 first material will be the inside of the first surface,
                 last last will be outside the last surface.
                 if comments are "", no comment will be written

    Since box surfaces aren't fully implemented yet, square grids around the
    outside of pins need to be added manually here.

    grid       - flag for whether or not to make the grid
    surfs      - full surfaces dictionary.  This routine uses the 'rod grid box'
                 surfaces
    gridMat    - material for the grid
    gridType   - either 'i' or 'tb' for intermediate or top/bottom
    
  """
  
  cells[name] = { 'order':   inc_order(co),
                  'comm':    "",
                  'id':      new_id(cellIDs),
                  'univ':    univ,
                  'mat':     matList[0][0],
                  'fill':    None,
                  'surfs':   '-{0}'.format(radSurfList[0])}
  if section != "":
    cells[name]['section'] = comm_t.format(section)
  if matList[0][1] != "":
    cells[name]['comm'] = comm_t.format(matList[0][1])

  for i,(matIDcomment,outSurf) in enumerate(zip(matList[1:-1],radSurfList[:-1])):
    cells[name + str(i)] = {  'order':   inc_order(co),
                              'comm':    "",
                              'id':      new_id(cellIDs),
                              'univ':    univ,
                              'mat':     matIDcomment[0],
                              'fill':    None,
                              'surfs':  '{0} -{1}'.format(outSurf,radSurfList[i+1])}
    if matIDcomment[1] != "":
      cells[name + str(i)]['comm'] = comm_t.format(matIDcomment[1])
      
  cells[name + 'last'] = {  'order':   inc_order(co),
                            'comm':    "",
                            'id':      new_id(cellIDs),
                            'univ':    univ,
                            'mat':     matList[-1][0],
                            'fill':    None,
                            'surfs':  '{0}'.format(radSurfList[-1])}


  if grid:
  
    # if box-type surfaces were implemented in openmc, this entire thing could be
    # skipped, and instead the grid material and box surface could be put in
    # radSurfList and matList
    
    if not surfs or not gridMat: raise Exception('need surfs and gridMat for grid')


    cells[name + 'last']['surfs'] = '{0} {1} -{2} {3} -{4}'.format(radSurfList[-1],
                                                                   surfs['rod grid box ybot {0}'.format(gridType)]['id'],
                                                                   surfs['rod grid box ytop {0}'.format(gridType)]['id'],
                                                                   surfs['rod grid box xbot {0}'.format(gridType)]['id'],
                                                                   surfs['rod grid box xtop {0}'.format(gridType)]['id'])
    
    cells[name + ' grid 1'] = {   'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    univ,
                                  'mat':     gridMat,
                                  'fill':    None,
                                  'surfs':  '-{0}'.format(surfs['rod grid box ybot {0}'.format(gridType)]['id'])}
    cells[name + ' grid 2'] = {   'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    univ,
                                  'mat':     gridMat,
                                  'fill':    None,
                                  'surfs':  '{0}'.format(surfs['rod grid box ytop {0}'.format(gridType)]['id'])}
    cells[name + ' grid 3'] = {   'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    univ,
                                  'mat':     gridMat,
                                  'fill':    None,
                                  'surfs':  '{0} -{1} {2}'.format(surfs['rod grid box xtop {0}'.format(gridType)]['id'],
                                                                  surfs['rod grid box ytop {0}'.format(gridType)]['id'],surfs['rod grid box ybot {0}'.format(gridType)]['id'])}
    cells[name + ' grid 4'] = {   'order':   inc_order(co),
                                  'comm':    "",
                                  'id':      new_id(cellIDs),
                                  'univ':    univ,
                                  'mat':     gridMat,
                                  'fill':    None,
                                  'surfs':  '-{0} -{1} {2}'.format(surfs['rod grid box xbot {0}'.format(gridType)]['id'],
                                                                   surfs['rod grid box ytop {0}'.format(gridType)]['id'],surfs['rod grid box ybot {0}'.format(gridType)]['id'])}

def make_stack(name,co,cells,univ,cellIDs,axSurfList,fillList):
  """Populates the cells dictionary with an axial stack universe
  
    name       - string, name of the cell as well as the comment to be written
    co         - cells order dictionary
    cells      - cells dictionary
    univ       - new universe id number for this stack
    cellIDs    - set of already used cell IDs
    axSurfList - list of surface IDs, from botom to top
    fillList   - list of fill universe IDs, from bottom to top.
                 length should be one more than axSurfList.
                 first fill universe will be below the first surface,
                 last fill universe will be above the last surface
  """
  
  cells[name] = { 'order':   inc_order(co),
                  'comm':    comm_t.format(name),
                  'id':      new_id(cellIDs),
                  'univ':    univ,
                  'fill':    fillList[0],
                  'surfs':  '-{0}'.format(axSurfList[0])}

  for i,(fillU,botSurf) in enumerate(zip(fillList[1:-1],axSurfList[:-1])):
    cells[name + str(i)] = {  'order':   inc_order(co),
                              'comm':    "",
                              'id':      new_id(cellIDs),
                              'univ':    univ,
                              'fill':    fillU,
                              'surfs':  '{0} -{1}'.format(botSurf,axSurfList[i+1])}
  cells[name + 'last'] = {  'order':   inc_order(co),
                            'comm':    "",
                            'id':      new_id(cellIDs),
                            'univ':    univ,
                            'fill':    fillList[-1],
                            'surfs':  '{0}'.format(axSurfList[-1])}


def make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, water, name,
                  comm=None,sect=None, dim=None,lleft=None,width=None,univs=None,
                  gridSurfs=None,sleeveMats=None):
  """Populates the cells and latts dictionary with an assembly

    The cell universe handle to use will be:  cells[name+' lattice']['univ']
  
    cells      - cells dictionary
    surfs      - surfs dictionary
    lo         - latts order dictionary
    co         - cells order dictionary
    univIDs    - set of already used universe IDs
    cellIDs    - set of already used cell IDs
    name       - string, name of the latt/cell family
    water      - material to put outside the lattice
    comm       - optional comment for the lattice and cell family
    sect       - optional section comment
    dim        - required lattice dimension
    lleft      - required lattice lower_left
    width      - required lattice width
    univs      - required lattice universe string.  Should be made with pinLattice_t
    gridSurfs  - required list of grid surface ids, from bottom to top
    sleeveMats - required materials for grid sleeves as [topbot,intermediate]

    returns list of all the created cell keys

  """

  name = str(name)

  # first make the lattice

  latts[name] =                 { 'order':   inc_order(lo),
                                  'id':      new_id(univIDs),
                                  'type':    'rectangular'}
  if comm:
    latts[name]['comm'] = comm_t.format(comm)
  else:
    latts[name]['comm'] = ""
  if sect:
    latts[name]['section'] = comm_t.format(sect)

  for key in ['dim','lleft','width','univs']:
    if not locals()[key]:
      raise Exception('make_assembly requires {0}'.format(key))
    else:
      latts[name][key] = locals()[key]
  
  # add lattice to bounding cell
  cells[name+' lattice'] =    { 'order':   inc_order(co),
                                'id':      new_id(cellIDs),
                                'univ':    new_id(univIDs),
                                'fill':    latts[name]['id'],
                                'surfs':  '-{0} {1} -{2} {3}'.format(surfs['lat box xtop']['id'],surfs['lat box xbot']['id'],surfs['lat box ytop']['id'],surfs['lat box ybot']['id'])}
  if comm:
    cells[name+' lattice']['comm'] = comm_t.format(comm)
  else:
    cells[name+' lattice']['comm'] = ""
  if sect:
    cells[name+' lattice']['section'] = comm_t.format(sect)
  
  
  # make axial all cells for outside of assembly

  # !! all of this would be greatly simplified if box-type surfaces were implemented in openmc !!
  
  outKeys = []  # we only keep track of this to facilitate certain plots/tallies
  
  # first bottom part
  cells[name+' lattice 2'] =  { 'order':   inc_order(co), 'comm':"",
                                'id':      new_id(cellIDs),
                                'univ':    cells[name+' lattice']['univ'],
                                'fill':    None,
                                'mat':     water,
                                'surfs':  '-{0} -{1}'.format(surfs['lat box ybot']['id'],gridSurfs[0])}
  outKeys.append(cells[name+' lattice 2']['id'])
  cells[name+' lattice 3'] =  { 'order':   inc_order(co), 'comm':"",
                                'id':      new_id(cellIDs),
                                'univ':    cells[name+' lattice']['univ'],
                                'fill':    None,
                                'mat':     water,
                                'surfs':  '{0} -{1}'.format(surfs['lat box ytop']['id'],gridSurfs[0])}
  outKeys.append(cells[name+' lattice 3']['id'])
  cells[name+' lattice 4'] =  { 'order':   inc_order(co), 'comm':"",
                                'id':      new_id(cellIDs),
                                'univ':    cells[name+' lattice']['univ'],
                                'fill':    None,
                                'mat':     water,
                                'surfs':  '{0} -{1} {2} -{3}'.format(surfs['lat box xtop']['id'],
                                                                surfs['lat box ytop']['id'],surfs['lat box ybot']['id'],
                                                                gridSurfs[0])}
  outKeys.append(cells[name+' lattice 4']['id'])
  cells[name+' lattice 5'] =  { 'order':   inc_order(co), 'comm':"",
                                'id':      new_id(cellIDs),
                                'univ':    cells[name+' lattice']['univ'],
                                'fill':    None,
                                'mat':     water,
                                'surfs':  '-{0} -{1} {2} -{3}'.format(surfs['lat box xbot']['id'],
                                                                 surfs['lat box ytop']['id'],surfs['lat box ybot']['id'],
                                                                 gridSurfs[0])}
  outKeys.append(cells[name+' lattice 5']['id'])

  gridnum = 0
  
  # all middle cells
  for i,botGridSurf in enumerate(gridSurfs[:-1]):
  
  
    if i%2 == 0:
      # make gridsleeve cells

      gridnum += 1
      
      if gridnum == 1 or gridnum == 8:
        smat = sleeveMats[0]
      else:
        smat = sleeveMats[1]
      
      outSurfsKey = 'lat grid box '
      inSurfsKey = 'lat box '
           
      cellKey = name+' lattice grid {0}'.format(6+i*4)
      cells[cellKey] =  { 'order':   inc_order(co), 'comm':"",
                          'id':      new_id(cellIDs),
                          'univ':    cells[name+' lattice']['univ'],
                          'fill':    None,
                          'mat':     smat,
                          'surfs':  '-{0} {1} {2} -{3} {4} -{5}'.format(surfs[inSurfsKey+'ybot']['id'],surfs[outSurfsKey+'ybot']['id'],
                                                                        surfs[outSurfsKey+'xbot']['id'],surfs[outSurfsKey+'xtop']['id'],
                                                                        botGridSurf,gridSurfs[i+1])}
      outKeys.append(cells[cellKey]['id'])
      cellKey = name+' lattice grid {0}'.format(7+i*4)
      cells[cellKey] =  { 'order':   inc_order(co), 'comm':"",
                          'id':      new_id(cellIDs),
                          'univ':    cells[name+' lattice']['univ'],
                          'fill':    None,
                          'mat':     smat,
                          'surfs':  '-{0} {1} {2} -{3} {4} -{5}'.format(surfs[outSurfsKey+'ytop']['id'],surfs[inSurfsKey+'ytop']['id'],
                                                                        surfs[outSurfsKey+'xbot']['id'],surfs[outSurfsKey+'xtop']['id'],
                                                                        botGridSurf,gridSurfs[i+1])}
      outKeys.append(cells[cellKey]['id'])
      cellKey = name+' lattice grid {0}'.format(8+i*4)
      cells[cellKey] =  { 'order':   inc_order(co), 'comm':"",
                          'id':      new_id(cellIDs),
                          'univ':    cells[name+' lattice']['univ'],
                          'fill':    None,
                          'mat':     smat,
                          'surfs':  '-{0} {1} {2} -{3} {4} -{5}'.format(surfs[inSurfsKey+'xbot']['id'],surfs[outSurfsKey+'xbot']['id'],
                                                                        surfs[inSurfsKey+'ybot']['id'],surfs[inSurfsKey+'ytop']['id'],
                                                                        botGridSurf,gridSurfs[i+1])}
      outKeys.append(cells[cellKey]['id'])
      cellKey = name+' lattice grid {0}'.format(9+i*4)
      cells[cellKey] =  { 'order':   inc_order(co), 'comm':"",
                          'id':      new_id(cellIDs),
                          'univ':    cells[name+' lattice']['univ'],
                          'fill':    None,
                          'mat':     smat,
                          'surfs':  '-{0} {1} {2} -{3} {4} -{5}'.format(surfs[outSurfsKey+'xtop']['id'],surfs[inSurfsKey+'xtop']['id'],
                                                                        surfs[inSurfsKey+'ybot']['id'],surfs[inSurfsKey+'ytop']['id'],
                                                                        botGridSurf,gridSurfs[i+1])}
      outKeys.append(cells[cellKey]['id'])
      
    else:
      outSurfsKey = 'lat box '
  
  
    cellKey = name+' lattice {0}'.format(6+i*4)
    cells[cellKey] =  { 'order':   inc_order(co), 'comm':"",
                        'id':      new_id(cellIDs),
                        'univ':    cells[name+' lattice']['univ'],
                        'fill':    None,
                        'mat':     water,
                        'surfs':  '-{0} {1} -{2}'.format(surfs[outSurfsKey+'ybot']['id'],botGridSurf,gridSurfs[i+1])}
    outKeys.append(cells[cellKey]['id'])
    cellKey = name+' lattice {0}'.format(7+i*4)
    cells[cellKey] =  { 'order':   inc_order(co), 'comm':"",
                        'id':      new_id(cellIDs),
                        'univ':    cells[name+' lattice']['univ'],
                        'fill':    None,
                        'mat':     water,
                        'surfs':  '{0} {1} -{2}'.format(surfs[outSurfsKey+'ytop']['id'],botGridSurf,gridSurfs[i+1])}
    outKeys.append(cells[cellKey]['id'])
    cellKey = name+' lattice {0}'.format(8+i*4)
    cells[cellKey] =  { 'order':   inc_order(co), 'comm':"",
                        'id':      new_id(cellIDs),
                        'univ':    cells[name+' lattice']['univ'],
                        'fill':    None,
                        'mat':     water,
                        'surfs':  '{0} -{1} {2} {3} -{4}'.format(surfs[outSurfsKey+'xtop']['id'],
                                                        surfs[outSurfsKey+'ytop']['id'],surfs[outSurfsKey+'ybot']['id'],
                                                        botGridSurf,gridSurfs[i+1])}
    outKeys.append(cells[cellKey]['id'])
    cellKey = name+' lattice {0}'.format(9+i*4)
    cells[cellKey] =  { 'order':   inc_order(co), 'comm':"",
                        'id':      new_id(cellIDs),
                        'univ':    cells[name+' lattice']['univ'],
                        'fill':    None,
                        'mat':     water,
                        'surfs':  '-{0} -{1} {2} {3} -{4}'.format(surfs[outSurfsKey+'xbot']['id'],
                                                         surfs[outSurfsKey+'ytop']['id'],surfs[outSurfsKey+'ybot']['id'],
                                                         botGridSurf,gridSurfs[i+1])}
    outKeys.append(cells[cellKey]['id'])
    
  # top part
  cells[name+' lat last 1'] = { 'order':   inc_order(co), 'comm':"",
                                'id':      new_id(cellIDs),
                                'univ':    cells[name+' lattice']['univ'],
                                'fill':    None,
                                'mat':     water,
                                'surfs':  '-{0} {1}'.format(surfs['lat box ybot']['id'],gridSurfs[-1])}
  outKeys.append(cells[name+' lat last 1']['id'])
  cells[name+' lat last 2'] = { 'order':   inc_order(co), 'comm':"",
                                'id':      new_id(cellIDs),
                                'univ':    cells[name+' lattice']['univ'],
                                'fill':    None,
                                'mat':     water,
                                'surfs':  '{0} {1}'.format(surfs['lat box ytop']['id'],gridSurfs[-1])}
  outKeys.append(cells[name+' lat last 2']['id'])
  cells[name+' lat last 3'] = { 'order':   inc_order(co), 'comm':"",
                                'id':      new_id(cellIDs),
                                'univ':    cells[name+' lattice']['univ'],
                                'fill':    None,
                                'mat':     water,
                                'surfs':  '{0} -{1} {2} {3}'.format(surfs['lat box xtop']['id'],
                                                                surfs['lat box ytop']['id'],surfs['lat box ybot']['id'],
                                                                gridSurfs[-1])}
  outKeys.append(cells[name+' lat last 3']['id'])
  cells[name+' lat last 4'] = { 'order':   inc_order(co), 'comm':"",
                                'id':      new_id(cellIDs),
                                'univ':    cells[name+' lattice']['univ'],
                                'fill':    None,
                                'mat':     water,
                                'surfs':  '-{0} -{1} {2} {3}'.format(surfs['lat box xbot']['id'],
                                                                 surfs['lat box ytop']['id'],surfs['lat box ybot']['id'],
                                                                 gridSurfs[-1])}
  outKeys.append(cells[name+' lat last 4']['id'])
  
  
  
  return outKeys # we only keep track of this to facilitate certain plots/tallies


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
