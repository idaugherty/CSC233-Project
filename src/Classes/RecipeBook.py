class RecipeBook:
    #this is the constructor
    def __init__(self):
        self.recipes = []

    #add recipe method
    def addRecipe(self, recipe):
        self.recipes.append(recipe)
        print(recipe.recipeName)
        print(recipe.ingredients)
        print(recipe.instructions)