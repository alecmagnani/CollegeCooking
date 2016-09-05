from flask import (
        Flask,
        request,
        render_template,
        redirect,
)
from werkzeug.contrib.cache import SimpleCache

import whatsfordinner

app = Flask(__name__)
usr_ingredients = []
cache = SimpleCache()

@app.route('/')
def home(recipe = None, usr_ingredients = None):
    #Get user ingredients from cache, generate search url, and gather a list of recipes
    usr_ingredients = cache.get('usr_ingredients')
    url = whatsfordinner.getIngredientSearchURL(None, usr_ingredients)
    recipes = whatsfordinner.ingredientSearch(url)

    #Give each recipe a score based on how many ingredients it has in common with the user's list of ingredients
    #Return one of the best possible recipes. This makes it more likely that the recipe will contain the user's ingredients
    if usr_ingredients != None:
        for recipe in recipes:
            score = 0
            for ingredient in usr_ingredients:
                if ingredient in recipe.ingredients:
                    score += 1
            recipe.setScore(score)

        recipe = whatsfordinner.findBest(recipes)
    else:
        #If user ingredient list is empty, just return a random recipe. No need to rate them
        recipe = whatsfordinner.getRandomRecipe(recipes)

    return render_template('webpage.html', recipe=recipe, usr_ingredients=usr_ingredients)

@app.route('/', methods=['POST'])
def home_add_ingredient(recipe=None, usr_ingredients=None):

    #If the button pressed is the Add Ingredient Button
    #Get the text from the field and add it to the user ingredients list
    #If the item is already in the list, remove it
    if request.form['action'] == "Add Ingredient":
        ingredient = request.form['Add Ingredient']
        
        usr_ingredients = cache.get('usr_ingredients')
        if usr_ingredients == None:
            usr_ingredients = [ingredient]
            cache.set('usr_ingredients', usr_ingredients)
            return home(None, usr_ingredients)
        if ingredient not in usr_ingredients:
            usr_ingredients.append(ingredient)
        else:
            usr_ingredients.remove(ingredient)

        cache.set('usr_ingredients', usr_ingredients)
        return home(None, usr_ingredients)

    #If the button pressed is Reset, cleare the cache and return home
    elif request.form['action'] == "Reset":
        usr_ingredients = []
        cache.set('usr_ingredients', usr_ingredients)

        return home(None, usr_ingredients)

if __name__ == '__main__':
    app.run()
