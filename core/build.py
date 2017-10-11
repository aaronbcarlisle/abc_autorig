#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    Build Core.
"""
#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

# built-in
import os
from maya import OpenMaya
import pymel.core as pm

# internal
from abc_autorig import autorig_settings

#------------------------------------------------------------------------------#
#------------------------------------------------------------------- CLASSES --#


class Build(object):

    def __init__(self):

        # globals
        self.modules = list()
        self.__folders_to_exclude = ["sub_modules"]
        self.__files_to_exclude = ["__init__.py", "limb_module.py", 
                                   "modules_reload.py"]
        self.modules = dict()
        self.available_modules = list()

        # entry
        self.get_available_modules()

    def get_available_modules(self):

        path = autorig_settings.ROOT_PATH + 'modules/'
        self.__check_path(path)

    def __check_path(self, path):
        dir_list = os.listdir(path)
        for dir_item in dir_list:
            if (dir_item not in self.__folders_to_exclude
                and os.path.isdir(path + dir_item)):

                self.__check_path(path + '/' + dir_item)

            if dir_item.endswith(".py") and "module" in dir_item:
                if dir_item not in self.__files_to_exclude:
                    self.available_modules.append(dir_item)
                    self.modules[dir_item] = path + dir_item

    def build_guides(self):
        for module in self.modules:
            module.build_guides()

    def build(self):
        for module in self.modules:
            module.build()

    def build_connections(self):
        for module in self.modules:
            module.build_connections()

        self.__cleanup()

    def __cleanup(self):
        for module in self.modules[1:]:
            grp_args = [self.modules[0].main_control.control, module.main_grp]
            pm.parentConstraint(*grp_args, mo=True)
            pm.scaleConstraint(*grp_args, mo=True)
            try:
                mir_args = [self.modules[0].main_control.control,
                            module.main_grp_mir]
                pm.parentConstraint(*mir_args, mo=True)
                pm.scaleConstraint(*mir_args, mo=True)
            except AttributeError:
                message = "There are no Mirrored Modules"
                return OpenMaya.MGlobal_displayWarning(message)
