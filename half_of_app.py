import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, Canvas, messagebox
from tkinter import filedialog

import cv2
import pytesseract
import re
from PIL import Image, ImageTk
from docxtpl import DocxTemplate

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.dob_entry = None
        self.name_combos = None
        self.entry_number = None
        self.passport_number = None
        self.title("Tkinter App")
        self.geometry("900x800")

        # Open the image and extract data
        self.open_image()

        # Creating the date of birth field
        self.date_of_birth_field()

        # Creating list-based fields for names
        self.name_fields()

        # Creating the "Who Gave Passport" field with multiple selections
        self.who_gave_passport_field()
        # self.selected_who_gave = ["", "", ""]

        # Creating the fields for passport series and number
        self.passport_series_number_fields()
        # self.selected_seria = []
        self.passport_number_fields()

        # Adding the canvas for the image
        self.canvas = tk.Canvas(self, width=400, height=600)
        self.canvas.grid(column=2, row=0, rowspan=7, padx=10, pady=10)

        # Loading and displaying the image
        self.show_image()

        # Adding the button for selecting the template file
        self.selected_template_path = tk.StringVar()
        self.select_template_button = ttk.Button(self, text="Select Template", command=self.select_template_file)
        self.select_template_button.grid(column=0, row=9, padx=10, pady=10)
        self.selected_template_label = ttk.Label(self, textvariable=self.selected_template_path)
        self.selected_template_label.grid(column=1, row=9, padx=10, pady=10)

        self.generate_word_file_button()

        # Adding the button for opening the generated Word file
        self.style = ttk.Style()
        self.style.configure("Large.TButton", font=("TkDefaultFont", 12))
        self.open_word_file_button = ttk.Button(self, text="Open Generated Word File", style="Large.TButton",
                                                command=self.open_word_file)
        self.open_word_file_button.grid(column=1, row=10, padx=10, pady=10)

    def open_word_file(self):
        # Get the path to the generated Word file
        file_path = "output.docx" # Change this to the actual path of your generated Word file
        if os.path.exists(file_path):
            # Open the file in an installed Word viewer
            if sys.platform == "win32":
                # On Windows, use the start command to open the file in Word
                subprocess.Popen(['start', '', file_path], shell=True)
            elif sys.platform == "darwin":
                # On macOS, use the open command to open the file in Word
                subprocess.Popen(['open', '-a', 'Microsoft Word', file_path])
            else:
                # On other platforms, use the xdg-open command to open the file in the default viewer
                subprocess.Popen(['xdg-open', file_path])
        else:
            messagebox.showerror("Error", "The generated Word file does not exist.")

    def select_template_file(self):
        # Show file dialog to choose a Docx file
        file_path = filedialog.askopenfilename(filetypes=[("Word Document", "*.docx"), ("All Files", "*.*")])
        if file_path:
            self.selected_template_path.set(os.path.basename(file_path))

    def open_image(self):
        # Show file dialog to choose image
        file_path = filedialog.askopenfilename()
        if file_path:
            # Reading an image in default mode
            img = cv2.imread(file_path)

            # Rotate image for scan numbers
            img2 = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

            # Read image and translate in text and numbers
            text = pytesseract.image_to_string(img, lang="rus")
            numbers = pytesseract.image_to_string(img2, lang="rus")

            # Create lists with data
            word_list = text.split()
            numbers_list = numbers.split()

            seria = [elem for elem in word_list if any(char.isalpha() for char in elem)]

            def filter_objects(lst):
                result = []
                # iterate over each element in the list
                for element in lst:
                    # remove non-letter characters from the element
                    element = ''.join(filter(str.isalpha, element))
                    # check if the filtered element starts with a letter and ends with a letter
                    if element and element[0].isalpha() and element[-1].isalpha():
                        # check if the length of the element is greater than 1
                        if len(element) > 2:
                            # if it is, append it to the result list (if it's not already there)
                            if element not in result:
                                result.append(element)
                # sort the result list in alphabetical order and then reverse the order
                result = sorted(result, key=str.lower, reverse=True)
                return result

            # Filter list with data
            num_list = [num for num in filter(
                lambda num: num.isnumeric(), numbers_list)]

            words_list = filter_objects(word_list)


            # take date of birth from text (default image)
            date_of_birth = re.findall("\d{2}[./,]?\d{2}[./,]?\d{4}", text)

            # Assign extracted data to class variables
            self.image_path = file_path
            self.text = text
            self.numbers = numbers
            self.seria = seria
            self.num_list = num_list
            self.words_list = words_list
            self.date_of_birth = date_of_birth

    def name_fields(self):
        self.name_combos = []
        for i in range(3):
            label = ttk.Label(self, text=f"{['First', 'Middle', 'Last'][i]} Name:")
            label.grid(column=0, row=i, padx=10, pady=10)

            combo = ttk.Combobox(self, values=self.words_list[::-1], state="normal")
            combo.grid(column=1, row=i, padx=10, pady=10)
            self.name_combos.append(combo)

            # Bind the on_select_name function to the ComboboxSelected event of the combobox
            combo.bind("<<ComboboxSelected>>", lambda event, index=i: self.on_select_name(event, index))

    def on_select_name(self, event, index):
        pass

    def who_gave_passport_field(self):
        label = ttk.Label(self, text="Who Gave Passport:")
        label.grid(column=0, row=3, padx=10, pady=10)

        listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        listbox.grid(column=1, row=3, padx=10, pady=10)

        def on_select(event=None):
            pass

        # Bind the on_select function to the ListboxSelect event
        listbox.bind("<<ListboxSelect>>", on_select)

        # Populate the listbox with data from the seria list
        for item in self.seria:
            listbox.insert(tk.END, item)

        def save_choose_data_button():
            # Get the selected items from the listbox
            selected_who_dave = [listbox.get(i) for i in listbox.curselection()]
            self.selected_who_gave = selected_who_dave

            if not selected_who_dave:
                # If no items are selected, show an error message and return
                messagebox.showerror("Error", "Please select at least one item.")
                return


        # Create the "Generate choose data" button and bind it to the save_choose_data_button function
        button = ttk.Button(self, text='Choose data', command=save_choose_data_button)
        button.grid(column=1, row=4, columnspan=1)

    def date_of_birth_field(self):
        label = ttk.Label(self, text="Date of Birth:")
        label.grid(column=0, row=5, padx=10, pady=10)

        self.dob_entry = ttk.Entry(self, state='ACTIVE')
        self.dob_entry.insert(0, string=self.date_of_birth[0])
        self.dob_entry.grid(column=1, row=5, padx=10, pady=10)

    def passport_series_number_fields(self):
        label_series = ttk.Label(self, text="Passport Series:")
        label_series.grid(column=0, row=6, padx=5, pady=5)

        entry_series = tk.Listbox(self, selectmode=tk.MULTIPLE)
        entry_series.grid(column=1, row=6, padx=5, pady=5)

        # Populate the listbox with data from the seria list
        for item in self.num_list:
            entry_series.insert(tk.END, item)

        def on_select_seria(event=None):
            pass

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

        # Create the "Generate choose data" button and bind it to the save_choose_data_button function
        button = ttk.Button(self, text='Choose data', command=save_choose_seria_button)
        button.grid(column=1, row=7, columnspan=1)

    def passport_number_fields(self):
        label_number = ttk.Label(self, text="Passport Number:")
        label_number.grid(column=0, row=8, padx=10, pady=10)

        self.entry_number = ttk.Combobox(self, values=self.num_list, state="normal")
        self.entry_number.grid(column=1, row=8, padx=10, pady=10)

    def show_image(self):
        # Load the image using PIL library
        image = Image.open(self.image_path)
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
        selected_items = [combo.get() for combo in self.name_combos]
        # Read the template file
        template = DocxTemplate('/home/anatolii/python_project/pythonProject9/template.docx')

        # Replace the placeholders with the chosen data
        context = {
            'first_name': selected_items[0],
            'middle_name': selected_items[1],
            'last_name': selected_items[2],
            'who_gave_passport': ' '.join(self.selected_who_gave),
            'date_of_birth': self.dob_entry.get(),
            'passport_series': ' '.join(self.selected_seria),
            'passport_number': self.entry_number.get()
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
