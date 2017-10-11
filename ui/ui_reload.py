#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    Main reloader for ui.
"""
#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

# built-in
from maya import OpenMaya

# internal
import autorig_ui
import main_module_ui
import arm_module_ui
import limb_module_ui

#------------------------------------------------------------------------------#
#----------------------------------------------------------------- FUNCTIONS --#

def reload_ui():
    reload(limb_module_ui)
    reload(main_module_ui)
    reload(arm_module_ui)
    reload(autorig_ui)

    return OpenMaya.MGlobal_displayInfo("-------------> UI RELOAD: OK")

