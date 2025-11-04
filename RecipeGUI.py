import tkinter
from tkinter.ttk import *

#creating main app window
root = tkinter.Tk()
#adding title to window
root.title("Recipe Book  App")
#setting screen size
root.geometry("350x250")

#creating recipe label and text area(widget)
recipeLabel = Label(root, text = "Enter the recipe name")
recipeLabel.grid(padx=10, pady=10,row=0, column=0)
recipeEntryBox = Entry(root, width=20)
recipeEntryBox.grid(padx=10, pady=10,row=0, column=2)

#creating ingredients label and text area(widget)
ingredientsLabel = Label(root, text = "Enter the ingredients ")
ingredientsLabel.grid(padx=10, pady=10, row=2, column=0)
ingredientsTextWidget = tkinter.Text(root, height=5, width = 20)
ingredientsTextWidget.grid(padx=10, pady=10, row=2, column=2)

#creating instructions label and text area(widget)
instructionsLabel = Label(root, text = "Enter the instructions ")
instructionsLabel.grid(padx=10, pady=10, row=4, column=0)
instructionsTextWidget = tkinter.Text(root, height=5, width = 20)
instructionsTextWidget.grid(padx=10, pady=10, row=4, column=2)


#run the event loop
root.mainloop()
