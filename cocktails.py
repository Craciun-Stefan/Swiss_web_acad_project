import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

API_URL = "https://www.thecocktaildb.com/api/json/v1/1/"
#oz = 29.57

# search for cocktails by name list all matching results
def search_cocktail():
    # set the query from the search entry trim spaces
    query = search_entry.get().strip()
    # check if nothing entered
    if not query:
        messagebox.showwarning("Warning", "Please enter a cocktail name.")
        return

    # Send request to API
    response = requests.get(API_URL + f"search.php?s={query}")
    data = response.json()

    # check for drinks
    if data["drinks"]:
        cocktail_list.delete(0, tk.END)
        # insert each drink in the listbox
        for drink in data["drinks"]:
            cocktail_list.insert(tk.END, drink["strDrink"])
    else:
        # drink does not exist
        messagebox.showinfo("Not Found", "No cocktails found with that name.")


# search for cocktails by ingredient and list the cocktails
def search_ingredient():
    ingredient = ingredient_entry.get().strip()
    if not ingredient:
        messagebox.showwarning("Warning", "Please enter an ingredient.")
        return
    # clear the cocktail search bar
    search_entry.delete(0, tk.END)

    # send a request to API with ingredient
    response = requests.get(API_URL + f"filter.php?i={ingredient}")
    data = response.json()

    if data["drinks"]:
        cocktail_list.delete(0, tk.END)
        for drink in data["drinks"]:
            cocktail_list.insert(tk.END, drink["strDrink"])
    else:
        messagebox.showinfo("Not Found", "No cocktails found with that ingredient")
        

# fetch a random cocktail
def get_random_cocktail():
    # send a request to API for random cocktail
    response = requests.get(API_URL + "random.php")
    data = response.json()
    # display cocktail details
    display_cocktail(data["drinks"][0])


#handle cocktail selection from the list and display details.
def on_list_select(event):
    # get selected cocktail name from listbox
    selected = cocktail_list.get(tk.ANCHOR)
    # Update the search entry
    search_entry.delete(0, tk.END)
    search_entry.insert(0, selected)
    # send request to API
    response = requests.get(API_URL + f"search.php?s={selected}")
    data = response.json()
    if data["drinks"]:
        display_cocktail(data["drinks"][0])

# display details of a selected cocktail: name, category, type, ingredients, instructions and image.
def display_cocktail(cocktail):
    # update the cocktail's name, category, and type
    name_label.config(text=cocktail["strDrink"])
    category_label.config(text=f"Category: {cocktail['strCategory']}")
    alcoholic_label.config(text=f"Type: {cocktail['strAlcoholic']}")

    # display the instructions
    instructions_text.config(state=tk.NORMAL)
    instructions_text.delete(1.0, tk.END)
    instructions_text.insert(tk.END, cocktail["strInstructions"])
    instructions_text.config(state=tk.DISABLED)

    # display the list of ingredients and measurements
    ingredients_list.delete(0, tk.END)
    for i in range(1, 15):
        ingredient = cocktail.get(f"strIngredient{i}")
        measure = cocktail.get(f"strMeasure{i}")
        if ingredient:
            ingredients_list.insert(tk.END, f"{ingredient} - {measure if measure else ''}")

    # display the cocktail's image
    if cocktail["strDrinkThumb"]:
        image_url = cocktail["strDrinkThumb"]
        image_response = requests.get(image_url)
        img_data = Image.open(BytesIO(image_response.content)).resize((200, 200))
        img = ImageTk.PhotoImage(img_data)
        image_label.config(image=img)
        image_label.image = img


#main application window
root = tk.Tk()
root.title("Cocktail Finder")
root.geometry("500x800")

#cocktail search Bar
search_entry = ttk.Entry(root, width=40)
search_entry.pack(pady=10)
search_button = ttk.Button(
    root, text="Search Cocktail", command=search_cocktail)
search_button.pack()

#ingredient Search
ingredient_entry = ttk.Entry(root, width=40)
ingredient_entry.pack(pady=10)
ingredient_button = ttk.Button(
    root, text="Search by Ingredient", command=search_ingredient)
ingredient_button.pack()

#random cocktail button
random_button = ttk.Button(
    root, text="Random Cocktail", command=get_random_cocktail)
random_button.pack(pady=10)

#listbox for search results
cocktail_list = tk.Listbox(root, height=5)
cocktail_list.pack(pady=10)
cocktail_list.bind("<Double-Button-1>", on_list_select)

#cocktail info
name_label = ttk.Label(root, text="", font=("Arial", 14, "bold"))
name_label.pack()
category_label = ttk.Label(root, text="")
category_label.pack()
alcoholic_label = ttk.Label(root, text="")
alcoholic_label.pack()

#ingredients List
ingredients_list = tk.Listbox(root, height=6)
ingredients_list.pack(pady=10)

#instructions
instructions_text = tk.Text(root, height=5, wrap=tk.WORD, state=tk.DISABLED)
instructions_text.pack(pady=10)

#image
image_label = ttk.Label(root)
image_label.pack()


root.mainloop()