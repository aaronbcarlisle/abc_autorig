#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    UI Widget for the base limb module
"""
#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

# built-in
from maya import OpenMaya
import pymel.core as pm

# third-party
from PySide import QtGui, QtCore

# external
from abc_autorig.utils.name_utils import header_path
from abc_autorig import autorig_settings

#------------------------------------------------------------------------------#
#----------------------------------------------------------------- FUNCTIONS --#

def get_ui(parent, ui):
    return BaseLimbModuleUI(parent, ui)

#------------------------------------------------------------------------------#
#------------------------------------------------------------------- CLASSES --#


class BaseLimbModuleUI(object):

    MODULE = None
    MODULE_TYPE = None

    def __init__(self, parent, ui):
        self.module_widget(parent)

    def module_widget(self, parent):
        # create window
        window = QtGui.QMainWindow()
        window.setStyleSheet('QMainWindow{border-color: #fff;}')
        window.setMaximumSize(265, 400)
        window.setMinimumSize(265, 400)

        # create base widget
        self.widget = QtGui.QWidget()
        window.setCentralWidget(self.widget)

        # create main layout
        self.main_layout =  QtGui.QVBoxLayout(self.widget)

        # set title text
        self.header_widget = QtGui.QLabel()
        self.header_widget.setMaximumSize(260, 50)
        self.header_widget.setMinimumSize(260, 50)
        self.header_path = header_path(self.MODULE_TYPE + 'ModuleHeader.png')
        self.image_header = QtGui.QPixmap(self.header_path)
        self.header_widget.setPixmap(self.image_header)

        # set header image
        self.header_layout = QtGui.QHBoxLayout()
        self.main_layout.layout().addLayout(self.header_layout)
        self.header_layout.addWidget(self.header_widget)

        # set char field
        self.char_field_layout = QtGui.QHBoxLayout()
        self.main_layout.layout().addLayout(self.char_field_layout)

        self.char_label = QtGui.QLabel('Char: ')
        self.char_text = QtGui.QLineEdit()
        self.char_text.setPlaceholderText('CharacterName')
        self.char_text.setStyleSheet('background-color:#2F2F2F;')

        self.char_field_layout.addWidget(self.char_label)
        self.char_field_layout.addWidget(self.char_text)

        # set side field
        self.side_field_layout = QtGui.QHBoxLayout()
        self.main_layout.layout().addLayout(self.side_field_layout)

        self.side_label = QtGui.QLabel('Side: ')
        self.side = QtGui.QComboBox()
        for side in autorig_settings.SIDES:
            if side != "c":
                self.side.addItem(side)
        self.side.setStyleSheet('background-color:#2F2F2F;')

        self.side_field_layout.addWidget(self.side_label)
        self.side_field_layout.addWidget(self.side)

        # set control color
        self.cc_color_field_layout = QtGui.QHBoxLayout()
        self.main_layout.layout().addLayout(self.cc_color_field_layout)

        self.cc_color_label = QtGui.QLabel('Character Control Color: ')
        self.cc_color_menu = QtGui.QComboBox()
        self.cc_color_menu.setStyleSheet('background-color: #2F2F2F;')
        self.cc_color_menu.addItem('blue')
        self.cc_color_menu.addItem('red')

        self.cc_color_field_layout.addWidget(self.cc_color_label)
        self.cc_color_field_layout.addWidget(self.cc_color_menu)

        # set cc_size field
        self.cc_size_field_layout = QtGui.QHBoxLayout()
        self.main_layout.layout().addLayout(self.cc_size_field_layout)

        self.cc_size_label = QtGui.QLabel('Character Control Size: ')
        self.cc_size = QtGui.QSpinBox()
        self.cc_size.setMinimum(1.0)
        self.cc_size.setMaximumWidth(60)
        self.cc_size.setStyleSheet('background-color:#2F2F2F;')

        self.cc_size_field_layout.addWidget(self.cc_size_label)
        self.cc_size_field_layout.addWidget(self.cc_size)

        # set solver menu
        self.solver_menu_layout = QtGui.QHBoxLayout()
        self.main_layout.layout().addLayout(self.solver_menu_layout)

        self.solver_menu_label = QtGui.QLabel('Solver Menu: ')
        self.solver_menu = QtGui.QComboBox()
        self.solver_menu.setStyleSheet('background-color: #2F2F2F;')
        self.solver_menu.addItem('ikRPsolver')
        self.solver_menu.addItem('ikSCsolver')

        self.solver_menu_layout.addWidget(self.solver_menu_label)
        self.solver_menu_layout.addWidget(self.solver_menu)

        # set in_hooks context menu
        self.hook_option_menu_layout = QtGui.QHBoxLayout()
        self.main_layout.layout().addLayout(self.hook_option_menu_layout)


        self.hook_context_label = QtGui.QLabel('In Hook: ')
        self.hook_context_label.setMaximumWidth(50)
        self.hook_context = QtGui.QComboBox()
        self.hook_context.setMaximumWidth(200)
        self.hook_context.setStyleSheet('background-color: #2F2F2F;')

        self.hook_option_menu_layout.addWidget(self.hook_context_label)
        self.hook_option_menu_layout.addWidget(self.hook_context)

        # set out_hooks context menu (pop up)
        self.out_hook_option_menu_layout = QtGui.QHBoxLayout()
        self.hook_button_layout = QtGui.QHBoxLayout()
        self.mir_module_layout = QtGui.QHBoxLayout()
        self.main_layout.layout().addLayout(self.out_hook_option_menu_layout)
        self.main_layout.layout().addLayout(self.mir_module_layout)
        self.main_layout.layout().addLayout(self.hook_button_layout)

        self.out_hook_context_label = QtGui.QLabel('Out Hook: ')
        self.out_hook_context_label.setMaximumWidth(50)
        self.out_hook_context = QtGui.QComboBox()
        self.out_hook_context.setMaximumWidth(200)
        self.out_hook_context.setStyleSheet('background-color: #2F2F2F;')
        self.mirror_module_checkbox = QtGui.QCheckBox('Mirror Module: ')
        self.mirror_module_checkbox.setChecked(1)
        self.add_hook_data_button = QtGui.QPushButton('Add Hook Data')
        self.add_hook_data_button.setMinimumHeight(30)
        self.mir_module_layout.addWidget(self.mirror_module_checkbox)
        self.hook_button_layout.addWidget(self.add_hook_data_button)
        self.add_hook_data_button.clicked.connect(self.__populate_hook_data)
        self.out_hook_option_menu_layout.addWidget(self.out_hook_context_label)
        self.out_hook_option_menu_layout.addWidget(self.out_hook_context)

        # remove module button
        self.remove_button_layout = QtGui.QHBoxLayout()
        self.main_layout.layout().addLayout(self.remove_button_layout)

        self.remove_button = QtGui.QPushButton('Remove')
        self.remove_button.setMinimumHeight(30)
        self.remove_button.clicked.connect(window.close)

        self.remove_button_layout.addWidget(self.remove_button)

        parent.addWidget(window)

        self.__pointer_class = None

    def get_module_instance(self):
        char = self.char_text.text()
        side = self.side.currentText()
        node_type = self.MODULE_TYPE
        cc_size = self.cc_size.value()
        solver = self.solver_menu.currentText()
        cc_color = self.cc_color_menu.currentText()
        self.mirror_module = self.mirror_module_checkbox.isChecked()

        self.__pointer_class = self.MODULE(char, side, node_type,
                                           cc_color=cc_color, cc_size=cc_size,
                                           solver=solver,
                                           mirror_module=self.mirror_module)
        return self.__pointer_class

    def __populate_hook_data(self, *args):
        # pop up item list
        self.__popup_items = []
        hooks = pm.ls("*hook")
        in_hooks = pm.ls("*In*_hook")
        for hook in hooks:
            try:
                hook.attr("hookType")

            except AttributeError:
                message = '%s does not have a hook type' % hook
                OpenMaya.MGlobal_displayInfo(message)

            else:
                if hook.attr("hookType").get():
                    hook = hook.split('|')
                    self.out_hook_context.addItem(str(hook[1]))

        for hook in in_hooks:
            if pm.nodeType(hook) == 'transform':
                hook = hook.split('|')
                self.hook_context.addItem(str(hook[1]))

    def set_hooks(self, *args):
        # grab selected hook from menu
        hook = self.hook_context.currentText()
        out_hook = self.out_hook_context.currentText()

        if not hook and not out_hook:
            message = "No hooks generated for this module."
            return OpenMaya.MGlobal_displayInfo(message)
        try:
            hook_menu_mir = pm.ls('*{0}In*_hookMirrored'.format(self.MODULE_TYPE))[0]
            out_hook_menu_mir = pm.ls('*{0}Out*_hookMirrored'.format(self.MODULE_TYPE))[0]

            hook = pm.ls(hook)[0]
            out_hook = pm.ls(out_hook)[0]

            pm.parentConstraint(out_hook, hook_menu_mir, mo=True)
            pm.parentConstraint(out_hook, hook, mo=True)
        except IndexError:
            hook = pm.ls(hook)[0]
            out_hook = pm.ls(out_hook)[0]
            pm.parentConstraint(out_hook, hook, mo=True)
