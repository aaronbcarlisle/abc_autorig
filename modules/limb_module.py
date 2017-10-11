#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    Base Limb Module

    This module is built for inheritance, not for use. Both the leg and arm
    modules inherit from this module. Since legs and arms share basically the
    same functionality, we'll save some work. If we want to diverge,
    we can override in the individual classes.
"""
#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

# built-in
import os
import pymel.core as pm
import maya.mel as mel

# external
from abc_autorig.ui import autorig_ui
from abc_autorig.modules.sub_modules.bone_chain import BoneChain
from abc_autorig.modules.sub_modules import fk_chain, ik_chain
from abc_autorig.utils import name_utils, hook_utils, meta_utils

#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

class BaseLimb(object):

    POSITION = None
    ROTATION = None

    def __init__(self, char, side, node_type, suffix, cc_color, cc_size,
                 solver, control_orient, mirror_module):
        '''
        PARAMS: (all must be met)
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

    def build_guides(self):
        for tr, rt in zip(self.POSITION, self.ROTATION):
            name = name_utils.get_unique_name(self.char, self.side,
                                              self.node_type, 'guide')
            loc = pm.spaceLocator(n=name)
            loc.t.set(tr)
            loc.r.set(rt)
            self.guides.append(loc)

        reversed_guides = list(self.guides)
        reversed_guides.reverse()
        for i in xrange(len(reversed_guides)):
            if i != (len(reversed_guides)-1):
                pm.parent(reversed_guides[i] , reversed_guides[i+1])

        name = name_utils.get_unique_name(self.char + 'Guides', self.side,
                                          self.node_type, 'grp')
        self.guides_grp = pm.group(self.guides[0], n=name)
        name_args = [self.char, self.side, self.node_type + "Main", "grp"]
        main_grp_name = name_utils.get_unique_name(*name_args)
        self.main_grp = pm.group(empty=1, n=main_grp_name)

        if self.mirror_module:
            mir_name_args = [self.char, self.mirrored_side,
                             self.node_type+"MirroredMain", "grp"]
            main_grp_mir_name = name_utils.get_unique_name(*mir_name_args)
            self.main_grp_mir = pm.group(empty=True, n=main_grp_mir_name)

        self.guides_grp.setParent(self.main_grp)

        self.__build_hooks()

    def build(self):
        # grab guide locations
        guides_pos = [x.getTranslation(space="world") for x in self.guides]
        guides_rot = [x.getRotation(space="world") for x in self.guides]

        # first build the fk
        self.fk_chain = fk_chain.FkChain(self.char, self.side, self.node_type,
                                    self.suffix, self.cc_color, self.cc_size)
        self.fk_chain.from_list(guides_pos, guides_rot)

        # build ik chain
        self.ik_chain = ik_chain.IkChain(self.char, self.side, self.node_type,
                                    self.suffix, self.cc_color, self.cc_size,
                                    self.solver, self.control_orient)
        self.ik_chain.from_list(guides_pos, guides_rot)

        # now blend them
        self.blend_chain = BoneChain(self.char, self.side,
                                                self.node_type, self.suffix)
        self.blend_chain.from_list(guides_pos, guides_rot)

        # blend data
        data_args = [self.fk_chain.chain, self.ik_chain.chain,
                     self.blend_chain.chain, self.config_node,"ikFk",
                     self.char, self.side, self.node_type]
        self.blend_data = BoneChain.blend_two_chains(*data_args)

        # mirror
        if self.mirror_module:

            # mirrored guide locations
            mir_guides_pos = [(x[0] * -1, x[1]* 1, x[2]* 1) for x in guides_pos]
            mir_guides_rot = [(x[0] * -1, x[1]* -1 + 180, x[2]* -1) for x in guides_rot]

            # build Mirrored fk
            fk_args = [self.char, self.mirrored_side, self.node_type,
                       self.suffix, self.cc_color, self.cc_size]
            self.fk_chain_mir = fk_chain.FkChain(*fk_args)
            self.fk_chain_mir.from_list(mir_guides_pos, mir_guides_rot)

            # build Mirrored ik chain
            ik_args = [self.char, self.mirrored_side, self.node_type,
                       self.suffix, self.cc_color, self.cc_size, self.solver,
                       self.control_orient]
            self.ik_chain_mir = ik_chain.IkChain(*ik_args)
            self.ik_chain_mir.from_list(mir_guides_pos, mir_guides_rot)

            # now blend the Mirrored chains
            blend_args = [self.char, self.mirrored_side,
                          self.node_type, self.suffix]
            self.blend_chain_mir = BoneChain(*blend_args)
            self.blend_chain_mir.from_list(mir_guides_pos, mir_guides_rot)

            # mirrored blend data
            BoneChain.blend_two_chains(self.fk_chain_mir.chain,
                                       self.ik_chain_mir.chain,
                                       self.blend_chain_mir.chain,
                                       self.mir_config_node, "ikFk", self.char,
                                       self.mirrored_side, self.node_type)

        # set hooks and cleanup
        self.__setup_hooks()
        self.__cleanup()

    def build_connections(self):
        pass

    def __cleanup(self):

        bones_grp_name = name_utils.get_unique_name(self.char, self.side,
                                            self.node_type + "Bones", "grp")
        self.bones_grp = pm.group(empty=True, n =bones_grp_name)
        self.bones_grp.setMatrix(self.blend_chain.chain[0].wm.get())

        # set parent
        for bone in (self.ik_chain, self.fk_chain, self.blend_chain):
            bone.chain[0].setParent(self.bones_grp)

        cc_grp_name = name_utils.get_unique_name(self.char, self.side,
                                            self.node_type + "Controls", "grp")
        self.cc_grp = pm.group(self.fk_chain.controls[0].control_grp,
                               self.ik_chain.ik_cc.control_grp,
                               self.ik_chain.pole_vector_cc.control_grp,
                               n=cc_grp_name)



        for o in (self.bones_grp, self.cc_grp,
                  self.ik_chain.ik_handle, self.config_node):
            o.setParent(self.main_grp)

        # connect to hooks
        for hook in (self.in_hooks + self.out_hooks + [self.switch_grp,
                     self.ik_chain.ik_handle, self.bones_grp]):
            hook.v.set(0)

        # parent constraint hook locator for spaceswitch to fkSwitch
        p_args = [self.__temp_space_switch, self.fk_chain.controls[0].control_grp]
        pm.parentConstraint(*p_args, mo=True)
        pm.parentConstraint(self.__temp_space_switch, self.bones_grp, mo=True)

        pm.delete(self.guides_grp)

        # connect everything to meta
        meta_utils.add_to_meta(self.meta, 'in_hooks', self.in_hooks)
        meta_utils.add_to_meta(self.meta, 'out_hooks', self.out_hooks)
        meta_utils.add_to_meta(self.meta, 'config', [self.config_node])
        meta_utils.add_to_meta(self.meta, 'skin_bones', self.blend_chain.chain)
        meta_utils.add_to_meta(self.meta, 'fk_bones', self.fk_chain.chain)
        meta_utils.add_to_meta(self.meta, 'ik_bones', self.ik_chain.chain)
        controls = ([c.control for c in self.fk_chain.controls] +
                    [self.ik_chain.pole_vector_cc.control,
                     self.ik_chain.ik_cc.control])
        meta_utils.add_to_meta(self.meta, 'controls', controls)
        meta_utils.add_to_meta(self.meta, 'main_grp', [self.main_grp])

        # mirror
        if self.mirror_module:
            mir_bones_grp_name = name_utils.get_unique_name(self.char,
                self.mirrored_side, self.node_type + "MirroredBones", "grp")
            self.mir_bones_grp = pm.group(empty=True, n=mir_bones_grp_name)
            self.mir_bones_grp.setMatrix(self.blend_chain_mir.chain[0].wm.get())

            for bone in (self.ik_chain_mir,
                         self.fk_chain_mir,self.blend_chain_mir):
                bone.chain[0].setParent(self.mir_bones_grp)

            mir_cc_grp_name = name_utils.get_unique_name(self.char,
                                    self.mirrored_side,
                                    self.node_type + "MirroredControls", "grp")
            self.mir_cc_grp = pm.group(self.fk_chain_mir.controls[0].control_grp,
                                   self.ik_chain_mir.ik_cc.control_grp,
                                   self.ik_chain_mir.pole_vector_cc.control_grp,
                                   n=mir_cc_grp_name)

            for o in (self.mir_bones_grp, self.mir_cc_grp,
                      self.ik_chain_mir.ik_handle, self.mir_config_node):
                o.setParent(self.main_grp_mir)

            # connect to hooks
            for hook in (self.in_hooks_mir + self.out_hooks_mir +
                         [self.switch_grp_mir, self.ik_chain_mir.ik_handle,
                          self.mir_bones_grp]):
                hook.v.set(0)

            # parent constraint hook locator for spaceswitch to fkSwitch
            pm.parentConstraint(self.__temp_space_switch_mir,
                          self.fk_chain_mir.controls[0].control_grp, mo=True)
            pm.parentConstraint(self.__temp_space_switch_mir,
                          self.mir_bones_grp, mo=True)

    def __build_hooks(self):
        """Builds the hook system"""
        for x in xrange(3):
            hook = hook_utils.create_hook(char=self.char, side=self.side,
                                      node_type=self.node_type+'Out',
                                      in_out='out')

            hook.setParent(self.main_grp)
            hook.v.set(0)
            self.out_hooks.append(hook)

        hook = hook_utils.create_hook(char=self.char, side=self.side,
                                      node_type=self.node_type+'In',
                                      in_out='in')

        hook.v.set(0)
        hook.setParent(self.main_grp)
        self.in_hooks.append(hook)

        # mirror
        if self.mirror_module:
            for x in xrange(3):

                mir_hook = hook_utils.create_hook(char=self.char,
                        side=self.mirrored_side, node_type=self.node_type+'Out',
                        in_out='out', suffix='hookMirrored')

                mir_hook.setParent(self.main_grp_mir)
                mir_hook.v.set(0)
                self.out_hooks_mir.append(mir_hook)

            mir_hook = hook_utils.create_hook(char=self.char,
                        side=self.mirrored_side, node_type=self.node_type+'In',
                        in_out='in', suffix='hookMirrored')

            mir_hook.v.set(0)
            mir_hook.setParent(self.main_grp_mir)
            self.in_hooks_mir.append(mir_hook)

    def __setup_hooks(self):
        for hook, bone in zip(self.out_hooks, self.blend_chain.chain):
            hook.setParent(bone)
            pm.xform(hook, ws=1, matrix=bone.wm.get())

        pm.xform(self.in_hooks[0], ws=1,
                matrix=self.blend_chain.chain[0].wm.get())

        # build space switch
        world_name = name_utils.get_unique_name(self.char, self.side,
                                                self.node_type + 'World', 'loc')
        world_loc = pm.spaceLocator(n=world_name)

        local_name = name_utils.get_unique_name(self.char, self.side,
                                                self.node_type + 'Local', 'loc')
        local_loc = pm.spaceLocator(n=local_name)

        pm.xform(world_loc, ws=1, matrix=self.in_hooks[0].wm.get())
        pm.xform(local_loc, ws=1, matrix=self.in_hooks[0].wm.get())

        pm.parentConstraint(self.in_hooks[0], local_loc, mo=True)
        pm.parentConstraint(self.in_hooks[0], world_loc,
                            skipRotate=['x', 'y', 'z'], mo=True)
        pm.orientConstraint(self.main_grp, world_loc, mo=True)

        target_name = name_utils.get_unique_name(self.char, self.side,
                                                 self.node_type+'Target', 'loc')
        self.__temp_space_switch = pm.spaceLocator(n=target_name)

        self.config_node.addAttr('fkSpace', at='enum', en='World:Local:', k=1)

        f_constraint = pm.parentConstraint(world_loc, local_loc,
                                           self.__temp_space_switch)

        self.config_node.attr('fkSpace').connect(f_constraint.attr(local_loc.name() + 'W1'))

        rev = pm.createNode('reverse')
        self.config_node.attr('fkSpace').connect(rev.inputX)
        rev.outputX.connect(f_constraint.attr(world_loc.name() + 'W0'))

        switch_name = name_utils.get_unique_name(self.char, self.side,
                                            self.node_type + 'Switch', 'grp')
        self.switch_grp = pm.group(n=switch_name, empty=True)

        for o in [world_loc, local_loc, self.__temp_space_switch] + self.in_hooks:
            o.setParent(self.switch_grp)

        self.switch_grp.setParent(self.main_grp)

        # mirror
        if self.mirror_module:
            for hook, bone in zip(self.out_hooks_mir,
                                  self.blend_chain_mir.chain):
                hook.setParent(bone)
                pm.xform(hook, ws=1, matrix=bone.wm.get())

            pm.xform(self.in_hooks_mir[0], ws=1,
                     matrix=self.blend_chain_mir.chain[0].wm.get())

            # build space switch
            world_mir_name = name_utils.get_unique_name(self.char,
                    self.mirrored_side, self.node_type + 'MirroredWorld', 'loc')
            world_loc_mir = pm.spaceLocator(n=world_mir_name)

            local_mir_name = name_utils.get_unique_name(self.char,
                    self.mirrored_side, self.node_type + 'MirroredLocal', 'loc')
            local_loc_mir = pm.spaceLocator(n=local_mir_name)

            pm.xform(world_loc_mir, ws=1, matrix=self.in_hooks_mir[0].wm.get())
            pm.xform(local_loc_mir, ws=1, matrix=self.in_hooks_mir[0].wm.get())

            # add constraints
            pm.parentConstraint(self.in_hooks_mir[0], local_loc_mir, mo=True)
            pm.parentConstraint(self.in_hooks_mir[0], world_loc_mir,
                                skipRotate = ['x', 'y', 'z'], mo=True)
            pm.orientConstraint(self.main_grp_mir, world_loc_mir, mo=True)

            target_name_mir = name_utils.get_unique_name(self.char,
                                    self.mirrored_side,
                                    self.node_type + 'MirroredTarget', 'loc')
            self.__temp_space_switch_mir = pm.spaceLocator(n=target_name_mir)

            self.mir_config_node.addAttr('fkSpace', at='enum',
                    en='World:Local:', k=1)

            final_c_mir = pm.parentConstraint(world_loc_mir, local_loc_mir,
                                              self.__temp_space_switch_mir)

            self.mir_config_node.attr('fkSpace').connect(final_c_mir.attr(local_loc_mir.name() + 'W1'))

            rev_mir = pm.createNode('reverse')
            self.mir_config_node.attr('fkSpace').connect(rev_mir.inputX)
            rev_mir.outputX.connect(final_c_mir.attr(world_loc_mir.name() + 'W0'))

            switch_name_mir = name_utils.get_unique_name(self.char,
                                    self.mirrored_side,
                                    self.node_type + 'MirroredSwitch', 'grp')
            self.switch_grp_mir = pm.group(n=switch_name_mir, empty=1)

            for o in ([world_loc_mir, local_loc_mir,
                      self.__temp_space_switch_mir] + self.in_hooks_mir):
                o.setParent(self.switch_grp_mir)

            self.switch_grp_mir.setParent(self.main_grp_mir)

    def set_hooks(self):
        pass

