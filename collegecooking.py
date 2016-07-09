from recipe import Recipe
from random import randint
import sys
import urllib2
import webbrowser

def generateURL(search_query, search_ingredients = [], *args):
    # basic search url
    url = "http://www.recipepuppy.com/api?"
    
    # add search ingredients
    if len(search_ingredients) > 0:
        url = url + "i="

        for x in range(0, len(search_ingredients)):
            url = url + search_ingredients[x]

            if x < len(search_ingredients) - 1:
                url = url + ","

    # add search query
    if search_query != None:
        url = url + "&q=" + search_query

    return url

search_ingredients = []
search_query = None
url = None

while True:
    print ""
    print "Welcome to the College Cookbook"
    print ""
    print "Press 1 to add specific ingredients"
    print "Press 2 to add a specific search term"
    print "Press 3 to grab a recipe"
    print "Press 4 to reset ingredients and search term"
    print "Press 5 to quit"

    user_choice = raw_input("> ")
    print ""

    # Add search ingredients
    if user_choice == "1":
        print "Enter ingredients you would like to use"
        print "To stop adding ingredients, leave the prompt empty and press ENTER"
        while True:
            ingr = raw_input("> ")
            if ingr == "":
                break;
            else:
                search_ingredients.append(ingr)

    # Add search query
    elif user_choice == "2":
        print "Enter a search query"
        query = raw_input("> ")
        search_query = query

    # Search for recipes
    elif user_choice == "3":
        url = generateURL(search_query, search_ingredients)
        response = urllib2.urlopen(url)
        html = response.read()
        recipes = []

        # get rid of API header
        raw_recipes = html.split("[")[1]
        raw_recipes = raw_recipes.translate(None, "]")

        # split into individual recipes
        success = False
        individuals = raw_recipes.split("},{")
        for recipe in individuals:
            recipe = recipe.translate(None, "{")
            recipe = recipe.translate(None, "}")

            # split recipe into segments (title, link, ingredients)
            recipe = recipe.split('","')
            try:
                title = recipe[0]
                link = recipe[1]
                ingredients = recipe[2]

                # split to remove extra characters, create recipe
                title = title.split('":"')
                link = link.split('":"')
                link[1] = link[1].translate(None, "\\")
                ingredients = ingredients.split('":"')

                recipe = Recipe(title[1], link[1], ingredients[1])
                recipes.append(recipe)
                success = True

            except IndexError:
                print ""
                print "Sorry, no results found."
                print "Try different ingredients, or a different search term"
                print "Resetting search"
                Recipe.recipeCount = 0
                search_ingredients = []
                search_query = None

        if success == True:

            number = randint(0, Recipe.recipeCount - 1)
            print""
            recipes[number].display()
            print ""
            print "Look interesting? Press ENTER to open the recipe, press anything else to keep moving"
            response = raw_input("> ")
            if not response: #input was an ENTER
                print "Opening recipe in browser"
                webbrowser.open_new_tab(recipes[number].link)

            # Reset the recipe counter
            Recipe.recipeCount = 0

    elif user_choice == "4":
        # Reset search terms and recipe counter
        search_ingredients = []
        search_query = None
        Recipe.recipeCount = 0

    elif user_choice == "5":
        sys.exit()
