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

if __name__ == "__main__":
  main()
