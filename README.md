## Tkinter App

This is a python application that allows users to extract data from an image of a passport and generate a word file with the extracted data. the application uses the following libraries:

- Tkinter: For the user interface
- OpenCV: For image processing
- Pytesseract: For optical character recognition
- Pillow: For image manipulation
- docxtpl: For generating the Word file.

#### Installation

To use this application, you will need to have Python 3 installed on your system along with the following libraries:

	pip install tkinter opencv-python pytesseract Pillow docxtpl
	
Additionally, you will need to change the tesseract_cmd variable in the pytesseract library to point to the location of your tesseract executable. By default, the tesseract_cmd variable is set to /usr/bin/tesseract, which may not be correct for your system. To change the tesseract_cmd variable, open the app.py file and modify the following line:

	pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

Replace /usr/bin/tesseract with the path to your tesseract executable.

#### Usage

To use the application, run the following command:

	python app.py

This will open the user interface. Click the "Open Image" button to choose an image of a passport. The application will then extract the data from the image and display it in the appropriate fields.

The user can then select the appropriate data from the dropdown menus and listboxes provided. Once all the fields are filled in, click the "Generate Word File" button to generate a Word file with the extracted data.

