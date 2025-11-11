try:
    from .Recipe import Recipe
except ImportError:
    from Recipe import Recipe
class RecipeBook:
    #this is the constructor
    def __init__(self):

        #initialize recipebook with recipe examples
        ex_recipe1 = Recipe("Peanut Butter Cookies", ["Sugar", "Peanut Butter", "Eggs"], "Mix ingredients, roll into balls and place on a baking sheet, bake at 350F for 10-12 minutes.")
        ex_recipe1.recipeAllergies = True
        ex_recipe1.restrictions.append("Nuts")
        ex_recipe2 = Recipe("Grilled Cheese Sandwich", ["Bread", "Cheese", "Butter"], "Butter the bread, place cheese between slices, and grill until golden brown.")
        ex_recipe2.recipeAllergies = True
        ex_recipe2.restrictions.append("Dairy")
        ex_recipe3 = Recipe("Pasta Primavera", ["Pasta", "Mixed Vegetables", "Olive Oil", "Garlic"], "Cook pasta, sauté vegetables in olive oil with garlic, and combine.")
        ex_recipe3.recipeAllergies = True
        ex_recipe3.restrictions.append("Gluten")
        ex_recipe4 = Recipe("Fruit Salad", ["Assorted Fruits", "Honey", "Lime Juice"], "Chop fruits, mix with honey and lime juice, and chill before serving.")
        self.recipes = [ex_recipe1, ex_recipe2, ex_recipe3, ex_recipe4]

    #add recipe method
    def addRecipe(self, recipe):
        self.recipes.append(recipe)
        print(recipe.recipeName)
        print(recipe.ingredients)
        print(recipe.instructions)
    
    #print all recipes in the recipe book
    def printAllRecipes(self):
        if not self.recipes:
            print("No recipes in the recipe book.")
            return
        print("=== ALL RECIPES ===")
        for i, recipe in enumerate(self.recipes, 1):
            print(f"\n--- Recipe #{i}: {recipe.recipeName} ---")
            print(f"Ingredients: {', '.join(recipe.ingredients) if isinstance(recipe.ingredients, list) else recipe.ingredients}")
            print(f"Instructions: {recipe.instructions}")
            print("-" * 50)