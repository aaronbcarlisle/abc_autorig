#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    Main reloader for abc_autorig
"""
#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

# built-in
from maya import OpenMaya

# internal
from abc_autorig import autorig_settings
from abc_autorig.modules import modules_reload
from abc_autorig.utils import utils_reload
from abc_autorig.ui import ui_reload
from abc_autorig.core import core_reload

#------------------------------------------------------------------------------#
#----------------------------------------------------------------- FUNCTIONS --#

def reload_main():

    reload(autorig_settings)
    reload(ui_reload)
    reload(utils_reload)
    reload(core_reload)
    reload(modules_reload)

    utils_reload.reload_utils()
    ui_reload.reload_ui()
    core_reload.reload_core()
    modules_reload.reload_modules()

    return OpenMaya.MGlobal_displayInfo("----------> MAIN RELOAD: OK")
