#-*- coding: utf-8 -*-

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

        shortcut = QtGui.QKeySequence(u"ctrl+F7")
        tooltip = u"Set secondary color ({})".format(shortcut.toString(QtGui.QKeySequence.NativeText))
        buttonSecondColor = Button("button_second_color", shortcut, tooltip,lambda: editor._wrapWithColour(editor.mw.pm.profile.get("lastSecondColour", "#0f0")), text=" ")
        setup_background_button(editor, buttonSecondColor)
        place_button(editor, buttonSecondColor)

        shortcut = QtGui.QKeySequence(u"ctrl+F8")
        tooltip = u"Change secondary color ({})".format(shortcut.toString(QtGui.QKeySequence.NativeText))
        buttonSecondColorDown = Button("button_second_color_choose",
                         shortcut,
                         tooltip,
                         lambda: change_color(editor),
                         # space is needed to center the arrow
                         text=downArrow())
        buttonSecondColorDown.setFixedWidth(16)
        place_button(editor, buttonSecondColorDown)



def change_color(self):
        """
        Choose new color.
        """
        new = QtGui.QColorDialog.getColor(QtGui.QColor(self.mw.pm.profile.get("lastSecondColour", "#0f0")), None)
        # native dialog doesn't refocus us for some reason
        self.parentWindow.activateWindow()
        if new.isValid():
            self.fSecondcolour = new.name()
            self._wrapWithColour(self.fSecondcolour)
            self.mw.pm.profile['lastSecondColour'] = self.fSecondcolour
            self.background_frame.setPalette(QtGui.QPalette(QtGui.QColor(self.fSecondcolour)))
            # setup_background_button(self, button);



def setup_background_button(self, button):
        """
        Create the actual button that the user can click on.
        """
        self.background_frame = QtGui.QFrame()
        self.background_frame.setAutoFillBackground(True)
        self.background_frame.setFocusPolicy(QtCore.Qt.NoFocus)
        #self._on_bg_color_changed()

        self.background_frame.setPalette(QtGui.QPalette(QtGui.QColor(self.mw.pm.profile.get("lastSecondColour", "#0f0"))))

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.background_frame)
        hbox.setMargin(5)
        button.setLayout(hbox)


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
        """
        Set icon by `name`.
        """
        # c = PrefHelper.get_config()
        # icon_path = os.path.join(PrefHelper.get_addons_folder(),
        #                          c.get(const.CONFIG_DEFAULT, "FOLDER_NAME"),
        #                          "icons",
        #                          "{}.png".format(name))
        super(Button, self)#.setIcon(QtGui.QIcon(icon_path))




# but = self._addButton("symbolButton", lambda s=self: onAnkiSymbols(self),
#                 text=unichr(945) + unichr(946) + unichr(947) + downArrow(), size=False)
# but.setShortcut(QKeySequence("Ctrl+S")) 
