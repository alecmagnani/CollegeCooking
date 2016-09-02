from flask import (
        Flask,
        request,
        render_template,
        redirect,
)

import whatsfordinner

app = Flask(__name__)

@app.route('/')
def home(recipe = None, usr_ingredients = None):
    usr_ingredients = whatsfordinner.importIngredients("ingredients.txt")
    url = whatsfordinner.getIngredientSearchURL(None, usr_ingredients)
    print(url)
    recipes = whatsfordinner.ingredientSearch(url)
    recipe = whatsfordinner.getRandomRecipe(recipes)

    usr_ingredients = whatsfordinner.importIngredients("ingredients.txt")

    return render_template('webpage.html', recipe=recipe, usr_ingredients=usr_ingredients)

@app.route('/', methods=['POST'])
def home_add_ingredient(recipe=None, usr_ingredients=None):

    ingredient = request.form['Add Ingredient']
    
    usr_ingredients = whatsfordinner.importIngredients("ingredients.txt")
    if ingredient not in usr_ingredients:
        usr_ingredients.append(ingredient)
    else:
        usr_ingredients.remove(ingredient)
    whatsfordinner.deleteIngredients("ingredients.txt")
    whatsfordinner.writeIngredients("ingredients.txt", usr_ingredients)

    return redirect('/')


if __name__ == '__main__':
    app.run()
