#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    Meta Utility functions.
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

def create_meta(char='meta', side='c', node_type='meta', is_main=False):

    meta_name = name_utils.get_unique_name(char, side, node_type, 'meta')
    meta_node = pm.createNode(autorig_settings.METANODE_TYPE, n=meta_name)

    if autorig_settings.METANODE_TYPE == 'locator':
        meta_node = meta_node.getParent()
        meta_node.rename(meta_name)

    # add attribute
    meta_node.addAttr('isMain', at='bool', dv=0)

    if is_main:
        meta_node.attr('isMain').set(True)

    return meta_node

def add_to_meta(meta_node, meta_attr, objs=None):
    '''
    This procedure attach a node ot the given meta_node
    PARAMS:
        @param meta_node : PyNode, the attribute we want to attach
        @param meta_attr : PyNode, to which attribute we want to attach the object
        @param objs : PyNode[], the objects we want to attach
    '''

    if not meta_node.hasAttr(meta_attr):
        meta_node.addAttr(meta_attr, at='message')

    for obj in objs:
        if not obj.hasAttr('meta'):
            obj.addAttr('meta', at='message')
        meta_node.attr(meta_attr).connect(obj.attr('meta'))
