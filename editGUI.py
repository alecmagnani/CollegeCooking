import sys
import collegecooking
from recipe import Recipe
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QApplication, QTextEdit, QGridLayout, QPushButton)

class Edit(QWidget):

    def __init__(self, filename):
        super().__init__()

        self.filename = filename

        saveButton = QPushButton("Save")
        cancelButton = QPushButton("Cancel")
        saveButton.clicked.connect(self.save)
        cancelButton.clicked.connect(self.cancel)

        self.ingredientEdit = QTextEdit()
        self.loadIngredients()

        grid = QGridLayout()
        grid.setSpacing(10)

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

    def loadIngredients(self):
        ingredients = collegecooking.importIngredients(self.filename)

        for i in ingredients:
            if (i != " ") and (i != "") and (i != None):
                self.ingredientEdit.append(i)

        self.ingredientEdit.repaint()

    def save(self):
        text = self.ingredientEdit.toPlainText()
        ingredients = text.split('\n')
        collegecooking.deleteIngredients(self.filename)
        collegecooking.writeIngredients(self.filename, ingredients)
        self.close()

    def cancel(self):
        self.close()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    edit = Edit()
    edit.show()
    sys.exit(app.exec_())
