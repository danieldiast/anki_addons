#-*- coding: utf-8 -*-
"""
Anki Add-on: Javascript Button

Author: Daniel Dias Teixeira

v0.1.0
"""


# import the main window object (mw) from aqt
from aqt import editor, mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *

from anki.hooks import wrap


from PyQt4 import QtGui, QtCore

#from power_format_pack.prefhelper import PrefHelper
# import os
# import const



def place_button(editor, button):
    editor.iconsBox.addWidget(button)   

def downArrow():
    if isWin:
        return u"▼"
    # windows 10 is lacking the smaller arrow on English installs
    return u"▾"



def setup_buttons(editor):
        shortcut = QtGui.QKeySequence(u"ctrl+q")
        tooltip = u"Run javascript ({})".format(shortcut.toString(QtGui.QKeySequence.NativeText))
        buttonJS  = Button("button_second_color", shortcut, tooltip,lambda s=editor: open_js_runner(editor), text="JS")
        place_button(editor, buttonJS)
        # editor._addButton("buttonJS", lambda s=editor: open_js_runner(s), text="JS", size=False)



def open_js_runner(self):
    dialog = QtGui.QDialog(self.parentWindow)
    dialog.setWindowTitle("JS comand") 

    form = QtGui.QFormLayout()
    form.addRow(QtGui.QLabel("Javascript:"))
    userText = QtGui.QTextEdit(self.widget)
    form.addRow(userText)
    buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
                                           QtGui.QDialogButtonBox.Cancel,
                                           QtCore.Qt.Horizontal,
                                           dialog)
    # butOk =  buttonBox.standardButton(QDialogButtonBox.OK)    

    shortcut = QtGui.QKeySequence(u"ctrl+enter")    
    # buttonBox.accepted.
    buttonBox.accepted.connect(dialog.accept)
    # buttonBox.accepted.setShortcut(shortcut)
    buttonBox.rejected.connect(dialog.reject)
    form.addRow(buttonBox)
    dialog.setLayout(form)

    if dialog.exec_() == QtGui.QDialog.Accepted:
        resp = self.web.eval(userText.toPlainText())
        # showInfo(resp)
        


editor.Editor.setupButtons = wrap(editor.Editor.setupButtons, setup_buttons)



class Button(QtGui.QPushButton):
    """
    Represents a clickable button.
    """
    def __init__(self, name, shortcut, tooltip, callback, text=""):
        super(Button, self).__init__(text)
        self.name = name
        self.setShortcut(shortcut)
        self.setToolTip(tooltip)
        self.clicked.connect(callback)
        self.setFixedHeight(20)
        self.setFixedWidth(20)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setIcon(self.name)


    def setIcon(self, name):
        super(Button, self)




# but = self._addButton("symbolButton", lambda s=self: onAnkiSymbols(self),
#                 text=unichr(945) + unichr(946) + unichr(947) + downArrow(), size=False)
# but.setShortcut(QKeySequence("Ctrl+S")) 
