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
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" /> <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" /> 
<img src="https://img.shields.io/badge/Elastic_Search-005571?style=for-the-badge&logo=elasticsearch&logoColor=white"/>
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=darkgreen"/>
<img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/>
<img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white"/>
<br>
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
<br>
Snapshots of outputs are provided in the output folder.
Report and other DBMS works are included in the report folder.
