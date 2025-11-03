import tkinter
from tkinter.ttk import *

#creating main app window
root = tkinter.Tk()
#adding title to window
root.title("Recipe Book  App")
#setting screen size
root.geometry("350x250")

#creating recipe label and input box
recipeLabel = Label(root, text = "Enter the recipe name")
recipeLabel.grid(row=0, column=0)
recipeEntryBox = Entry(root, width=20)
recipeEntryBox.grid(row=0, column=2)

#creating ingredients label and input box
ingredientsLabel = Label(root, text = "Enter the ingredients ")
ingredientsLabel.grid(row=2, column=0)
ingredientsEntryBox = Entry(root, width=20)
ingredientsEntryBox.grid(row=2, column=2)

#creating instructions label and input box
instructionsLabel = Label(root, text = "Enter the instructions ")
instructionsLabel.grid(row=4, column=0)
instructionsEntryBox = Entry(root, width=20)
instructionsEntryBox.grid(row=4, column=2)


#run the event loop
root.mainloop()
