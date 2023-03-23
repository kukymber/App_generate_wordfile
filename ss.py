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
num_list = [num for num in filter(
    lambda num: num.isnumeric(), numbers_list)]

words_list = [word for word in filter(
    lambda word: word.isalpha(), word_list)]

# take date of brith from text (default image)
date_of_birth = re.findall("\d{2}[./,]?\d{2}[./,]?\d{4}", text)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter App")
        self.geometry("800x800")
        # Creating the date of birth field
        self.date_of_birth_field()
        # Creating list-based fields for names
        self.name_fields()
        # Creating the "Who Gave Passport" field with multiple selections
        self.who_gave_passport_field()
        self.selected_who_gave = []
        # Creating the fields for passport series and number
        self.passport_series_number_fields()
        self.selected_seria = []
        self.passport_number_fields()
        # Adding the canvas for the image
        self.canvas = tk.Canvas(self, width=400, height=600)
        self.canvas.grid(column=2, row=0, rowspan=7, padx=10, pady=10)
        # Loading and displaying the image
        self.show_image()
        self.generate_word_file()
        self.generate_word_file_button()

    def name_fields(self):

        for i in range(3):
            label = ttk.Label(self, text=f"{['First', 'Middle', 'Last'][i]} Name:")
            label.grid(column=0, row=i, padx=10, pady=10)

            combo = ttk.Combobox(self, values=words_list[::-1], state="normal")
            combo.grid(column=1, row=i, padx=10, pady=10)



    def who_gave_passport_field(self):
        label = ttk.Label(self, text="Who Gave Passport:")
        label.grid(column=0, row=3, padx=10, pady=10)

        listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        listbox.grid(column=1, row=3, padx=10, pady=10)

        def on_select(event=None):
            # Get the selected items from the listbox and format them as a comma-separated string
            selected_items = ', '.join([listbox.get(i) for i in listbox.curselection()])
            print("Selected items:", selected_items)

        # Bind the on_select function to the ListboxSelect event
        listbox.bind("<<ListboxSelect>>", on_select)

        # Populate the listbox with data from the seria list
        for item in seria:
            listbox.insert(tk.END, item)

        def save_choose_data_button():
            # Get the selected items from the listbox
            selected_who_dave = [listbox.get(i) for i in listbox.curselection()]
            self.selected_who_gave = selected_who_dave

            if not selected_who_dave:
                # If no items are selected, show an error message and return
                messagebox.showerror("Error", "Please select at least one item.")
                return

            # Do something with the selected items here, for example, save them to a file
            print("Selected items:", selected_who_dave)

        # Create the "Generate choose data" button and bind it to the save_choose_data_button function
        button = ttk.Button(self, text='Generate choose data', command=save_choose_data_button)
        button.grid(column=1, row=4, columnspan=1)

    def date_of_birth_field(self):
        label = ttk.Label(self, text="Date of Birth:")
        label.grid(column=0, row=5, padx=10, pady=10)

        dob_entry = ttk.Entry(self, state='ACTIVE')
        dob_entry.insert(0, string=date_of_birth[0])
        dob_entry.grid(column=1, row=5, padx=10, pady=10)

    def passport_series_number_fields(self):
        label_series = ttk.Label(self, text="Passport Series:")
        label_series.grid(column=0, row=6, padx=5, pady=5)

        entry_series = tk.Listbox(self, selectmode=tk.MULTIPLE)
        entry_series.grid(column=1, row=6, padx=5, pady=5)

        # Populate the listbox with data from the seria list
        for item in num_list:
            entry_series.insert(tk.END, item)

        def on_select_seria(event=None):
            # Get the selected items from the listbox and format them as a comma-separated string
            selected_items = ', '.join([entry_series.get(i) for i in entry_series.curselection()])
            print("Selected items:", selected_items)

        # Bind the on_select function to the ListboxSelect event
        entry_series.bind("<<ListboxSelect>>", on_select_seria)

        def save_choose_seria_button():
            # Get the selected items from the listbox
            selected_seria = [entry_series.get(i) for i in entry_series.curselection()]
            self.selected_seria = selected_seria
            if not selected_seria:
                # If no items are selected, show an error message and return
                messagebox.showerror("Error", "Please select at least one item.")
                return

            # Do something with the selected items here, for example, save them to a file
            print("Selected items:", selected_seria)

        # Create the "Generate choose data" button and bind it to the save_choose_data_button function
        button = ttk.Button(self, text='Generate choose data', command=save_choose_seria_button)
        button.grid(column=1, row=7, columnspan=1)

    def passport_number_fields(self):
        label_number = ttk.Label(self, text="Passport Number:")
        label_number.grid(column=0, row=8, padx=10, pady=10)

        entry_number = ttk.Combobox(self, values=num_list, state="normal")
        entry_number.grid(column=1, row=8, padx=10, pady=10)

    def show_image(self):
        # Load the image using PIL library
        image = Image.open(path)
        # Resize the image to fit the canvas
        image = image.resize((400, 600), Image.ANTIALIAS)
        # Convert the PIL image to tkinter-compatible format
        photo = ImageTk.PhotoImage(image)
        # Add the image to the canvas
        self.canvas.create_image(0, 0, image=photo, anchor='nw')
        # Make sure the image is not garbage collected
        self.canvas.image = photo

    def generate_word_file_button(self):
        button = ttk.Button(self, text='Generate Word File', command=self.generate_word_file)
        button.grid(column=1, row=9, columnspan=2)

    def generate_word_file(self):
        # Read the template file
        template = DocxTemplate('template.docx')

        # Replace the placeholders with the chosen data
        context = {
            'first_name': self.name_fields[0].get(),
            'middle_name': self.name_fields[1].get(),
            'last_name': self.name_fields[2].get(),
            'who_gave_passport': ', '.join(self.selected_who_gave),
            'date_of_birth': self.date_of_birth_field.get(),
            'passport_series': ', '.join(self.selected_seria),
            'passport_number': self.passport_number_fields.get()
        }

        # Render the template with the context
        template.render(context)

        # Save the Word file
        template.save('output.docx')

        # Show a message box to inform the user that the file has been generated
        messagebox.showinfo("File Generated", "The Word file has been generated successfully.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
