#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    Builds a standard FK chain.
"""
#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

# built-in
import pymel.core as pm

# internal
import control
from bone_chain import BoneChain

#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

class FkChain(BoneChain):
    def __init__(self, char="batman", side="l", node_type="arm", suffix='fkJ',
                 cc_color="yellow", cc_size=1):
        '''
        This is the constructor
        @param char: str, the character name used to generate the names
        @param side: str, the side used to generate names
        @param node_type: the type of node used to generate the names
        @param cc_color: str, what color to apply on the controls
        @param cc_size: float, the control size
        '''

        BoneChain.__init__(self, char, side, node_type, suffix)

        self.char = char
        self.side = side

        self.node_type = node_type
        if self.node_type == 'spine':
            self.suffix = 'jj'
        elif self.node_type == 'neck':
            self.suffix = 'jj'
        elif self.node_type == 'head':
            self.suffix = 'jj'
        else:
            self.suffix = 'fkJ'

        self.cc_color = cc_color
        self.cc_size = cc_size

        self.controls = list()

    def from_list(self, pos_list, orient_list, auto_orient=True, skip_last=True):
        '''
        PARAMS:
            @param pos_list: float[3] the position list needed for the chain
            @param orient_list: float[3] the orientation list needed for the chain
            @param auto_orient: bool, whether to auto_orient the list
            @param skip_last: bool, whether or not to add controls on the last bone
        '''

        BoneChain.from_list(self, pos_list, orient_list, auto_orient)

        self.__add_controls(skip_last)
        self.__finalize_fk_chain()

    def __add_controls(self, skip_last):
        '''
        This procedure is in charge of creating and attaching the controls
        to the chain

        PARAMS:
            @param skip_last: bool, whether or not add controls on the last bone
        '''
        for i in xrange(self.chain_length()):
            if skip_last:
                if i == (self.chain_length()-1):
                    return

            control_obj = control.Control(self.char, self.side,
                                       self.node_type + 'Fk',
                                       self.cc_size, self.cc_color)
            control_obj.circle_cc()

            # snap the control
            pm.xform(control_obj.control_grp, ws=1,
                     matrix=self.chain[i].worldMatrix.get())

            self.controls.append(control_obj)

    def __finalize_fk_chain(self):
        reversed_controls = list(self.controls)
        reversed_controls.reverse()

        for i in xrange(len(reversed_controls)):
            if i != (len(reversed_controls)-1):
                pm.parent(reversed_controls[i].control_grp,
                          reversed_controls[i + 1].control)

        for count, control in enumerate(self.controls):
            pm.parentConstraint(control.control, self.chain[count], mo=True)

