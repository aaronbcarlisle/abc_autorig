#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    UI Widget for the main module
"""
#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

# third-party
from PySide import QtGui, QtCore

# external
from abc_autorig.modules.main_module import Main
from abc_autorig import autorig_settings

#------------------------------------------------------------------------------#
#----------------------------------------------------------------- FUNCTIONS --#

def get_ui(parent, ui):
    return MainModuleUI(parent, ui)

#------------------------------------------------------------------------------#
#------------------------------------------------------------------- CLASSES --#


class MainModuleUI(object):

    def __init__(self, parent, ui):

        # create window
        window = QtGui.QMainWindow()
        window.setStyleSheet('QMainWindow{border-color: #fff;}')
        window.setMaximumSize(265, 150)
        window.setMinimumSize(265, 150)

        # create base widget
        self.widget = QtGui.QWidget()
        window.setCentralWidget(self.widget)

        # create main layout
        self.main_layout =  QtGui.QVBoxLayout(self.widget)

        # set title text
        self.module_title = QtGui.QHBoxLayout()
        self.name = QtGui.QLabel('MAIN MODULE')
        self.main_layout.layout().addLayout(self.module_title)
        self.module_title.addWidget(self.name)

        # set char field
        self.char_field_layout = QtGui.QHBoxLayout()
        self.main_layout.layout().addLayout(self.char_field_layout)

        self.char_label = QtGui.QLabel('Char: ')
        self.char_text = QtGui.QLineEdit()
        self.char_text.setPlaceholderText('CharacterName')
        self.char_text.setStyleSheet('background-color:#2F2F2F;')

        self.char_field_layout.addWidget(self.char_label)
        self.char_field_layout.addWidget(self.char_text)

        # set cc_size field
        self.cc_size_field_layout = QtGui.QHBoxLayout()
        self.main_layout.layout().addLayout(self.cc_size_field_layout)

        self.cc_size_label = QtGui.QLabel('Character Main Control Size: ')
        self.cc_size = QtGui.QSpinBox()
        self.cc_size.setMinimum(1.0)
        self.cc_size.setMaximumWidth(60)
        self.cc_size.setStyleSheet('background-color:#2F2F2F;')

        self.cc_size_field_layout.addWidget(self.cc_size_label)
        self.cc_size_field_layout.addWidget(self.cc_size)

        # remove module button
        self.remove_button_layout = QtGui.QHBoxLayout()
        self.main_layout.layout().addLayout(self.remove_button_layout)

        self.remove_button = QtGui.QPushButton('Remove')
        self.remove_button.setMinimumHeight(30)
        self.remove_button.clicked.connect(window.close)

        self.remove_button_layout.addWidget(self.remove_button)

        # parent widget to scrollLayout
        parent.addWidget(window)

        self.__pointer_class = None

    def get_module_instance(self):

        char = self.char_text.text()

        side = "c"
        node_type = "main"
        cc_size = self.cc_size.value()

        self.__pointer_class = Main(char, side, node_type, cc_size=cc_size)
        return self.__pointer_class

    def set_hooks(self):
        pass
