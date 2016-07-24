import sys
import xml.etree.ElementTree as ET
import urllib.request
import webbrowser
from random import randint
from recipe import Recipe

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

        while True:
            recipe = getRandomRecipe(ingrRecipes)
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

def getIngredientSearchURL(query, ingredients = [], *args):
    url = "http://recipepuppy.com/api?"
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

def getRandomSearchURL(query):
    url = "http://recipepuppy.com/api?"
    if (query != None) and (query != "") and (query != " "):
        url = url + "&q" + query
    print("Searching: " + url)
    print("")
    return url

def ingredientSearch(url):
    ingredient_recipes = []
    for x in range(1, 2):
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

    print("Finished search on page " + str(x) + ", selecting from " + str(Recipe.recipeCount) + " recpipes")
    print("")
    return ingredient_recipes

def randomSearch(url):
    all_recipes = []
    request = urllib.request.Request(url)
    result = urllib.request.urlopen(request)
    json = result.read()

    for x in range(1, 2):
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

    print("Finished search on page " + str(x))
    print("Collected " + str(Recipe.recipeCount) + " recipes")
    return all_recipes

def getRandomRecipe(recipes = [], *args):
    num = randint(0, len(recipes) - 1)
    return recipes[num]

def getQuery():
    print("Enter search term:")
    query = input("> ")
    return query

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

def displayIngredients(filename):
    file = open(filename, 'r')
    print("Current Ingredients:")
    for line in file:
        print(line.strip())
    file.close()

def writeIngredients(filename, ingredients):
    file = open(filename, 'a')
    old = importIngredients(filename)
    for i in ingredients:
        if i not in old:
            file.write(i + "\n")

def importIngredients(filename):
    user_ingredients = []
    file = open(filename, 'r')
    for line in file:
        line = line.strip()
        user_ingredients.append(line)
    file.close()
    return user_ingredients

def deleteIngredients(filename):
    file = open(filename, 'w')
    file.close()

def prompt(recipe):
    print("Look interesting?")
    print("Press 1 to open in browser and make shopping list")
    print("Press 2 to see a different recipe")
    print("Press any other button to go to the menu")
    choice = input("> ")
    return choice

def select(recipe):
    file = open("shoppinglist.txt", 'w')
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
