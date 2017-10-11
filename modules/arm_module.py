#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    Arm module.
"""
#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

# built-in
import pymel.core as pm

# external
from abc_autorig.utils import name_utils, meta_utils

# internal
from limb_module import BaseLimb

#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

class Arm(BaseLimb):

    POSITION = [
                [8.238, 19.246, 0.245],
                [13.623, 19.246, 0.245],
                [18.452, 19.246, 1.539]]
    ROTATION = [
                [0,0,0],
                [0, -15, 0],
                [0, -15, 0]]

    def __init__(self, char=None, side=None, node_type="arm", suffix=None,
                 cc_color=None, cc_size=1, solver="ikRPsolver",
                 control_orient=[0,0,0], mirror_module=True):
        '''
        PARAMS:
            @param char: str, the characters name used to generate the names
            @param side: str, the direction used to generate the names
            @param node_type: str, the node_type use to generate the names
            @param suffix: str, the suffix
            @param cc_color: str, what color to apply on the controls
            @param cc_size: int, size of control
            @param solver: str, solver type
            @param control_orient: array
            @param mirror_module: bool
        '''

        self.char = char
        self.side = side
        self.mirrored_side = 'r'
        if self.side == 'r':
            self.mirrored_side = 'l'
        self.node_type = node_type
        self.suffix = suffix
        self.cc_color = cc_color
        self.cc_size = cc_size
        self.solver = solver
        self.control_orient = control_orient
        self.mirror_module = mirror_module

        self.fk_chain = None
        self.ik_chain = None
        self.blend_chain = None
        self.blend_data = None

        # config
        config_name = name_utils.get_unique_name(self.char, self.side,
                                               self.node_type, "config")
        mir_config_name = name_utils.get_unique_name(self.char,
                          self.mirrored_side, self.node_type, "mirroredConfig")

        self.config_node = pm.spaceLocator(n=config_name)
        if self.mirror_module:
            self.mir_config_node = pm.spaceLocator(n=mir_config_name)

        self.guides = list()
        self.guides_grp = None

        self.in_hooks = list()
        self.out_hooks = list()
        self.hook_data = dict()

        # mirroed data
        if self.mirror_module:
            self.in_hooks_mir = list()
            self.out_hooks_mir = list()
            self.hook_data_mir = dict()

        # switching
        self.__temp_space_switch = None
        self.switch_grp = None

        # create meta node
        meta_args = [self.char, self.side, self.node_type, 0]
        self.meta = meta_utils.create_meta(*meta_args)
