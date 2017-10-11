#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    UI Widget for the leg module
"""
#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

# external
from abc_autorig.modules.leg_module import Leg

# internal
from abc_autorig.ui.limb_module_ui import BaseLimbModuleUI

#------------------------------------------------------------------------------#
#----------------------------------------------------------------- FUNCTIONS --#

def get_ui(parent, ui):
    return LegModuleUI(parent, ui)

#------------------------------------------------------------------------------#
#------------------------------------------------------------------- CLASSES --#


class LegModuleUI(BaseLimbModuleUI):

    MODULE = Leg
    MODULE_TYPE = "leg"

    def __init__(self, parent, ui):
        self.module_widget(parent)
