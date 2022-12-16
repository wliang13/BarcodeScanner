App Documentation
Morning Star: Automated Barcode Scanning of Containers in an Outdoor Warehouse

Team 314: Jerin Sajimon, Malik Khan, Warren Liang, Luis Palafox, Brayan Ortiz, Lucas Netto

Github Link: https://github.com/wliang13/BarcodeScanner


Installing Python:

Download and install  the latest version of python using the following link:
https://www.python.org/downloads/

Mark the “Add Python 3.10 to PATH” checkbox when installing to access python from the command prompt. 
	
It is recommended to select the “Disable path length limit” that shows up at the end of the installation to prevent debugging errors in the future


Installing and activating the virtual environment:
In-depth instruction:
https://linuxhint.com/activate-virtualenv-windows/

Install the virtual environment by opening the command prompt and type:
		>>pip install virtualenv

Create a new project directory and switch to it:
		>>mkdir barcode_scanner
		>>cd barcode_scanner

Download all the files from the GitHub page into the new project directory

Create the virtual environment and activate it:
		>>virtualenv venv
>>venv\Scripts\activate

Make sure that all of the next steps are done with the virtual environment activated


Installing Flask and setting up the SQLite database
In-depth instruction:
https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application

Install Flask and Flask-SQLAlchemy:
		>>pip install Flask Flask-SQLAlchemy

Creating the database and importing the database model:
		>>set FLASK_APP=app
		>>flask shell
		>>from app import db, Todo
		>>db.create_all()

Note:
If there is already a database created, then the old one has to be dropped before creating a new one. Do the following steps as well if there are modifications done to the database model.
		>>db.drop_all()
		>>db.create_all()
	
Exit the flask shell:
			>>quit()


Installing the needed libraries:

Pyzbar: Library used for decoding barcodes
	>>pip install pyzbar

Opencv: Library for manipulating images:
>>pip install opencv-python

Xlsxwriter: Library for importing data to excel file
>>pip install xlsxwriter


Running the application:

Tell Flask about the application and run it:
		>> set FLASK_APP=app
		>>flask run

Hold the Ctrl button and click the link that appears
	>>http://127.0.0.1:5000/
	
To exit the program, hold the Ctrl and C key on the keyboard while using the cmd prompt.





