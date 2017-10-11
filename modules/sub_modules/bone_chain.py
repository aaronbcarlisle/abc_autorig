#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    Bone Chain module.
"""
#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

# built-in
import pymel.core as pm

# external
from abc_autorig.utils import name_utils

#------------------------------------------------------------------------------#
#------------------------------------------------------------------- CLASSES --#

class BoneChain(object):
    def __init__(self, char='batman', side='l', node_type='arm', suffix='jj'):
        '''
        PARAMS:
            @PARAM char: str, the character name used to generate the names
            @PARAM side: str, the side used to generate names
            @PARAM node_type: str, node type.
            @PARAM suffix: str, suffix
        '''

        self.char = char
        self.side = side
        self.node_type = node_type
        self.suffix = suffix

        self.chain = list()

    def from_list(self, pos_list, orient_list, auto_orient=True):
        '''
        This procedure lets you create a chain from a list of points and orient
        PARAMS:
            @PARAM pos_list: float[3], the  position list needed for the chain
            @PARAM orient_list: float[3], the orientation list needed for the chain
            @PARAM auto_orient: bool, whether to auto_orient
        '''
        for i in xrange(len(pos_list)):

            # build uniqe name
            temp_args = [self.char, self.side, self.node_type, self.suffix]
            temp_name = name_utils.get_unique_name(*temp_args)

            # clear selection
            pm.select(cl=1)

            # build the joint
            if not auto_orient:
                temp_jnt = pm.joint(n=temp_name, position=pos_list[i])
            else:
                temp_jnt = pm.joint(n=temp_name, position=pos_list[i],
                                    orientation=orient_list[i])
            self.chain.append(temp_jnt)

        self.__parent_joint()

        if not auto_orient:
            pm.joint(self.chain[0].name(), e=True, oj='xyz',
                     secondaryAxisOrient='zup', ch=True, zso=True)

        # orients last joint in chain
        self.__zero_orient_joint(self.chain[-1])

    def __str__(self):
        result = "BoneChain class, length: {l}, chain: ".format(l=self.chain_length())
        chain_name = [obj.name() for obj in self.chain]
        result += str(chain_name)

        return result

    def chain_length(self):
        '''
        This procedure returns the length of the created chain
        '''
        return len(self.chain)

    def __zero_orient_joint(self, bone):
        '''
        This procedure zero outs the jointOrient attribute of a bone
        PARAMS:
            @param bone: PyNode, the bone to zero out the jointOrient
        '''
        for attribute in ["jointOrientX", "jointOrientY", "jointOrientZ"]:
            bone.attr(attribute).set(0)

    def __parent_joint(self):
        '''
        This procedure parents with each other a list of joints
        '''
        chain_reversed = list(self.chain)
        chain_reversed.reverse()

        for i in xrange(len(chain_reversed)):
            if i != (len(chain_reversed)-1):
                pm.parent(chain_reversed[i], chain_reversed[i + 1])

    @staticmethod
    def blend_two_chains(chain_one, chain_two, result_chain, attr_holder,
                         attr_name, char_name, side, node_type):
        '''
        This procedure will blend two provided chains
        PARAMS:
            @param chain_one: PyNode[] , the first chain you want to blend
            @param chain_two: PyNode[] , the second chain you want to blend
            @param result_chain: PyNode[] , the blended chain
            @param attr_holder: PyNode , the node holding the attribute for the switch
            @param attr_name: str, the nae of the attribute used for the blend
            @param baseName: str, the base name used to generate the names
            @param side: str, the side used to generate names
            @return: dict
        '''

        blend_t_array = list()
        blend_r_array = list()
        blend_s_array = list()
        data = {"blendTranslate" : blend_t_array,
                "blendRotate" : blend_r_array,
                "blendScale" : blend_s_array, }

        if not attr_holder.hasAttr(attr_name):
            attr_holder.addAttr(attr_name, at="float", min=0, max=1, dv=0, k=1)

        for count, bone in enumerate(result_chain):
            blnt = name_utils.get_unique_name(char_name, side, node_type, "bln")
            blnr = name_utils.get_unique_name(char_name, side, node_type, "bln")
            blns = name_utils.get_unique_name(char_name, side, node_type, "bln")
            if not blnt or not blnr or not blns:
                return

            blend_node_t = pm.createNode("blendColors", n=blnt)
            blend_node_r = pm.createNode("blendColors", n=blnr)
            blend_node_s = pm.createNode("blendColors", n=blns)

            # connect translate
            chain_two[count].t.connect(blend_node_t.color2)
            chain_one[count].t.connect(blend_node_t.color1)

            # connect rotate
            chain_two[count].r.connect(blend_node_r.color2)
            chain_one[count].r.connect(blend_node_r.color1)

            # connect scale
            chain_two[count].s.connect(blend_node_s.color2)
            chain_one[count].s.connect(blend_node_s.color1)

            blend_node_t.output.connect(bone.t)
            blend_node_r.output.connect(bone.r)
            blend_node_s.output.connect(bone.s)

            blend_t_array.append(blend_node_t)
            blend_r_array.append(blend_node_r)
            blend_s_array.append(blend_node_s)

            attr_holder.attr(attr_name).connect(blend_node_t.blender)
            attr_holder.attr(attr_name).connect(blend_node_r.blender)
            attr_holder.attr(attr_name).connect(blend_node_s.blender)

        return data
