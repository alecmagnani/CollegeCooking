import sys
import xml.etree.ElementTree as ET
import urllib.request
import webbrowser
from random import randint
from recipe import Recipe

# Main loop for command line version of program
def main(query, ingredients = [], recipes = [], allRecipes = [], ingrRecipes = [], *args):
    query = query
    ingredients = ingredients
    recipes = recipes

    print("")
    print("1. add ingredients to search with")
    print("2. add search term")
    print("3. search with current ingredients")
    print("4. search all recipes")
    print("5. reset search term and ingredients")
    print("6. exit")

    usr = input("> ")
    print("")

    if usr == "1":
        ingrRecipes = []
        displayIngredients("ingredients.txt")
        ingredients = getIngredients()
        writeIngredients("ingredients.txt", ingredients)
        main(query, ingredients, recipes, allRecipes, ingrRecipes)

    elif usr == "2":
        query = getQuery()
        main(query, ingredients, recipes, allRecipes, ingrRecipes)

    elif usr == "3":
        if len(ingrRecipes) == 0:
            ingredients = importIngredients("ingredients.txt")
            url = getIngredientSearchURL(query, ingredients)
            ingrRecipes = ingredientSearch(url)
            scoreRecipes(ingrRecipes, ingredients)

        while True:
            recipe = findBest(ingrRecipes)
            recipe.display()
            choice = prompt(recipe)

            if choice == "1":
                select(recipe)
                break
            elif choice == "2":
                pass    
            else:
                main(query, ingredients, recipes, allRecipes, ingrRecipes)

    elif usr == "4":
        if len(allRecipes) == 0:
            url = getRandomSearchURL(query)
            allRecipes = randomSearch(url)
        
        while True:
            recipe = getRandomRecipe(allRecipes)
            recipe.display()
            choice = prompt(recipe)
            
            if choice == "1":
                select(recipe)
                break
            elif choice == "2":
                pass
            else:
                main(query, ingredients, recipes, allRecipes, ingrRecipes)
        
    elif usr == "5":
        reset()
        main(query, ingredients, recipes, allRecipes, ingrRecipes)

    elif usr == "6":
        sys.exit()

    else:
        main(query, ingredients, recipes, allRecipes, ingrRecipes)

# The API returns one page of 10 recipes at a time in JSON
# This method separates the page of text into individual recipes
# A recipe consists of a title, a link, and a list of ingredients (see recipe.py for Recipe class)
def jsonparse(json):
    split = json.decode('utf8').split("[")
    raw_recipes = split[1]
    raw_recipes = raw_recipes.strip("]")

    individuals = raw_recipes.split("},{")
    for recipe in individuals:
        recipe = recipe.strip("{")
        recipe = recipe.strip("}")
        recipe = recipe.split( '","' )
        
        title = recipe[0]
        link = recipe[1]
        ingredients = recipe[2]

        title = title.split('":"')
        link = link.split('":"')
        ingredients = ingredients.split('":"')
        link[1] = link[1].replace("\\", "")

        recipe = Recipe(title[1], link[1], ingredients[1])
        recipes.append(recipe)

    return recipes

# generates a url containing the search query (if applicable) and all user ingredients from 'ingredients.txt'
def getIngredientSearchURL(query, ingredients = [], *args):
    url = "http://recipepuppy.com/api?"
    if ingredients == None:
        return url
    if len(ingredients) > 0:
        url = url + "i="
        for x in range(0, len(ingredients)):
            url = url + ingredients[x].strip()
            if x < (len(ingredients) - 1):
                url = url + ","
    if (query != None) and (query != "") and (query != " "):
        url = url + "&q=" + query

    print("Searching: " + url)
    print("")
    return url

# generates a url containing the search query (if applicable) and no ingredients
def getRandomSearchURL(query):
    url = "http://recipepuppy.com/api?"
    if (query != None) and (query != "") and (query != " "):
        url = url + "&q" + query
    print("Searching: " + url)
    print("")
    return url

# picks a random selection of 5 pages out of 100+ (~50 recipes)
# and returns a list of those recipes
def ingredientSearch(url):
    ingredient_recipes = []
    pageMin = randint(1, 15)
    pageMax = pageMin + 5
    for x in range(pageMin, pageMax):
        # the try/except handles the blank pages that sometimes occur
        try:
            url = url + "&p=" + str(x)
            request = urllib.request.Request(url)
            result = urllib.request.urlopen(request)
            json = result.read()
            recipes = jsonparse(json)
            for recipe in recipes:
                ingredient_recipes.append(recipe)
        except:
            pass

    print("Searching pages " + str(pageMin) + " through " + str(pageMax))
    print("")
    return ingredient_recipes

# picks a random selection of 5 pages out of 100+ (~50 recipes)
# and returns a list of those recipes
def randomSearch(url):
    all_recipes = []
    request = urllib.request.Request(url)
    result = urllib.request.urlopen(request)
    json = result.read()

    pageMin = randint(1, 15)
    pageMax = pageMin + 5
    for x in range(pageMin, pageMax):
        try:
            url = url + "&p=" + str(x)
            request = urllib.request.Request(url)
            result = urllib.request.urlopen(request)
            json = result.read()
            recipes = jsonparse(json)
            for recipe in recipes:
                all_recipes.append(recipe)
        except:
            pass

    print("Searching pages " + str(pageMin) + " through " + str(pageMax))
    print("")
    return all_recipes

# picks a random recipe from a given list of recipes
def getRandomRecipe(recipes = [], *args):
    num = randint(0, len(recipes) - 1)
    return recipes[num]

def findBest(recipes = [], *args):
    # Set placeholder best score at 0
    best = Recipe(None, None, None)
    best.setScore(0)

    # For each recipe in the given list, compare the score with the current best
    # If the recipe is better, make it the new best
    # If they are the same, randomly either make the new recipe the best or leave the current one
    for recipe in recipes:
        if recipe.score > best.score:
            best = recipe
        if recipe.score == best.score:
            coin = randint(0, 1)
            if coin == 0:
                best = recipe
            else:
                pass

    # Return the best recipe
    return best

def scoreRecipes(recipes = [], usr_ingredients = [], *args):
    for recipe in recipes:
        score = 0
        for ingredient in usr_ingredients:
            if ingredient in recipe.ingredients:
                score += 1
        recipe.setScore(score)

# get the user search query
def getQuery():
    print("Enter search term:")
    query = input("> ")
    return query

# get the user ingredients, save in 'ingredients.txt'
def getIngredients():
    ingredients = []
    print("Enter ingredients, leave empty to exit")
    while True:
        search_ingredient = input("> ")
        if not search_ingredient:
            break
        else:
            ingredients.append(search_ingredient)
    return ingredients

# display all ingredients from 'ingredients.txt'
def displayIngredients(filename):
    file = open(filename, 'r')
    print("Current Ingredients:")
    for line in file:
        print(line.strip())
    file.close()

# write ingredients to 'ingredients.txt'
def writeIngredients(filename, ingredients):
    file = open(filename, 'a')
    old = importIngredients(filename)
    for i in ingredients:
        if (i not in old) and (i != " ") and (i != "") and (i != None):
            file.write(i + "\n")

# open ingredients and return as a list
def importIngredients(filename):
    user_ingredients = []
    file = open(filename, 'r')
    for line in file:
        line = line.strip()
        user_ingredients.append(line)
    file.close()
    return user_ingredients

# clear ingredients.txt
def deleteIngredients(filename):
    file = open(filename, 'w')
    file.close()

# after the recipe is displayed to the user (recipe.display())
# prompt the user for an action
def prompt(recipe):
    print("Look interesting?")
    print("Press 1 to open in browser and make shopping list")
    print("Press 2 to see a different recipe")
    print("Press any other button to go to the menu")
    choice = input("> ")
    return choice

# if the recipe is selected (user inputs 1 at prompt above)
# open the recipe in browser (if the program is being run as a command line tool)
# either way, generate a shopping list containing all ingredients that the user does not already have
def select(recipe):
    file = open("shoppinglist.txt", 'w')

    # Only open in browser if the program is being run from command line, not in GUI form
    if __name__ == "__main__":
        webbrowser.open_new_tab(recipe.link)

    user_ingredients = importIngredients("ingredients.txt")
    recipe_ingredients = recipe.ingredients.split(", ")
    
    for ingredient in recipe_ingredients:
        if ingredient not in user_ingredients:
            file.write(ingredient + "\n")
    file.close()

    file = open("shoppinglist.txt", 'r')
    print("Shopping list complete! You need:")
    for line in file:
        print(line.strip())

# reset query and ingredients
def reset():
    query = None
    ingredients = deleteIngredients("ingredients.txt")

query = None
ingredients = importIngredients("ingredients.txt")
recipes = []
allRecipes = []
ingrRecipes = []

if __name__ == "__main__":
    main(query, ingredients, recipes, allRecipes, ingrRecipes)
