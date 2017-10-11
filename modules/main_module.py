#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    Main Module
"""
#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

# built-in
import pymel.core as pm
import maya.cmds as cmds

# internal
from abc_autorig.modules.sub_modules import control
from abc_autorig.utils import name_utils, hook_utils, meta_utils

#------------------------------------------------------------------------------#
#------------------------------------------------------------------- CLASSES --#


class Main(object):

    def __init__(self, char='main', side='c', node_type='arm',
                 cc_color='yellow', cc_size=1):

        '''
        PARAMS:
            @param char: str, the char name is used ot generate the names
            @param side: str, the side used to generate names
            @param node_type: str, type of node
            @param cc_color: str, what color to apply on the controls
            @param cc_size: int, size of control
        '''

        self.char = char
        self.side = side
        self.node_type = node_type
        self.cc_color = cc_color
        self.cc_size = cc_size

        self.main_control = None
        self.in_hooks = list()
        self.out_hooks = list()

        config_args = [self.char, self.side, self.node_type, 'config']
        config_name = name_utils.get_unique_name(*config_args)
        self.config_node = pm.spaceLocator(n=config_name)

        # create metaNode
        meta_args = [self.char, self.side, self.node_type, 1]
        self.meta = meta_utils.create_meta(*meta_args)

    def build_guides(self):
        args = [self.char, self.side, self.node_type + 'Main', 'grp']
        self.main_grp = pm.group(empty=1, n=name_utils.get_unique_name(*args))

        # create hook
        hook_args = [self.char, self.side, self.node_type + 'Out', "hook",
                       self.main_grp, 'out']
        hook = hook_utils.create_hook(*hook_args)

        hook.setParent(self.main_grp)
        self.out_hooks.append(hook)
        self.config_node.setParent(self.main_grp)

    def build(self):

        ctrl_args = [self.char, self.side, self.node_type, self.cc_size,
                       self.cc_color, 'y']
        self.main_control = control.Control(*ctrl_args)

        self.main_control.circle_cc()

        self.main_control.control_grp.setParent(self.main_grp)
        self.config_node.setParent(self.main_grp)
        self.out_hooks[0].setParent(self.main_control.control)

        # clean the scale
        self.main_control.control.addAttr('globalScale', at='float',
                                          min=0.001, dv=1, k=1)
        for attribute in ['sx', 'sy', 'sz']:
            atr_args = [self.main_control.control.attr(attribute)]
            self.main_control.control.attr('globalScale').connect(*atr_args)
            self.main_control.control.attr(attribute).lock()
            self.main_control.control.attr(attribute).setKeyable(0)
            self.main_control.control.attr(attribute).showInChannelBox(0)

        self.__cleanup()

    def build_connections(self):
        pass

    def __cleanup(self):

        # connect everything to meta
        meta_utils.add_to_meta(self.meta, 'out_hooks', self.out_hooks)
        meta_utils.add_to_meta(self.meta, 'main_grp', [self.main_grp])
        meta_utils.add_to_meta(self.meta, 'controls', [self.main_control.control])

        for hook in self.out_hooks:
            hook.v.set(0)
        self.config_node.v.set(0)

    def set_hooks(self):
        pass

