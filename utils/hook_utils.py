#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    Hook utility functions
"""
#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

# built-in
import pymel.core as pm

# external
from abc_autorig import autorig_settings

# internal
import name_utils

#------------------------------------------------------------------------------#
#----------------------------------------------------------------- FUNCTIONS --#

def create_hook(char='character', side='c', node_type='spine',
                suffix='hook', snap_to=None, in_out='in'):

    # data
    hook_name = name_utils.get_unique_name(char, side, node_type, suffix)
    hook_node = pm.createNode(autorig_settings.HOOKNODE_TYPE, n=hook_name)

    # rename
    if autorig_settings.HOOKNODE_TYPE == 'locator':
        hook_node = hook_node.getParent()
        hook_node.rename(hook_name)

    digitType = 0
    if in_out == 'out':
        digitType = 1

    hook_node.addAttr('hookType', at='float', dv=digitType)
    hook_node.attr('hookType').lock(1)
    if snap_to:
        pm.xform(hook_node, ws=True, matrix=snap_to.wm.get())

    return hook_node
