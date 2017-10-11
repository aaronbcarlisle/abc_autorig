#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    xform utility functions
"""
#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

# built-in
from maya import OpenMaya
import pymel.core as pm

# internal
import name_utils

#------------------------------------------------------------------------------#
#----------------------------------------------------------------- FUNCTIONS --#

def zero(obj):
    '''
    This procedure gets a input as pymel object and group it in order
    to zero out the transform
    PARAMS:
        @param obj: PyNode, the object to zero out
        @return PyNode , the offset group
    '''

    # Get parent object
    parent = obj.getParent()

    # Create group name
    temp = obj.name().split("_")

    grp_args = [temp[0].split('0')[0], temp[1], temp[2].split('0')[0], "grp"]
    grp_name = name_utils.get_unique_name(*grp_args)
    if not grp_name:
        OpenMaya.MGlobal.displayError('ERROR generating name')
        return

    grp = pm.createNode("transform", n=grp_name)

    matrix = obj.wm.get()
    grp.setMatrix(matrix)

    # rebuild the hierarchy
    obj.setParent(grp)
    if parent:
        grp.setParent(parent)
    return grp
