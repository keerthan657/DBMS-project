# DBMS-project
Project to automate traffic rule violation detection

This project is done as part of **LAB component of DBMS subject**
<br>

Project contributors:
<br>
:smiley:Jaikishan Jaikumar
<br>
:smile:Keerthan Kumar A
<br>
:wink:Mahendra Vishwakarma
<br>

## Tools and Components
Backend - Flask and Flask_SQLAlchemy
<br>
Frontend - Flask, HTML and CSS
<br>
OCR using pytesseract
<br>
Databases - postgreSQL(SQL) and Elasticsearch(NoSQL)
<br>

## Working
**camera.py** is the script responsible for backend work. Run it using 
> python camera.py
<br>
Enter either image path (PNG image specifically) which you want to recognize using OCR, or directly give vehicle number itself. Vehicle details are fetched and fines are calculated. It is also simultaneously updated in the database, and also being checked for missing status. If found as missing, a mail alert is sent (to email address specified in alert.py). Fine rates are fetched from NoSQL.
<br>
<br>

**main.py** is the script responsible for frontend work. Run it using
> python main.py
<br>
This runs the website on https://localhost:5000, and can then be used to access project functionalities.
