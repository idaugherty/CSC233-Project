import tkinter as tk
from tkinter import Text, Toplevel, BooleanVar, END
import RecipeLogic

# ===================== RUSTIC THEME COLORS =====================
COLOR_BG = "#faf3e0"              # linen
COLOR_PANEL = "#fffdf6"           # soft cream
COLOR_BORDER = "#d2c4b0"          # warm brown edge
COLOR_ACCENT = "#c44536"          # rustic brick red
COLOR_ACCENT_DARK = "#a8372c"     # darker accent for hover

# ===================== MAIN WINDOW =====================
root = tk.Tk()
root.title("Recipe Book App")
root.geometry("900x600")          # increased to prevent overlap
root.resizable(False, False)
root.configure(bg=COLOR_BG)

# Allow right column and rows to expand properly
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(2, weight=1)

# ===================== RUSTIC BUTTON BUILDER =====================
def rustic_button(parent, text, command=None):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=COLOR_ACCENT,
        fg="white",
        activebackground=COLOR_ACCENT_DARK,
        activeforeground="white",
        relief=tk.RAISED,
        bd=2,
        padx=10,
        pady=5
    )

# ===================== ADD RECIPE WINDOW =====================
def opens_new_window():
    newWindow = Toplevel(root)
    newWindow.title("Add Recipe")
    newWindow.geometry("500x450")
    newWindow.resizable(False, False)
    newWindow.configure(bg=COLOR_BG)
    newWindow.grab_set()

    form_frame = tk.Frame(newWindow, bg=COLOR_BG)
    form_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

    tk.Label(form_frame, text="Recipe Name:", bg=COLOR_BG).grid(
        row=0, column=0, sticky="e", padx=10, pady=8
    )
    recipeEntryBox = tk.Entry(form_frame, width=35)
    recipeEntryBox.grid(row=0, column=1, sticky="w", padx=10, pady=8)

    tk.Label(form_frame, text="Ingredients:", bg=COLOR_BG).grid(
        row=1, column=0, sticky="ne", padx=10, pady=8
    )
    ingredientsTextWidget = Text(form_frame, height=5, width=35)
    ingredientsTextWidget.grid(row=1, column=1, sticky="w", padx=10, pady=8)

    tk.Label(form_frame, text="Instructions:", bg=COLOR_BG).grid(
        row=2, column=0, sticky="ne", padx=10, pady=8
    )
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

    submit_btn = rustic_button(newWindow, "Submit", submit_action)
    submit_btn.grid(row=3, column=0, columnspan=2, pady=15, padx=20, sticky="ew")

# ===================== LEFT SIDE FRAMES =====================
allergy_frame = tk.Frame(root, bg=COLOR_PANEL, relief=tk.GROOVE, bd=1)
allergy_frame.grid(row=0, column=0, padx=15, pady=5, sticky="nw")

tk.Label(allergy_frame, text="Filter by Dietary Restrictions:", bg=COLOR_PANEL).pack(pady=5)

checkbox_frame = tk.Frame(allergy_frame, bg=COLOR_PANEL)
checkbox_frame.pack(pady=5)

dairy_checkbox_var = BooleanVar()
tk.Checkbutton(checkbox_frame, text="Dairy", variable=dairy_checkbox_var, bg=COLOR_PANEL).pack(side=tk.LEFT, padx=10)

gluten_checkbox_var = BooleanVar()
tk.Checkbutton(checkbox_frame, text="Gluten", variable=gluten_checkbox_var, bg=COLOR_PANEL).pack(side=tk.LEFT, padx=10)

nut_checkbox_var = BooleanVar()
tk.Checkbutton(checkbox_frame, text="Nuts", variable=nut_checkbox_var, bg=COLOR_PANEL).pack(side=tk.LEFT, padx=10)

# Search Panel
search_frame = tk.Frame(root, bg=COLOR_PANEL, relief=tk.GROOVE, bd=1)
search_frame.grid(row=1, column=0, padx=15, pady=5, sticky="nw")

search_box = tk.Entry(search_frame, width=20)
search_box.pack(side=tk.LEFT, padx=5, pady=5)

search_button = rustic_button(search_frame, "Search")
search_button.pack(side=tk.LEFT, padx=5, pady=5)

show_all_button = rustic_button(search_frame, "Show All")
show_all_button.pack(side=tk.LEFT, padx=5, pady=5)

# Results panel
results_frame = tk.Frame(root, bg=COLOR_BG)
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
    results = RecipeLogic.update_search(
        term,
        nut_checkbox_var.get(),
        dairy_checkbox_var.get(),
        gluten_checkbox_var.get(),
    )
    results_text_widget.delete(0, END)
    for recipe in results:
        results_text_widget.insert(END, recipe.recipeName)


search_button.config(command=search_recipes)
show_all_button.config(command=populate_all_recipes)


def save_selected_recipe():
    selected = results_text_widget.curselection()
    if not selected:
        print("No recipe selected")
        return
    index = selected[0]
    recipe = RecipeLogic.book.recipes[index]
    RecipeLogic.save_to_list(recipe)
    print(f"{recipe.recipeName} added to grocery list")


# ===================== BOTTOM BUTTONS =====================
button_frame1 = tk.Frame(root, bg=COLOR_PANEL, relief=tk.GROOVE, bd=1)
button_frame1.grid(row=3, column=0, padx=15, pady=10, sticky="w")

add_recipe_button = rustic_button(button_frame1, "Add New Recipe", opens_new_window)
add_recipe_button.pack(side=tk.LEFT, padx=5, pady=5)

button_frame2 = tk.Frame(root, bg=COLOR_PANEL, relief=tk.GROOVE, bd=1)
button_frame2.grid(row=3, column=1, padx=15, pady=10, sticky="w")

save_list_button = rustic_button(button_frame2, "Save Ingredients", save_selected_recipe)
save_list_button.pack(side=tk.LEFT, padx=5, pady=5)

clear_list_button = rustic_button(button_frame2, "Clear Grocery List", RecipeLogic.clear_grocery_list)
clear_list_button.pack(side=tk.LEFT, padx=5, pady=5)

generate_list_button = rustic_button(button_frame2, "Generate Grocery List", RecipeLogic.generate_grocery_list)
generate_list_button.pack(side=tk.LEFT, padx=5, pady=5)

# ===================== RUN APP =====================
root.mainloop()

