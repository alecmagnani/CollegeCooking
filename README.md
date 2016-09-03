# What's For Dinner?
A basic recipe program utilizing the Recipe Puppy API (http://www.recipepuppy.com/about/api/)

Written in Python 3, Requires urllib and PyQt5

A GUI can be launched with "python gui.py", or a command line tool with "python whatsfordinner.py"

A work-in-progress web page written using Flask can be launched using "python web.py"

This program seeks to help the indecisive chef by taking the decision making out of answering the question "What's for Dinner?". It uses the RecipePuppy API to generate recipes either at random, or based on a list of ingredients specified by the user. The user can open the recipe in their browser, and also select the recipe, which generates a shopping list of ingredients not found in their ingredients list.

![Web App](/screenshots/webapp.png?raw=true "Web app displaying a random recipe")

![Main Screen](/screenshots/recipe.png?raw=true "Screen after the program has generated a recipe")

![Ingredients](/screenshots/ingredients.png?raw=true "Add, edit, or remove ingredients from your list")

![Shopping List](/screenshots/shoppinglist.png?raw=true "Automatically generates a shopping list once a recipe is selected")

The program consists of the following files:

    whatsfordinner.py - the main program file containing functions, API access, etc.
    recipe.py - recipe class used to store and display information for each recipe
    gui.py - the main window for the program user interface
    editGUI.py - secondary window for displaying/editing user ingredients as well as the shopping list
    ingredients.txt - list of ingredients that the user has available
    shoppinglist.txt - list of ingredients generated after the user selects a recipe. Contains ingredients required for the recipe that are not found in the user's ingredients list
    ___________In progress_____________________________
    web.py - working on creating a webapp version using Flask
    templates (Flask folder)
    static (Flask folder)
