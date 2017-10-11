#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    Build a usable UI for the abc_autorig tool.
"""
#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

# built-in
import imp
import shiboken
import os
import pymel.core as pm
from maya import OpenMayaUI

# third-party
from PySide import QtGui, QtCore
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

# external
from abc_autorig.modules import sub_modules
from abc_autorig.core import build
from abc_autorig.utils import json_utils
from abc_autorig import autorig_settings

#------------------------------------------------------------------------------#
#----------------------------------------------------------------- FUNCTIONS --#

def get_maya_window():
    pointer = OpenMayaUI.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(pointer), QtGui.QWidget)

#------------------------------------------------------------------------------#
#------------------------------------------------------------------- CLASSES --#


class AutorigUI(object):

    MODULES = list()

    def __init__(self):

        self.image_path = autorig_settings.IMAGES_PATH

        self.ui_modules = list()
        self.build_session = build.Build()

    def ui(self):

        self.window_name = 'ABC_Autorig'

        # check if window exists
        if pm.window('ABC_Autorig', exists = True):
            pm.deleteUI('ABC_Autorig', wnd = True)

        # create the window
        self.parent = get_maya_window()
        self.window = type('ABC_Autorig', (MayaQWidgetDockableMixin,
                            QtGui.QMainWindow),  {})(self.parent)
        self.window.setStyleSheet('background-color: #1b1b1b;')
        self.window.setObjectName(self.window_name)
        self.window.setWindowTitle('ABC Autorig V1')
        self.window.setMinimumSize(320, 700)
        self.window.setMaximumWidth(320)

        # set font
        self.font = QtGui.QFont()
        self.font.setPointSize(12)

        # create main widget
        self.main_widget = QtGui.QWidget()
        self.window.setCentralWidget(self.main_widget)

        # create our main vertical layout
        self.main_layout = QtGui.QVBoxLayout(self.main_widget)

        # create modules layout
        self.modules_layout = QtGui.QVBoxLayout()
        self.modules_layout.layout().setAlignment(QtCore.Qt.AlignTop)
        self.main_layout.layout().addLayout(self.modules_layout)

        self.menu_layout = QtGui.QHBoxLayout()
        self.modules_layout.layout().addLayout(self.menu_layout)

        self.menu_name = QtGui.QLabel('MODULES: ')
        self.modules_menu = QtGui.QComboBox()
        for module in self.build_session.available_modules:
            self.modules_menu.addItem(module)
        self.modules_menu.setFixedWidth(200)
        self.modules_menu.setStyleSheet('background-color: #2F2F2F;')

        self.menu_layout.addWidget(self.menu_name)
        self.menu_layout.addWidget(self.modules_menu)

        # create add button
        self.add_button = QtGui.QPushButton('Add Module')
        self.add_button.setStyleSheet('QPushButton{background-color: #2F2F2F;'\
                        'border-radius: 2px; height: 30px; font-size: 16px;}'\
                        'QPushButton:pressed{background-color: #6f6f6f;'\
                        'border-radius: 2px; height: 30px; font-size: 16px;}')

        # connect button
        self.add_button.clicked.connect(self.add_module)
        self.modules_layout.addWidget(self.add_button)

        # create modules scroll layout
        self.scroll_layout = QtGui.QVBoxLayout()
        self.main_layout.layout().addLayout(self.scroll_layout)

        self.scroll_widget = QtGui.QWidget()
        self.scroll_area = QtGui.QScrollArea()
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.inside_layout = QtGui.QVBoxLayout(self.scroll_widget)
        self.inside_layout.setAlignment(QtCore.Qt.AlignTop)

        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_layout.addWidget(self.scroll_area)

        self.bg_image = self.image_path + 'scrollAreaBackground.png'
        image = "QScrollArea{background-image: url(" + self.bg_image + ");}"
        self.scroll_area.setStyleSheet(image)

        # add build guides and build rig buttons
        self.build_button_layout = QtGui.QVBoxLayout()
        self.main_layout.layout().addLayout(self.build_button_layout)

        self.build_guides_button = QtGui.QPushButton('BUILD GUIDES')
        self.build_rig_button = QtGui.QPushButton('BUILD RIG')

        self.build_guides_button.setStyleSheet('QPushButton{background-color:'\
                '#2F2F2F; border-radius: 2px; height: 30px; font-size: 16px;}'\
                'QPushButton:pressed{background-color: '\
                '#6f6f6f; border-radius: 2px; height: 30px; font-size: 16px;}')

        self.build_rig_button.setStyleSheet('QPushButton{background-color: '\
                '#2F2F2F; border-radius: 2px; height: 30px; font-size: 16px;}'
                'QPushButton:pressed{background-color: '\
                '#6f6f6f; border-radius: 2px; height: 30px; font-size: 16px;}')

        # connect the buttons
        self.build_guides_button.clicked.connect(self.build_guides)
        self.build_rig_button.clicked.connect(self.build_rig)

        self.main_layout.addWidget(self.build_guides_button)
        self.main_layout.addWidget(self.build_rig_button)

        self.window.show(dockable=True, floating=False, area='left')

    def add_module(self):

        self.module = self.modules_menu.currentText()
        self.module = self.build_session.modules[self.module]

        # find ui module
        module_name = os.path.basename(self.module).split(".py")[0]
        module_ui_path = autorig_settings.UI_PATH + module_name + "_ui.py"

        # load module
        self.module = imp.load_source('module.name', module_ui_path)
        self.module_ui = self.module.get_ui(self.inside_layout, self)
        self.MODULES.append(self.module_ui)
        self.ui_modules.append(self.module_ui)

    def build_guides(self):

        self.temp_objects = list()
        for ui_module in self.ui_modules:
            self.temp_objects.append(ui_module.get_module_instance())
            self.MODULES.append(ui_module.get_module_instance())

        self.build_session.modules = self.temp_objects
        self.build_session.build_guides()


    def build_rig(self):

        self.build_session.build()

        for ui_module in self.ui_modules:
            ui_module.set_hooks()
        self.build_session.build_connections()

    def get_hook_data(self):

        path = autorig_settings.MODULES_PATH + 'hook_data.json'
        for ui_module in self.ui_modules:
            json_utils.save(ui_module.set_hooks(), path)
