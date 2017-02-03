from surfaces import surfs

# FIXME: Add docstring explanation
# FIXME: Put this in surface.py??

# FIXME: Use get_rectangular_prism method instead???

grids = {}

grids['inner grid box (intermediate)'] = (+surfs['rod grid box ybot i'] &
                                          -surfs['rod grid box ytop i'] &
                                          +surfs['rod grid box xbot i'] &
                                          -surfs['rod grid box xtop i'])

grids['outer grid box (intermediate)'] = (-surfs['rod grid box ybot i']) | \
                                         (+surfs['rod grid box ytop i']) | \
                                         (+surfs['rod grid box xtop i'] &
                                          -surfs['rod grid box ytop i'] &
                                          +surfs['rod grid box ybot i']) | \
                                         (-surfs['rod grid box xbot i'] &
                                          -surfs['rod grid box ytop i'] &
                                          +surfs['rod grid box ybot i'])

grids['inner grid box (top/bottom)'] = (+surfs['rod grid box ybot tb'] &
                                        -surfs['rod grid box ytop tb'] &
                                        +surfs['rod grid box xbot tb'] &
                                        -surfs['rod grid box xtop tb'])

grids['outer grid box (top/bottom)'] = (-surfs['rod grid box ybot tb']) | \
                                       (+surfs['rod grid box ytop tb']) | \
                                       (+surfs['rod grid box xtop tb'] &
                                        -surfs['rod grid box ytop tb'] &
                                        +surfs['rod grid box ybot tb']) | \
                                       (-surfs['rod grid box xbot tb'] &
                                        -surfs['rod grid box ytop tb'] &
                                        +surfs['rod grid box ybot tb'])