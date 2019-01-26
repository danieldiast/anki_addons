from anki.hooks import wrap
from aqt.editor import Editor, EditorWebView
from aqt.qt import *
from aqt.utils import shortcut, showInfo, showWarning, getBase, getFile, \
    openHelp, tooltip, downArrow
from BeautifulSoup import BeautifulSoup

# This is the favourites list - Add desired symbols' decimal values here
faves = [8592, 8593, 8594, 8595]

def onAddAnkiSymbol(self, entity_number):
    my_entity = "&#" + str(entity_number) + ";"
    #self.note.fields[self.currentField] += unicode(BeautifulSoup(my_entity))

    text = self.web.page().mainFrame().evaluateJavaScript("""
        function retTxt(){return currentField.innerText};
        retTxt();
        """)
    pos = len(text.replace("\n", "").split("|-|Symbol|-|")[0])
    pos += 1
    self.web.eval("""
            currentField.innerHTML = currentField.innerHTML.replace("|-|Symbol|-|", '"""+my_entity+"""')
            saveField("key");
            """)
    self.loadNote()
    self.web.setFocus()
    self.web.eval("focusField(%d);" % self.currentField)
    self.web.page().mainFrame().evaluateJavaScript(js_move_cursor % pos)

def onAddAnkiSymbol_factory(self, entity_number):
    return lambda s=self: onAddAnkiSymbol(self, entity_number)

def onAnkiSymbols(self):
    self.web.page().mainFrame().evaluateJavaScript("""
        // use placeholder to mark current cursor position
        document.execCommand("insertText", false, "|-|Symbol|-|");
        """)
    
    # self.web.eval("focusField(%d);" % self.currentField)

    # Creating menus
    main = QMenu(self.mw)

    favourites = QMenu("Favourites", self.mw)
    greek = QMenu("Greek letters", self.mw)
    arrows = QMenu("Arrows", self.mw)


    # Adding submenus to main menu
    main.addMenu(favourites)
    main.addMenu(greek)
    main.addMenu(arrows)

    # Adding symbols to sub menus
    # Greek Letters 913 - 974
    for greek_letter in range(913, 975):
        a = greek.addAction(unichr(greek_letter))
        a.connect(a, SIGNAL("triggered()"), onAddAnkiSymbol_factory(self, greek_letter))

    # Arrows 8592 - 8703
    for arrow in range(8592, 8704):
        a = arrows.addAction(unichr(arrow))
        #a.setShortcut(QKeySequence("Ctrl+A"))
        a.connect(a, SIGNAL("triggered()"), onAddAnkiSymbol_factory(self, arrow))

    # Add favourites to menu
    for f in faves:
        a = favourites.addAction(unichr(f))
        a.connect(a, SIGNAL("triggered()"), onAddAnkiSymbol_factory(self, f))
    main.exec_(QCursor.pos())

def mySetupButtons(self):
    but = self._addButton("symbolButton", lambda s=self: onAnkiSymbols(self),
                    text=unichr(945) + unichr(946) + unichr(947) + downArrow(), size=False)
    but.setShortcut(QKeySequence("Ctrl+S"))

Editor.setupButtons = wrap(Editor.setupButtons, mySetupButtons)

js_move_cursor = """
function findHiddenCharacters(node, beforeCaretIndex) {
    var hiddenCharacters = 0
    var lastCharWasWhiteSpace=true
    for(var n=0; n-hiddenCharacters<beforeCaretIndex &&n<node.length; n++) {
        if([' ','\\n','\\t','\\r'].indexOf(node.textContent[n]) !== -1) {
            if(lastCharWasWhiteSpace)
                hiddenCharacters++
            else
                lastCharWasWhiteSpace = true
        } else {
            lastCharWasWhiteSpace = false   
        }
    }

    return hiddenCharacters
}

var setSelectionByCharacterOffsets = null;

if (window.getSelection && document.createRange) {
    setSelectionByCharacterOffsets = function(containerEl, position) {
        var charIndex = 0, range = document.createRange();
        range.setStart(containerEl, 0);
        range.collapse(true);
        var nodeStack = [containerEl], node, foundStart = false, stop = false;

        while (!stop && (node = nodeStack.pop())) {
            if (node.nodeType == 3) {
                var hiddenCharacters = findHiddenCharacters(node, node.length)
                var nextCharIndex = charIndex + node.length - hiddenCharacters;

                if (position >= charIndex && position <= nextCharIndex) {
                    var nodeIndex = position - charIndex
                    var hiddenCharactersBeforeStart = findHiddenCharacters(node, nodeIndex)
                    range.setStart(node, nodeIndex + hiddenCharactersBeforeStart );
                    range.setEnd(node, nodeIndex + hiddenCharactersBeforeStart);
                    stop = true;
                }
                charIndex = nextCharIndex;
            } else {
                var i = node.childNodes.length;
                while (i--) {
                    nodeStack.push(node.childNodes[i]);
                }
            }
        }

        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
    }
} else if (document.selection) {
    setSelectionByCharacterOffsets = function(containerEl, start, end) {
        var textRange = document.body.createTextRange();
        textRange.moveToElementText(containerEl);
        textRange.collapse(true);
        textRange.moveEnd("character", end);
        textRange.moveStart("character", start);
        textRange.select();
    };
}
setSelectionByCharacterOffsets(currentField, %s)
"""