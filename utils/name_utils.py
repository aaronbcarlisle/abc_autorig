#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    Name utility functions
"""
#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

# built-in
import os
from maya import OpenMaya, cmds

# external
from abc_autorig import autorig_settings

#------------------------------------------------------------------------------#
#----------------------------------------------------------------- FUNCTIONS --#

def get_unique_name(asset, side, node_type, suffix):
        """
        Builds unique name based off the following parameters.
        :parameters:
            asset: Name of the asset, i.e., Batman, car, cheetah.
            side: Right, Left, or Center (r, l, c).
            node_type: The node_type of the asset, i.e., arm, door, tail.
            suffix: The name of the object, i.e., loc, jnt, geo.
        """

        # naming convention
        root_name = '{0}_{1}_{2}0{3}_{4}'
        name = root_name.format(asset, side, node_type, str(1), suffix)

        count = 1
        while cmds.objExists(name):
            count += 1
            name = root_name.format(asset, side, node_type, count, suffix)
        return name

def header_path(icon):
    return os.path.join(autorig_settings.IMAGES_PATH, icon)
