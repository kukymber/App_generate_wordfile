'''To create a Python application that scrapes information from a document picture and
fills it into a DOCX template using the docx-template, Tkinter, passport-eye, and OCR (Optical Character Recognition)
libraries such as pytesseract, follow these steps:

    Install the required libraries:

bash

pip install docxtpl pytesseract opencv-python passporteye tkinter Pillow python-docx

    Prepare the DOCX template (e.g., template.docx) with placeholders for the data you want to fill in (e.g., {{name}},
{{passport_number}}, etc.).

    Create the Python script:

pytho'''

import cv2
import tkinter as tk
from tkinter import filedialog
from passporteye import read_mrz
from docxtpl import DocxTemplate
from PIL import Image, ImageTk
import pytesseract

# Set the path to the tesseract executable
# pytesseract.pytesseract.tesseract_cmd = "/home/anatolii/python_project/pythonProject9/venv/lib/python3.10/site" \
#                                         "-packages/pytesseract/pytesseract.py"
# tessdata_dir_config = r'--tessdata-dir "/home/anatolii/Downloads/rus.traineddata"'
# img_src = cv2.imread('/home/anatolii/python_project/pythonProject9/passport.png',0)
# print(img_src)


def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = cv2.imread(file_path)
        process_image(image, file_path)


def process_image(image, file_path):
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

    # Filter list with data
    num_list = [int(num) for num in filter(
        lambda num: num.isnumeric(), numbers_list)]

    words_list = [word for word in filter(
        lambda word: word.isalpha(), word_list)]
    # Input result
    print(num_list)
    print(words_list)
    print(data)
    fill_template(num_list, words_list)


def fill_template(data, num_list, word_list):
    template = DocxTemplate("template.docx")
    context = {
        'name': data['names'],
        'surname': data['surname'],
        'passport_number': data['number'],
        'country': data['country'],
        'nationality': data['nationality'],
        'date_of_birth': data['date_of_birth'],
        'expiration_date': data['expiration_date'],
        'sex': data['sex']
    }
    template.render(context)
    template.save("output.docx")


def main():
    root = tk.Tk()
    root.title("Passport Information Scraper")

    open_button = tk.Button(root, text="Open Image", command=open_image)
    open_button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()

""" ("\" Update the path-to-tesseract-executable with the actual path of the Tesseract executable \n"
 "   (e.g., C:/Program Files/Tesseract-OCR/tesseract.exe on Windows).\n"
 "\n"
 "    Run the script, and a simple Tkinter window with an \"Open Image\" button will appear. \n"
 "    Click the button to open an image of a passport, and the script will scrape the information \n"
 "    and fill it into the specified DOCX template. The output will be saved as output.docx in the same directory as the script.\n"
 "\n"
 "ostapenkodi@gmail.com\n"
 "continue\n"
 "\n"
 "As your application is already set up to scrape information from a document picture and fill it \n"
 "into a DOCX template using the docx-template, Tkinter, passport-eye, and pytesseract libraries, \n"
 "let's now improve the user interface by adding a label to display the status and a button to save the generated DOCX file.\n"
 "\n"
 "    Modify the main function to include new UI elements:\n"
 "\n"
 "python") """


def main():
    global status_label
    global save_button

    root = tk.Tk()
    root.title("Passport Information Scraper")

    open_button = tk.Button(root, text="Open Image", command=open_image)
    open_button.pack()

    status_label = tk.Label(root, text="Status: Awaiting image", wraplength=300)
    status_label.pack()

    save_button = tk.Button(root, text="Save DOCX", state=tk.DISABLED, command=save_docx)
    save_button.pack()

    root.mainloop()


""" Add a new global variable and a function to save the output DOCX file: python"""

output_file = None


def save_docx():
    if output_file:
        save_path = filedialog.asksaveasfilename(defaultextension=".docx")
        if save_path:
            output_file.save(save_path)
            status_label.config(text="Status: DOCX file saved")

    """Update the fill_template function to use the global output_file variable and update the UI elements:

python"""


def fill_template(data):
    global output_file

    template = DocxTemplate("template.docx")
    context = {
        'name': data['names'],
        'surname': data['surname'],
        'passport_number': data['number'],
        'country': data['country'],
        'nationality': data['nationality'],
        'date_of_birth': data['date_of_birth'],
        'expiration_date': data['expiration_date'],
        'sex': data['sex']
    }
    template.render(context)
    output_file = template

    status_label.config(text="Status: Template filled, ready to save")
    save_button.config(state=tk.NORMAL)

    '''Now, the application has a label to display the current status and a button to save the generated DOCX file.'''
    'The "Save DOCX" button will be enabled after the template is filled with the scraped information. '
    ''' The user can then click it to save the output file to their desired location.'''
