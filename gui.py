import sys
import collegecooking
from recipe import Recipe
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QGridLayout, QApplication, QPushButton, QToolTip)

class Home(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        grid = QGridLayout()

        editButton = QPushButton("Edit My Ingredients")
        ingrSearchButton = QPushButton("Search With Ingredients")
        randSearchButton = QPushButton("Search All Recipes")
        selectButton = QPushButton("Select")
        # nextButton = QPushButton("Next")

        ingrSearchButton.setToolTip("Get a random recipe that contains ingredients from your ingredient list")
        randSearchButton.setToolTip("Get a completely random recipe")
        selectButton.setToolTip("Select and generate a shopping list")

        editButton.clicked.connect(edit)
        ingrSearchButton.clicked.connect(ingrSearch)
        randSearchButton.clicked.connect(randSearch)
        selectButton.clicked.connect(select)
        # nextButton.clicked.connect(nextRecipe)

        titleLabel = QLabel("Title: ")
        ingredientsLabel = QLabel("Ingredients: ")
        titleLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        ingredientsLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Sample info
        self.title = QLabel(self)
        self.ingredients = QLabel(self)
        self.title.setOpenExternalLinks(True)

        self.title.setText("Find a recipe!")

        grid.addWidget(editButton, 1, 0)
        grid.addWidget(ingrSearchButton, 2, 0)
        grid.addWidget(randSearchButton, 3, 0)

        grid.addWidget(titleLabel, 1, 1)
        grid.addWidget(ingredientsLabel, 2, 1)

        grid.addWidget(self.title, 1, 2, 5, 1)
        grid.addWidget(self.ingredients, 2, 2, 5, 1)

        grid.addWidget(selectButton, 3, 2)
        # grid.addWidget(nextButton, 3, 3)

        self.setLayout(grid)

        self.setGeometry(800, 600, 700, 175)
        self.setWindowTitle("College Cooking")
        self.show()

def edit():
    print("edit")

def ingrSearch():

    ingredients = collegecooking.importIngredients("ingredients.txt")
    url = collegecooking.getIngredientSearchURL(None, ingredients)
    ingredient_recipes = collegecooking.ingredientSearch(url)
    recipe = collegecooking.getRandomRecipe(ingredient_recipes)
    recipe.display()
    
    home.title.setText('''<a href='''+recipe.link+'''>'''+recipe.title +'''</a>''')
    home.ingredients.setText(recipe.ingredients)
    home.title.repaint()
    home.ingredients.repaint()

def randSearch():

    url = collegecooking.getRandomSearchURL(None)
    all_recipes = collegecooking.randomSearch(url)
    recipe = collegecooking.getRandomRecipe(all_recipes)
    recipe.display()

    home.title.setText('''<a href='''+recipe.link+'''>'''+recipe.title +'''</a>''')
    home.ingredients.setText(recipe.ingredients)
    home.title.repaint()
    home.ingredients.repaint()

def select():
    print("select")

# def nextRecipe():
    # print("nextRecipe")

if __name__ == '__main__':

    app = QApplication(sys.argv)
    home = Home()
    sys.exit(app.exec_())
