import sys
import collegecooking
import ingredientsGUI
from recipe import Recipe
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QGridLayout, QApplication, QPushButton, QToolTip)

class Home(QWidget):

    def __init__(self):
        super().__init__()

        self.currentRecipe = None
        self.initUI()

    def initUI(self):

        editButton = QPushButton("Edit My Ingredients")
        ingrSearchButton = QPushButton("Search With Ingredients")
        randSearchButton = QPushButton("Search All Recipes")
        exitButton = QPushButton("Exit")
        selectButton = QPushButton("Select")

        ingrSearchButton.setToolTip("Get a random recipe that contains ingredients from your ingredient list")
        randSearchButton.setToolTip("Get a completely random recipe")
        selectButton.setToolTip("Select and generate a shopping list")

        editButton.clicked.connect(self.edit)
        ingrSearchButton.clicked.connect(self.ingrSearch)
        randSearchButton.clicked.connect(self.randSearch)
        exitButton.clicked.connect(self.exit)
        selectButton.clicked.connect(self.select)

        titleLabel = QLabel("Title: ")
        ingredientsLabel = QLabel("Ingredients: ")
        titleLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        ingredientsLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.title = QLabel(self)
        self.ingredients = QLabel(self)
        self.title.setOpenExternalLinks(True)
        self.title.setText("Click a search button to get started!")
        self.title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.ingredients.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        grid = QGridLayout()
        grid.addWidget(editButton, 1, 0)
        grid.addWidget(ingrSearchButton, 2, 0)
        grid.addWidget(randSearchButton, 3, 0)
        grid.addWidget(exitButton, 4, 0)

        grid.addWidget(titleLabel, 1, 1, 1, 1)
        grid.addWidget(ingredientsLabel, 2, 1, 2, 1)

        grid.addWidget(self.title, 1, 2, 1, 2)
        grid.addWidget(self.ingredients, 2, 2, 2, 2)

        grid.addWidget(selectButton, 4, 3, 1, 2)

        self.setLayout(grid)
        self.setGeometry(800, 600, 700, 175)
        self.setWindowTitle("College Cooking")
        self.show()

    def edit(self):
        self.editUI = ingredientsGUI.Edit("ingredients.txt")
        self.editUI.show()

    def ingrSearch(self):

        ingredients = collegecooking.importIngredients("ingredients.txt")
        url = collegecooking.getIngredientSearchURL(None, ingredients)
        ingredient_recipes = collegecooking.ingredientSearch(url)
        recipe = collegecooking.getRandomRecipe(ingredient_recipes)
        
        home.currentRecipe = recipe
        home.title.setText('''<a href='''+recipe.link+'''>'''+recipe.title +'''</a>''')
        home.ingredients.setText(recipe.ingredients)
        home.title.repaint()
        home.ingredients.repaint()

    def randSearch(self):

        url = collegecooking.getRandomSearchURL(None)
        all_recipes = collegecooking.randomSearch(url)
        recipe = collegecooking.getRandomRecipe(all_recipes)

        home.currentRecipe = recipe
        home.title.setText('''<a href='''+recipe.link+'''>'''+recipe.title +'''</a>''')
        home.ingredients.setText(recipe.ingredients)
        home.title.repaint()
        home.ingredients.repaint()

    def select(self):
        if home.currentRecipe == None:
            print("No recipe selected")
        else:
            home.currentRecipe.display()
            print("")
            collegecooking.select(home.currentRecipe)

    def exit(self):
        self.close()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    home = Home()
    sys.exit(app.exec_())
