import sys
import whatsfordinner
from recipe import Recipe
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QApplication, QTextEdit, QGridLayout, QPushButton)

#GUI for the user ingredients list, and the generated shopping list
#Depending on which file is used as an argument (ingredients.txt or shoppinglist.txt)

class Edit(QWidget):

    def __init__(self, filename):
        super().__init__()

        self.filename = filename

        #Save and Cancel buttons, placed at the bottom of the window
        saveButton = QPushButton("Save")
        cancelButton = QPushButton("Cancel")
        saveButton.clicked.connect(self.save)
        cancelButton.clicked.connect(self.cancel)

        #Text edit field above the buttons
        #Containing all ingredients in the file, to be edited/removed/added to by the user
        self.ingredientEdit = QTextEdit()
        self.loadIngredients()

        #Set grid layout
        grid = QGridLayout()
        grid.setSpacing(10)

        #Add buttons, text field
        grid.addWidget(self.ingredientEdit, 1, 0, 5, 2)
        grid.addWidget(saveButton, 6, 0)
        grid.addWidget(cancelButton, 6, 1)

        self.setLayout(grid)
        self.setGeometry(800, 600, 350, 300)
        if filename == "ingredients.txt":
            self.setWindowTitle("My Ingredients")
        elif filename == "shoppinglist.txt":
            self.setWindowTitle("Shopping List")
        else:
            self.setWindowTitle(filename)

    # import ingredients from whichever file and put them in the text field
    # So that they can be edited by the user
    def loadIngredients(self):
        ingredients = whatsfordinner.importIngredients(self.filename)

        for i in ingredients:
            if (i != " ") and (i != "") and (i != None):
                self.ingredientEdit.append(i)

        self.ingredientEdit.repaint()

    # write ingredients to file
    def save(self):
        text = self.ingredientEdit.toPlainText()
        ingredients = text.split('\n')
        whatsfordinner.deleteIngredients(self.filename)
        whatsfordinner.writeIngredients(self.filename, ingredients)
        self.close()

    # close without writing
    def cancel(self):
        self.close()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    edit = Edit()
    edit.show()
    sys.exit(app.exec_())
