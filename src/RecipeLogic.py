from Classes.Recipe import Recipe
from Classes.RecipeBook import RecipeBook

# Maintain a RecipeBook instance for storing recipes
book = RecipeBook()

def add_recipe(recipeName: str, ingredients: str, instructions: str):

    # create a Recipe object and add it to the book
    newRecipe = Recipe(recipeName, ingredients, instructions)

    #dietary restriction checks (limited ingredients for demo purposes)
    if "peanut" in ingredients.lower() or "almond" in ingredients.lower() or "walnut" in ingredients.lower() or "cashew" in ingredients.lower() or "pecan" in ingredients.lower():
        newRecipe.recipeAllergies = True
        newRecipe.restrictions.append("Nuts")
    if "milk" in ingredients.lower() or "cheese" in ingredients.lower() or "butter" in ingredients.lower():
        newRecipe.recipeAllergies = True
        newRecipe.restrictions.append("Dairy")
    if "wheat" in ingredients.lower() or "flour" in ingredients.lower() or "bread" in ingredients.lower() or "pasta" in ingredients.lower():
        newRecipe.recipeAllergies = True
        newRecipe.restrictions.append("Gluten")
    
    book.addRecipe(newRecipe)
    return newRecipe

#search button logic
def update_search(search_term, filter_nuts, filter_dairy, filter_gluten):
    results = []
    for recipe in book.recipes:
        # Convert ingredients to string for searching (handle both list and string formats)
        ingredients_str = ', '.join(recipe.ingredients) if isinstance(recipe.ingredients, list) else str(recipe.ingredients)
        
        # Check if search term matches ingredients
        if (search_term.lower() in ingredients_str.lower() or search_term.lower() in recipe.recipeName.lower()):
            
            # Check allergy restrictions if recipe has allergies
            skip_recipe = False
            if recipe.recipeAllergies:
                if "Nuts" in recipe.restrictions and filter_nuts:
                    skip_recipe = True
                if "Dairy" in recipe.restrictions and filter_dairy:
                    skip_recipe = True
                if "Gluten" in recipe.restrictions and filter_gluten:
                    skip_recipe = True
            
            # Add recipe to results if it passes all filters
            if not skip_recipe:
                results.append(recipe)
    
    return results


#prints all recipes in the recipe book (testing method)
def print_all_recipes():
    book.printAllRecipes()


# Initialize grocery list
grocery_list = []

#save list of recipes for grocery list
def save_to_list(recipe):
    grocery_list.append(recipe)
   
#clear list of recipes for grocery list
def clear_grocery_list():
    grocery_list.clear()
    print("List Cleared")

#generate grocery list from selected recipes
def generate_grocery_list():
    print("List Generated")
   