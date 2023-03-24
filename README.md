Tkinter App

This is a Python application that allows users to extract data from an image of a passport and generate a Word file with the extracted data. The application uses the Tkinter library for the user interface, OpenCV for image processing, Pytesseract for optical character recognition, and docxtpl for generating the Word file.
Installation

To use this application, you will need to have Python 3 installed on your system along with the following libraries:

    tkinter
    OpenCV
    Pytesseract
    Pillow
    docxtpl

You can install these libraries using pip by running the following command:

python

pip install tkinter opencv-python pytesseract Pillow docxtpl

Usage

To use the application, run the following command:

python

python app.py

This will open the user interface. Click the "Open Image" button to choose an image of a passport. The application will then extract the data from the image and display it in the appropriate fields.

The user can then select the appropriate data from the dropdown menus and listboxes provided. Once all the fields are filled in, click the "Generate Word File" button to generate a Word file with the extracted data.
