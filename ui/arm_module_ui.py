#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    UI Widget for the arm module
"""
#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

# external
from abc_autorig.modules.arm_module import Arm

# internal
from abc_autorig.ui.limb_module_ui import BaseLimbModuleUI

#------------------------------------------------------------------------------#
#----------------------------------------------------------------- FUNCTIONS --#

def get_ui(parent, ui):
    return ArmModuleUI(parent, ui)

#------------------------------------------------------------------------------#
#------------------------------------------------------------------- CLASSES --#


class ArmModuleUI(BaseLimbModuleUI):

    MODULE = Arm
    MODULE_TYPE = "arm"

    def __init__(self, parent, ui):
        self.module_widget(parent)
