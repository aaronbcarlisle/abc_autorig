#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    Responsible for creating the IK chain.
"""
#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

# built-in
import pymel.core as pm
from maya import OpenMaya

# internal
import control
from bone_chain import BoneChain

# external
from abc_autorig.utils import name_utils

#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

class IkChain(BoneChain):
    def __init__(self, char="batman", side="l", node_type="arm", suffix='ikJ',
                 cc_color="yellow", cc_size=1, solver="ikSCsolver",
                 control_orient = [0,0,0]):
        '''
        PARAMS:
            @param char: str, the characters name used to generate the names
            @param side: str, the direction used to generate the names
            @param node_type: str, the node_type use to generate the names
            @param cc_color: str, what color to apply on the controls
            @param cc_size: float, the control size
            @param solver: str, the solver for the IK supported value:
                - ikSCsolver: simple chain
                - ikRPsolver: rotation plane

                beware if SC is provided no poleVector will be created
            @param control_orient: float [3], what orient apply on the control

        '''

        BoneChain.__init__(self, char, side, node_type, suffix)

        # class globals
        self.char = char
        self.side = side
        self.node_type = node_type
        self.suffix = 'ikJ'
        self.cc_color = cc_color
        self.cc_size = cc_size
        self.solver = solver
        self.control_orient = control_orient

        self.__accepted_solvers = ['ikSCsolver', 'ikRPsolver']

        self.ik_cc = None
        self.pole_vector_cc = None
        self.ik_handle = None
        self.ikconst = None
        self.pole_vector_const = None
        self.ik_effector = None

    def from_list(self, pos_list, orient_list, auto_orient=True, skip_last=True):
        '''
        This procedure builds a chain from the given position and orient list

        PARAMS:
            @param posList: float[3], the position list needed for the chain
            @param orientList: float[3], the orientation list needed for the chain
            @param autoOrient: bool, whather to auto orient
            @param skipLast: bool, whether or not add controls on the last bone
        '''

        if not self.__check_solver():
            return

        BoneChain.from_list(self, pos_list, orient_list, auto_orient)

        self.__add_controls()

        # build ik_handle
        ik_name = name_utils.get_unique_name(self.char, self.side,
                                             self.node_type, "ikH")

        if self.node_type == 'leg':
            self.ik_handle, self.ik_effector = pm.ikHandle(sj=self.chain[0],
                            ee=self.chain[2], solver=self.solver, n=ik_name)
        else:
            self.ik_handle, self.ik_effector = pm.ikHandle(sj=self.chain[0],
                            ee=self.chain[-1], solver=self.solver, n=ik_name)

        # constraints
        ik_name_args = [self.char, self.side, self.node_type, "pntc"]
        ik_const_name = name_utils.get_unique_name(*ik_name_args)
        self.ikconst = pm.pointConstraint(self.ik_cc.control, self.ik_handle,
                                          n=ik_const_name, mo=True)

        if self.solver == "ikRPsolver":
            args = [self.pole_vector_cc.control, self.ik_handle]
            self.pole_vector_const = pm.poleVectorConstraint(*args)

    def __add_controls(self):
        '''
        This procedure is in charge of creating and attaching the controls
        '''

        # build end control
        self.ik_cc = control.Control(self.char, self.side, self.node_type+'Ik',
                                     self.cc_size, self.cc_color)
        self.ik_cc.circle_cc()
        self.ik_cc.control_grp.rotate.set(self.control_orient)

        #snap the control
        if self.node_type == 'leg':
            pm.xform(self.ik_cc.control_grp, ws=1,
                     t=self.chain[2].getTranslation(space="world"))

        else:
            pm.xform(self.ik_cc.control_grp, ws=1,
                     t=self.chain[-1].getTranslation(space = "world"))

        if self.solver == "ikRPsolver":
            # build the poleVector
            self.pole_vector_cc = control.Control(self.char, self.side,
                                                  self.node_type + "PoleVec",
                                                  self.cc_size, self.cc_color)
            self.pole_vector_cc.sphere_cc()

            # grab joints
            joint_a = self.chain[2]
            joint_b = self.chain[0]
            joint_mid = self.chain[1]

            # finda A's Positions
            posA = pm.xform(str(joint_a), q=True, ws=True, t=True)
            a = OpenMaya.MVector(posA[0], posA[1], posA[2])

            # finda B's Positions
            posB = pm.xform(str(joint_b), q=True, ws=True, t=True)
            b = OpenMaya.MVector(posB[0], posB[1], posB[2])

            # finda C's Positions
            posC = pm.xform(str(joint_mid), q=True, ws=True, t= True)
            mid = OpenMaya.MVector(posC[0], posC[1], posC[2])

            # calculate pole vector position
            calc = a + ((b-a)*.5)
            result = calc + ((mid - (calc)) * 3)

            # snap the control
            vector = [result.x, result.y, result.z]
            pm.xform(self.pole_vector_cc.control_grp, t=vector)

    def __check_solver(self):
        '''
        this procedure checks that the given solver is valid
        @return: bool
        '''

        if not self.solver in self.__accepted_solvers:
            message = "Please provide a valid solver, "\
                    "accepted values are: " " , ".join(self.__accepted_solvers)
            return OpenMaya.MGlobal.displayError()
        return True



