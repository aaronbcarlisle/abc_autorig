#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    Base class for creating animation controls.
"""
#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

# built-in
import pymel.core as pm

# external
from abc_autorig.utils import name_utils, xform_utils

#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

class Control(object):
    def __init__(self, char="control", side="c", node_type="arm", size=1,
                 cc_color="yellow", aim_axis="x"):
        '''
        PARAMS:
            :param[in] char: str
            :param[in] side: str
            :param[in] node_type: str
            :param size: int/float
            :param cc_color: str
            :param aim_axis: str, (x, y or z)
        '''

        self.char = char
        self.side = side
        self.node_type = node_type
        self.cc_color = cc_color
        self.size = size
        self.aim_axis = aim_axis

        self.control = None
        self.control_grp = None
        self.control_name = None

    def circle_cc(self):
        '''
        This procedure creates a circle control
        '''

        self.__build_name()
        if self.control_name:
            self.control = pm.circle(name=self.control_name,
                                     ch=0, o=1, nr=[1, 0, 0])[0]

        self.__finalize_cc()

    def pin_cc(self):
        '''
        This procedure creates a pin control
        '''
        self.__build_name()
        if not self.control_name:
            return
        curve = pm.curve(d=1, p=[(0,0,0), (0.8, 0,0)], k=[0,1],
                        n=self.control_name)
        circle = pm.circle(ch=1, o=True, nr=(0,1,0), r=0.1)[0]

        pm.move(0.9, 0, 0, circle.getShape().cv, r=1)
        pm.parent(circle.getShape(), curve, shape=1, add=1)

        pm.delete(circle)
        pm.select(cl=True)
        self.control = curve

        self.__finalize_cc()

    def sphere_cc(self):
        '''
        This procedure creates a sphere
        '''
        self.__build_name()
        if self.control_name:
           self.control = pm.sphere(n=self.control_name, ax=(0,1,0), r=0.5)[0]

        self.__finalize_cc()

    def __build_name(self):
        '''
        This function creates the name of the control
        '''
        args = [self.char, self.side, self.node_type, 'cc']
        self.control_name = name_utils.get_unique_name(*args)

    def __finalize_cc(self):
        '''
        This function is in charge of orienting, scaling and zeroing the control
        '''

        self.__aim_cc()

        if self.size != 1:
            for s in self.control.getShapes():
                pm.scale(s.cv, self.size, self.size, self.size, r=1)
            pm.delete(self.control, ch=1)

        self.control_grp = xform_utils.zero(self.control)

    def __aim_cc(self):
        '''
        This procedure lets you correctly aim the control based aim_axis
        '''

        y = 0
        z = 0

        if self.aim_axis == "y":
            z = 90

        elif self.aim_axis == "z":
            y = -90

        # grabs the control vertices
        for s in self.control.getShapes():
            pm.rotate(s.cv, 0, y, z, r = 1)
            if self.cc_color == "yellow":
                s.overrideEnabled.set(True)
                s.overrideColor.set(17)
            elif self.cc_color == "blue":
                if self.side == "l":
                    s.overrideEnabled.set(True)
                    s.overrideColor.set(6)
                elif self.side == "r":
                    s.overrideEnabled.set(True)
                    s.overrideColor.set(13)
            elif self.cc_color == "red":
                if self.side == "l":
                    s.overrideEnabled.set(True)
                    s.overrideColor.set(13)
                elif self.side == "r":
                    s.overrideEnabled.set(True)
                    s.overrideColor.set(6)
