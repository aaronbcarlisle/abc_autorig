#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    Main reloader for modules.
"""
#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

# built-in
from maya import OpenMaya

# internal
from sub_modules import control, bone_chain, fk_chain, ik_chain

# modules
import arm_module
import leg_module
import main_module

#------------------------------------------------------------------------------#
#----------------------------------------------------------------- FUNCTIONS --#

def reload_modules():

    # sub modules
    reload(control)
    reload(bone_chain)
    reload(fk_chain)
    reload(ik_chain)

    # modules
    reload(arm_module)
    reload(leg_module)
    reload(main_module)

    return OpenMaya.MGlobal_displayInfo("-------------> MODULES RELOAD: OK")
