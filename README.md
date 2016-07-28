# What's For Dinner?
A basic recipe program utilizing the Recipe Puppy API (http://www.recipepuppy.com/about/api/) and urllib for Python 3

A GUI can be launched with "python3 gui.py", or as a command line tool with "python3 whatsfordinner.py

This program seeks to help the indecisive chef by taking the decision making out of answering the question "What's for Dinner?". It uses the RecipePuppy API to generate recipes either at random, or based on a list of ingredients specified by the user. The user can open the recipe in their browser, and also select the recipe, which generates a shopping list of ingredients not found in their ingredients list.

![Main Screen](/screenshots/main.png?raw=true "This is the screen upon opening the program")

The program consists of the following files:

    whatsfordinner.py - the main program file containing functions, API access, etc.
    recipe.py - recipe class used to store and display information for each recipe
    gui.py - the main window for the program user interface
    editGUI.py - secondary window for displaying/editing user ingredients as well as the shopping list
    ingredients.txt - list of ingredients that the user has available
    shoppinglist.txt - list of ingredients generated after the user selects a recipe. Contains ingredients required for the recipe that are not found in the user's ingredients list

To do:

    Improve GUI functionality/usability
