import tkinter as tk
from tkinter import Toplevel, BooleanVar, END
from tkinter.ttk import Button, Label, Entry
import RecipeLogic

root = tk.Tk()
root.title("Recipe Book App")
root.geometry("800x500")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# Creates a new window for adding recipes
def opens_new_window():
    # opens a new window in front of the parent window
    newWindow = Toplevel(root)
    newWindow.title("Add Recipe")
    newWindow.geometry("500x450")
    newWindow.resizable(False, False)
    newWindow.configure(bg="#f0f0f0")
    newWindow.grab_set()

    # Configure grid to center content
    newWindow.grid_columnconfigure(0, weight=1)
    newWindow.grid_columnconfigure(1, weight=1)
    newWindow.grid_columnconfigure(2, weight=1)
    
    # Add a frame for form inputs
    form_frame = tk.Frame(newWindow, bg="#f0f0f0")
    form_frame.grid(row=1, column=0, columnspan=1, padx=20, pady=10, sticky="nsew")

    recipeLabel = Label(form_frame, text="Recipe Name:", background="#f0f0f0")
    recipeLabel.grid(padx=10, pady=8, row=0, column=0, sticky="e")
    recipeEntryBox = Entry(form_frame, width=35)
    recipeEntryBox.grid(padx=10, pady=8, row=0, column=1, sticky="w")

    ingredientsLabel = Label(form_frame, text="Ingredients:", background="#f0f0f0")
    ingredientsLabel.grid(padx=10, pady=8, row=1, column=0, sticky="ne")
    ingredientsTextWidget = tk.Text(form_frame, height=5, width=35)
    ingredientsTextWidget.grid(padx=10, pady=8, row=1, column=1, sticky="w")

    instructionsLabel = Label(form_frame, text="Instructions:", background="#f0f0f0")
    instructionsLabel.grid(padx=10, pady=8, row=2, column=0, sticky="ne")
    instructionsTextWidget = tk.Text(form_frame, height=5, width=35)
    instructionsTextWidget.grid(padx=10, pady=8, row=2, column=1, sticky="w")


    def submit_action():
        """Collect field values and pass them to the logic module."""
        recipe_name = recipeEntryBox.get()
        ingredients = ingredientsTextWidget.get("1.0", "end-1c")
        instructions = instructionsTextWidget.get("1.0", "end-1c")
        try:
            RecipeLogic.add_recipe(recipe_name, ingredients, instructions)
            print(f"Saved recipe: {recipe_name}")
            #prints all recipes after adding a new one (for testing)
            RecipeLogic.print_all_recipes() 
            
        except Exception as e:
            print("Error saving recipe:", e)


    # creating a submit button
    submitButton = Button(newWindow, text="Submit", command=submit_action)
    submitButton.grid(row=2, column=0, columnspan=3, pady=15, sticky="ew", padx=20)

# Allergy filter frame
allergy_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=1)
allergy_frame.grid(row=0, column=0, columnspan=1, padx=15, pady=10, sticky="w")

allergyLabel = Label(allergy_frame, text="Filter by Dietary Restrictions:", background="#ffffff")
allergyLabel.pack(pady=5, anchor="center")

checkbox_frame = tk.Frame(allergy_frame, bg="#ffffff")
checkbox_frame.pack(pady=5, anchor="center")

dairy_checkbox_var = BooleanVar()
dairy_allergy_checkbox = tk.Checkbutton(checkbox_frame, text="Dairy", variable=dairy_checkbox_var, bg="#ffffff")
dairy_allergy_checkbox.pack(side=tk.LEFT, padx=10)

gluten_checkbox_var = BooleanVar()
gluten_allergy_checkbox = tk.Checkbutton(checkbox_frame, text="Gluten", variable=gluten_checkbox_var, bg="#ffffff")
gluten_allergy_checkbox.pack(side=tk.LEFT, padx=10)

nut_checkbox_var = BooleanVar()
nut_allergy_checkbox = tk.Checkbutton(checkbox_frame, text="Nuts", variable=nut_checkbox_var, bg="#ffffff")
nut_allergy_checkbox.pack(side=tk.LEFT, padx=10)

# Search frame
search_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=1)
search_frame.grid(row=1, column=0, columnspan=1, padx=15, pady=10, sticky="w")

search_box = Entry(search_frame, width=20)
search_box.pack(side=tk.LEFT, padx=5, pady=5, anchor="center", expand=True)

# Search results frame
results_frame = tk.Frame(root, bg="#f0f0f0")
results_frame.grid(row=2, column=0, columnspan=1, padx=15, pady=10, sticky="ws")

# ListBox with scroll bar with all eligible recipes
results_text_widget = tk.Listbox(results_frame, height=15, width=50)
results_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(results_frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
results_text_widget.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=results_text_widget.yview)

# Function to populate listbox with all recipes (initial load)
def populate_all_recipes():
    results_text_widget.delete(0, END)
    for recipe in RecipeLogic.book.recipes:
        results_text_widget.insert(END, recipe.recipeName)

# Load all recipes initially
populate_all_recipes()

def search_recipes():
    search_term = search_box.get().strip()
    
    # If search term is empty, show all recipes
    if not search_term:
        populate_all_recipes()
        return
        
    results = RecipeLogic.update_search(
        search_term,
        nut_checkbox_var.get(),
        dairy_checkbox_var.get(),
        gluten_checkbox_var.get()
    )

    # Clear previous results
    results_text_widget.delete(0, END)

    # Insert new results
    for recipe in results:
        results_text_widget.insert(END, recipe.recipeName)

search_button = Button(search_frame, text="Search", command=search_recipes)
search_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="center", expand=True)

show_all_button = Button(search_frame, text="Show All", command=populate_all_recipes)
show_all_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="center", expand=True)

button_frame1 = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=1)
button_frame1.grid(row=3, column=0, columnspan=1, padx=15, pady=10, sticky="w")

add_recipe_button = Button(button_frame1, text="Add New Recipe", command=opens_new_window)
add_recipe_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="center", expand=True)

#right side of main window

button_frame2 = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=1)
button_frame2.grid(row=3, column=2, columnspan=1, padx=15, pady=10, sticky="w")

#save to list button
#command=RecipeLogic.save_to_list()
save_list_button = Button(button_frame2, text="Save Ingredients", )
save_list_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="center", expand=True)

#clear list button
clear_list_button = Button(button_frame2, text="Clear Grocery List", command=RecipeLogic.clear_grocery_list())
clear_list_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="center", expand=True)

#generatelist button
generate_list_button = Button(button_frame2, text="Generate Grocery List", command=RecipeLogic.generate_grocery_list())
generate_list_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="center", expand=True)
# display selected recipe details when clicked?


# run the event loop
root.mainloop()
