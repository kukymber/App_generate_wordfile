import tkinter as tk
from tkinter import ttk, Canvas, messagebox
import cv2
import pytesseract
import re
from PIL import Image, ImageTk
from docxtpl import DocxTemplate

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

seria = [elem for elem in word_list if any(char.isalpha() for char in elem)]

# Filter list with data
num_list = [num for num in filter(lambda num: num.isnumeric(), numbers_list)]
words_list = [word for word in filter(lambda word: word.isalpha(), word_list)]

# Extract date of birth from text (default image)
date_of_birth = re.findall("\d{2}[./,]?\d{2}[./,]?\d{4}", text)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter App")
        self.geometry("800x800")

        # Creating fields and initializing variables
        self.create_date_of_birth_field()
        self.create_name_fields()
        self.create_who_gave_passport_field()
        self.create_passport_series_number_fields()
        self.create_passport_number_fields()
        self.create_canvas()
        self.create_generate_word_file_button()
        # Initialize variables to store selected values
        self.date_birth = None
        self.selected_names = ["", "", ""]
        self.name_combos = ["", "", ""]
        self.selected_who_gave = ["", "", ""]
        self.selected_seria = []
        self.passport_number = None

    def create_date_of_birth_field(self):
        label = ttk.Label(self, text="Date of Birth:")
        label.grid(column=0, row=5, padx=10, pady=10)

        dob_entry = ttk.Entry(self, state='ACTIVE')
        dob_entry.insert(0, string=date_of_birth[0])
        dob_entry.grid(column=1, row=5, padx=10, pady=10)

        def selected_date_of_birth():
            self.date_birth = dob_entry.get()
            print(self.date_birth)

    def create_name_fields(self):
        self.name_combos = []
        for i in range(3):
            label = ttk.Label(self, text=f"{['First', 'Middle', 'Last'][i]} Name:")
            label.grid(column=0, row=i, padx=10, pady=10)

            combo = ttk.Combobox(self, values=words_list[::-1], state="normal")
            combo.grid(column=1, row=i, padx=10, pady=10)
            self.name_combos.append(combo)

            # Bind the on_select_name function to the ComboboxSelected event of the
