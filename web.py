from flask import (
        Flask,
        request,
        render_template,
)

import whatsfordinner

app = Flask(__name__)

@app.route('/')
def home(recipe = None, usr_ingredients = None):
    url = whatsfordinner.getIngredientSearchURL(None)
    recipes = whatsfordinner.ingredientSearch(url)
    recipe = whatsfordinner.getRandomRecipe(recipes)

    usr_ingredients = whatsfordinner.importIngredients("ingredients.txt")

    return render_template('webpage.html', recipe=recipe, usr_ingredients=usr_ingredients)

@app.route('/', methods=['POST'])
def home_add_ingredient(recipe=None, usr_ingredients=None):

    ingredient = request.form['Add Ingredient']
    
    usr_ingredients = whatsfordinner.importIngredients("ingredients.txt")
    usr_ingredients.append(ingredient)
    whatsfordinner.deleteIngredients("ingredients.txt")
    whatsfordinner.writeIngredients("ingredients.txt", usr_ingredients)

    url = whatsfordinner.getIngredientSearchURL(None)
    recipes = whatsfordinner.ingredientSearch(url)
    recipe = whatsfordinner.getRandomRecipe(recipes)

    return render_template('webpage.html', recipe=recipe, usr_ingredients=usr_ingredients)


if __name__ == '__main__':
    app.run()
