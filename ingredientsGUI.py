import sys
import collegecooking
from recipe import Recipe
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QApplication, QTextEdit, QGridLayout, QPushButton, QToolTip)

class Edit(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

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
        self.setWindowTitle("My Ingredients")

    def loadIngredients(self):
        ingredients = collegecooking.importIngredients("ingredients.txt")

        for i in ingredients:
            if (i != " ") and (i != "") and (i != None):
                self.ingredientEdit.append(i)

        self.ingredientEdit.repaint()

    def save(self):
        text = self.ingredientEdit.toPlainText()
        ingredients = text.split('\n')
        collegecooking.deleteIngredients("ingredients.txt")
        collegecooking.writeIngredients("ingredients.txt", ingredients)
        self.close()

    def cancel(self):
        self.close()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    edit = Edit()
    edit.show()
    sys.exit(app.exec_())
