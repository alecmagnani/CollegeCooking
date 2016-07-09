from recipe import Recipe
from random import randint
import sys
import urllib2
import webbrowser

def generateURL(page, search_query, search_ingredients = [], *args):
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

    if page != 0:
        url = url + "&p=" + str(page)
    return url

def getRecipes(page, search_query, search_ingredients = [], recipes = [], *args):
        url = generateURL(page, search_query, search_ingredients)

        response = urllib2.urlopen(url)
        json = response.read()

        # get rid of API header
        raw_recipes = json.split("[")[1]
        raw_recipes = raw_recipes.translate(None, "]")

        # split into individual recipes
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
            except:
                return recipes

        getRecipes(page + 1, search_query, search_ingredients, recipes) 
        return recipes

def getRandom(recipes):
    num = randint(0, len(recipes) - 1)
    return recipes[num]

if __name__ == "__main__":

    allRecipes = []
    recipes = []
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
            if len(allRecipes) == 0:
                print("Loading recipes...")
                allRecipes = getRecipes(0, search_query, search_ingredients, recipes)
                recipe = getRandom(allRecipes)
            else:
                recipe = getRandom(allRecipes)

            print ""
            print "Picked from " + str(Recipe.recipeCount) + " recipes:"
            recipe.display()
            while True:
                print ""
                print "Does this look interesting?"
                print "Press 1 to open"
                print "Press 2 to grab a new recipe"
                print "Press any other key to go to the menu"
                print ""
                choice = raw_input("> ")
                if choice == "1":
                    webbrowser.open_new_tab(recipe.link)
                    break
                elif choice == "2":
                    recipe = getRandom(allRecipes)
                    recipe.display()
                else:
                    break

        elif user_choice == "4":
            allRecipes = []
            recipes = []
            search_ingredients = []
            search_query = None
            Recipe.recipeCount = 0

        elif user_choice == "5":
            sys.exit()
