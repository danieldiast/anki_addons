# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *


from anki.hooks import wrap
from aqt.editor import Editor
from aqt.utils import showInfo

def buttonPressed(self):
    showInfo("pressed " + 'teste')

def mySetupButtons(self):
    # - size=False tells Anki not to use a small button
    # - the lambda is necessary to pass the editor instance to the
    #   callback, as we're passing in a function rather than a bound
    #   method
    self._addButton("mybutton", lambda s=self: buttonPressed(self),
                    text="PressMe", size=False)

Editor.setupButtons = wrap(Editor.setupButtons, mySetupButtons)



# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def testFunction():
    # get the number of cards in the current collection, which is stored in
    # the main window
    cardCount = mw.col.cardCount()
    # show a message box
    showInfo("Card count: %d" % cardCount)

# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)