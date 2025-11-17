import tkinter as tk
from tkinter import Text, Toplevel, BooleanVar, END
from tkinter.ttk import Button  # Only ttk.Button is safe
import RecipeLogic

# ===================== MAIN WINDOW =====================
root = tk.Tk()
root.title("Recipe Book App")
root.geometry("900x500")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# ===================== ADD RECIPE WINDOW =====================
def opens_new_window():
    newWindow = Toplevel(root)
    newWindow.title("Add Recipe")
    newWindow.geometry("500x450")
    newWindow.resizable(False, False)
    newWindow.configure(bg="#f0f0f0")
    newWindow.grab_set()

    form_frame = tk.Frame(newWindow, bg="#f0f0f0")
    form_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

    # Labels are tk.Label now
    tk.Label(form_frame, text="Recipe Name:", bg="#f0f0f0").grid(row=0, column=0, sticky="e", padx=10, pady=8)
    recipeEntryBox = tk.Entry(form_frame, width=35)
    recipeEntryBox.grid(row=0, column=1, sticky="w", padx=10, pady=8)

    tk.Label(form_frame, text="Ingredients:", bg="#f0f0f0").grid(row=1, column=0, sticky="ne", padx=10, pady=8)
    ingredientsTextWidget = Text(form_frame, height=5, width=35)
    ingredientsTextWidget.grid(row=1, column=1, sticky="w", padx=10, pady=8)

    tk.Label(form_frame, text="Instructions:", bg="#f0f0f0").grid(row=2, column=0, sticky="ne", padx=10, pady=8)
    instructionsTextWidget = Text(form_frame, height=5, width=35)
    instructionsTextWidget.grid(row=2, column=1, sticky="w", padx=10, pady=8)

    def submit_action():
        recipe_name = recipeEntryBox.get()
        ingredients = ingredientsTextWidget.get("1.0", "end-1c")
        instructions = instructionsTextWidget.get("1.0", "end-1c")
        try:
            RecipeLogic.add_recipe(recipe_name, ingredients, instructions)
            RecipeLogic.print_all_recipes()
        except Exception as e:
            print("Error saving recipe:", e)

    # ttk.Button is fine here
    Button(newWindow, text="Submit", command=submit_action).grid(
        row=3, column=0, columnspan=2, pady=15, sticky="ew", padx=20
    )

# ===================== LEFT SIDE FRAMES =====================
allergy_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=1)
allergy_frame.grid(row=0, column=0, padx=15, pady=5, sticky="nw")
tk.Label(allergy_frame, text="Filter by Dietary Restrictions:", bg="#ffffff").pack(pady=5)

checkbox_frame = tk.Frame(allergy_frame, bg="#ffffff")
checkbox_frame.pack(pady=5)
dairy_checkbox_var = BooleanVar()
tk.Checkbutton(checkbox_frame, text="Dairy", variable=dairy_checkbox_var, bg="#ffffff").pack(side=tk.LEFT, padx=10)
gluten_checkbox_var = BooleanVar()
tk.Checkbutton(checkbox_frame, text="Gluten", variable=gluten_checkbox_var, bg="#ffffff").pack(side=tk.LEFT, padx=10)
nut_checkbox_var = BooleanVar()
tk.Checkbutton(checkbox_frame, text="Nuts", variable=nut_checkbox_var, bg="#ffffff").pack(side=tk.LEFT, padx=10)

search_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=1)
search_frame.grid(row=1, column=0, padx=15, pady=5, sticky="nw")
search_box = tk.Entry(search_frame, width=20)
search_box.pack(side=tk.LEFT, padx=5, pady=5)
search_button = Button(search_frame, text="Search")
search_button.pack(side=tk.LEFT, padx=5, pady=5)
show_all_button = Button(search_frame, text="Show All")
show_all_button.pack(side=tk.LEFT, padx=5, pady=5)

results_frame = tk.Frame(root, bg="#f0f0f0")
results_frame.grid(row=2, column=0, padx=15, pady=5, sticky="nw")
results_text_widget = tk.Listbox(results_frame, height=20, width=50)
results_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(results_frame, orient=tk.VERTICAL, command=results_text_widget.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
results_text_widget.config(yscrollcommand=scrollbar.set)

# ===================== RIGHT SIDE =====================
recipe_display = Text(root, width=50, height=25)
recipe_display.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="n")

# ===================== FUNCTIONS =====================
def populate_all_recipes():
    results_text_widget.delete(0, END)
    for recipe in RecipeLogic.book.recipes:
        results_text_widget.insert(END, recipe.recipeName)

def on_recipe_click(event):
    selected = results_text_widget.curselection()
    if not selected:
        return
    index = selected[0]
    recipe = RecipeLogic.book.recipes[index]
    recipe_display.delete("1.0", END)
    text = f"Recipe Name: {recipe.recipeName}\n\nIngredients:\n"
    for ing in recipe.ingredients:
        text += f" - {ing}\n"
    text += f"\nInstructions:\n{recipe.instructions}"
    recipe_display.insert(END, text)

results_text_widget.bind("<<ListboxSelect>>", on_recipe_click)
populate_all_recipes()

def search_recipes():
    term = search_box.get().strip()
    if not term:
        populate_all_recipes()
        return
    results = RecipeLogic.update_search(term, nut_checkbox_var.get(), dairy_checkbox_var.get(), gluten_checkbox_var.get())
    results_text_widget.delete(0, END)
    for recipe in results:
        results_text_widget.insert(END, recipe.recipeName)

search_button.config(command=search_recipes)
show_all_button.config(command=populate_all_recipes)

# ===================== BOTTOM BUTTONS =====================
button_frame1 = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=1)
button_frame1.grid(row=3, column=0, padx=15, pady=10, sticky="w")
add_recipe_button = Button(button_frame1, text="Add New Recipe", command=opens_new_window)
add_recipe_button.pack(side=tk.LEFT, padx=5, pady=5)

button_frame2 = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=1)
button_frame2.grid(row=3, column=1, padx=15, pady=10, sticky="w")
save_list_button = Button(button_frame2, text="Save Ingredients", command=RecipeLogic.save_to_list)
save_list_button.pack(side=tk.LEFT, padx=5, pady=5)
clear_list_button = Button(button_frame2, text="Clear Grocery List", command=RecipeLogic.clear_grocery_list)
clear_list_button.pack(side=tk.LEFT, padx=5, pady=5)
generate_list_button = Button(button_frame2, text="Generate Grocery List", command=RecipeLogic.generate_grocery_list)
generate_list_button.pack(side=tk.LEFT, padx=5, pady=5)

# ===================== RUN APP =====================
root.mainloop()
