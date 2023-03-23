import tkinter as tk
from tkinter import ttk
import cv2
import pytesseract
import re
from PIL import Image

path = "/home/anatolii/python_project/pythonProject9/passport.jpg"

# Reading an image in default mode
img = cv2.imread(path)

# Rotate image for scan numbers
img2 = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

# Read image and translate in text and numbers
text = pytesseract.image_to_string(img, lang="rus")
numbers = pytesseract.image_to_string(img2, lang="rus")

# Create lists with data
word_list = text.split()
numbers_list = numbers.split()

# Filter list with data
num_list = [int(num) for num in filter(
    lambda num: num.isnumeric(), numbers_list)]

words_list = [word for word in filter(
    lambda word: word.isalpha(), word_list)]
# take date of brith from text (default image)
date_of_brith = re.search("\d{2}[./,]?\d{2}[./,]?\d{4}", text)

# Input result
# print(num_list)
# print(words_list)
# print(date_of_brith[0])


class App(tk.Tk, words_list):
    def __init__(self):
        super().__init__()
        self.title("Tkinter App")
        self.geometry("400x400")

        # Creating list-based fields
        self.create_list_fields(words_list)

        # Creating the field for 'yek' data
        self.create_yek_field()

    def create_list_fields(self):
        # Sample data for list fields
        lists_data = [
            ["Option A1", "Option A2", "Option A3"],
            ["Option B1", "Option B2", "Option B3"],
            ["Option C1", "Option C2", "Option C3"],
            ["Option D1", "Option D2", "Option D3"],
            ["Option E1", "Option E2", "Option E3"],
            ["Option F1", "Option F2", "Option F3"]
        ]

        for i, data in enumerate(lists_data):
            label = ttk.Label(self, text=f"Field {i+1}:")
            label.grid(column=0, row=i, padx=10, pady=10)

            combo = ttk.Combobox(self, values=data, state="readonly")
            combo.grid(column=1, row=i, padx=10, pady=10)

    def create_yek_field(self):
        label = ttk.Label(self, text="Field 7:")
        label.grid(column=0, row=6, padx=10, pady=10)

        yek_entry = ttk.Entry(self)
        yek_entry.grid(column=1, row=6, padx=10, pady=10)

        # Function to validate 'yek' data
        def is_yek_data(data):
            return data.lower() == "yek"

        def validate_yek_data(*args):
            if is_yek_data(yek_entry.get()):
                submit_button.config(state="normal")
            else:
                submit_button.config(state="disabled")

        # Validate 'yek' data on key release
        yek_entry.bind("<KeyRelease>", validate_yek_data)

        submit_button = ttk.Button(self, text="Submit", state="disabled")
        submit_button.grid(column=1, row=7, padx=10, pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()