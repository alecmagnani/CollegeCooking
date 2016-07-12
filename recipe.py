class Recipe:
    recipeCount = 0;

    def __init__(self, title, link, ingredients):
        self.title = title
        self.link = link
        self.ingredients = ingredients
        Recipe.recipeCount += 1

    def display(self):
        print("Title: " + self.title)
        print("Link: " + self.link)
        print("Ingredients: " + self.ingredients)
