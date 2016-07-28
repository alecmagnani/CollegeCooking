# What's For Dinner?
A basic recipe program utilizing the Recipe Puppy API (http://www.recipepuppy.com/about/api/) and urllib for Python 3

The program keeps track of what ingredients are available, and can search for recipes that include those ingredients, do a random search, or search with a keyword. The program then collects hundreds of recipes and selects one at random. The user can select it, at which point the program opens the recipe in the browser and simultaneously produces a "shopping list" of missing ingredients, or the user can pass on that recipe and view a different one. 

The program consists of the following files:

    whatsfordinner.py - the main program file containing functions, API access, etc.
    recipe.py - recipe class used to store and display information for each recipe
    gui.py - the main window for the program user interface
    editGUI.py - secondary window for displaying/editing user ingredients as well as the shopping list
    ingredients.txt - list of ingredients that the user has available
    shoppinglist.txt - list of ingredients generated after the user selects a recipe. Contains ingredients required for the recipe that are not found in the user's ingredients list

To do:

    Improve GUI functionality/usability
