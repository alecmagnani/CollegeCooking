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
    usr_ingredients = cache.get('usr_ingredients')
    url = whatsfordinner.getIngredientSearchURL(None, usr_ingredients)

    recipes = whatsfordinner.ingredientSearch(url)
    #Give each recipe a score based on how many ingredients it has in common with the user's list of ingredients
    if usr_ingredients != None:
        for recipe in recipes:
            score = 0
            for ingredient in usr_ingredients:
                if ingredient in recipe.ingredients:
                    score += 1
            recipe.setScore(score)

        recipe = whatsfordinner.findBest(recipes)
    else:
        recipe = whatsfordinner.getRandomRecipe(recipes)

    return render_template('webpage.html', recipe=recipe, usr_ingredients=usr_ingredients)

@app.route('/', methods=['POST'])
def home_add_ingredient(recipe=None, usr_ingredients=None):

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

    elif request.form['action'] == "Reset":
        usr_ingredients = []
        cache.set('usr_ingredients', usr_ingredients)

        return home(None, usr_ingredients)

if __name__ == '__main__':
    app.run()
