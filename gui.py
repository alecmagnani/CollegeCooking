import sys
import whatsfordinner
import editGUI
from recipe import Recipe
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QGridLayout, QApplication,
    QPushButton, QToolTip, QStyleFactory)

# Main program GUI
class Home(QWidget):

    def __init__(self):
        super().__init__()

        self.currentRecipe = None
        self.initUI()

    def initUI(self):

        #Create edit, 2 search, and exit buttons for the left hand side
        editButton = QPushButton("Edit My Ingredients")
        ingrSearchButton = QPushButton("Search With Ingredients")
        randSearchButton = QPushButton("Search All Recipes")
        exitButton = QPushButton("Exit")
        #Create the select button, for the bottom right corner
        selectButton = QPushButton("Select")

        #Create tooltips for mouse hover over buttons
        ingrSearchButton.setToolTip("Get a random recipe that contains ingredients from your ingredient list")
        randSearchButton.setToolTip("Get a completely random recipe")
        selectButton.setToolTip("Select and generate a shopping list")

        #Attach methods to buttons
        editButton.clicked.connect(self.edit)
        ingrSearchButton.clicked.connect(self.ingrSearch)
        randSearchButton.clicked.connect(self.randSearch)
        exitButton.clicked.connect(self.exit)
        selectButton.clicked.connect(self.select)

        #Title and Ingredients labels
        titleLabel = QLabel("Title: ")
        ingredientsLabel = QLabel("Ingredients: ")
        titleLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        ingredientsLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        #Title and Ingredients fields created, to be filled with the recipe title and ingredients
        self.title = QLabel(self)
        self.ingredients = QLabel(self)
        self.title.setOpenExternalLinks(True) #The title will be a hyperlink so that the recipe can be opened in browser
        self.title.setText("Click a search button to get started!")
        self.title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.ingredients.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        #Create grid, add widgets
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
        self.setWindowTitle("What's For Dinner?")
        self.show()

    #Open editGUI for user ingredients
    def edit(self):
        self.ingredientsUI = editGUI.Edit("ingredients.txt")
        self.ingredientsUI.show()

    #Grab a random recipe with user ingredients
    def ingrSearch(self):

        ingredients = whatsfordinner.importIngredients("ingredients.txt")
        url = whatsfordinner.getIngredientSearchURL(None, ingredients)
        ingredient_recipes = whatsfordinner.ingredientSearch(url)
        whatsfordinner.scoreRecipes(ingredient_recipes, ingredients)
        recipe = whatsfordinner.findBest(ingredient_recipes)
        
        home.currentRecipe = recipe
        home.title.setText('''<a href='''+recipe.link+'''>'''+ recipe.title +'''</a>''')
        home.ingredients.setText(recipe.ingredients)
        home.title.repaint()
        home.ingredients.repaint()

    #Grab a completely random recipe
    def randSearch(self):

        url = whatsfordinner.getRandomSearchURL(None)
        all_recipes = whatsfordinner.randomSearch(url)
        recipe = whatsfordinner.getRandomRecipe(all_recipes)

        home.currentRecipe = recipe
        home.title.setText('''<a href='''+recipe.link+'''>'''+recipe.title +'''</a>''')
        home.ingredients.setText(recipe.ingredients)
        home.title.repaint()
        home.ingredients.repaint()

    #Select the recipe that is currently displayed
    #Generate the shopping list, open editGUI with the shopping list
    def select(self):
        if home.currentRecipe == None:
            print("No recipe selected")
        else:
            home.currentRecipe.display()
            print("")
            whatsfordinner.select(home.currentRecipe)
            self.shoppinglistUI = editGUI.Edit("shoppinglist.txt")
            self.shoppinglistUI.show()

    #Close the GUI
    def exit(self):
        self.close()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("cleanlooks"))
    home = Home()
    sys.exit(app.exec_())
