#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    Autorig Settings
"""
#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

# built-in
import os

#------------------------------------------------------------------------------#
#------------------------------------------------------------------- GLOBALS --#

# root path
ROOT_PATH = os.path.split(__file__)[0] + '/'
separator = os.sep
if separator != '/':
    ROOT_PATH = ROOT_PATH.replace(os.sep, '/')

# directories
MODULES_PATH = ROOT_PATH + 'modules/'
UI_PATH = ROOT_PATH + 'ui/'
UTILS_PATH = ROOT_PATH + 'utils/'
IMAGES_PATH = ROOT_PATH + 'images/'

# sides
SIDES = ["c", "l", "r"]

# suffixes
SUFFIXES = [
            "grp", # group
            "jj", # joints
            "loc", # locators
            "hook", # rig hooks
            "hookMirrored", # mirrored rig hooks
            "geo", # geometry
            "cc", # controls
            "ikH", # ikHandle
            "ikJ", # ikJoint
            "fkJ", # fkJoint
            "pntc", # point constraint
            "PoleVec", # poleVector
            "config", # configuration
            "mirroredConfig", # mirrored configuration
            "bln", # blendNode
            "guide", # locator guide
            "node", # a node
            "meta", # metaData
            ]

HOOKNODE_TYPE = 'locator'
METANODE_TYPE = 'lightInfo'
