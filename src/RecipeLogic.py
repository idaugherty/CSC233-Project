from Classes.Recipe import Recipe
from Classes.RecipeBook import RecipeBook

# Maintain a RecipeBook instance for storing recipes
book = RecipeBook()

def add_recipe(recipeName: str, ingredients: str, instructions: str):

    # create a Recipe object and add it to the book
    newRecipe = Recipe(recipeName, ingredients, instructions)
    # RecipeBook exposes addRecipe()
    book.addRecipe(newRecipe)
    return newRecipe