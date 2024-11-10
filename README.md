# Bright_Smile_Management_Systems
## Overview
This project provides an interface for the staff of Bright Smile yo manage their medical services, staff and clients.  
### BaseUrl
- localhost
### Setup Procedure 
- pip install -r requirements.txt
- python manage.py makemigrations
- python manage.py migrate
- python manage.py collectstatic
- python manage.py runserver
### Endpoints Available
#### - /patients/add/<br />
      method: GET, POST
      body: {}
      response: {message: success, status=200}
      description: add patient record 
#### - /doctors/add/<br />
      method: GET, POST
      body: {name: "", graph_id: "", size: "", file: ""}
      response: {message: success, status=200}
      description: add doctor record 
#### - /clinics/add/<br />
      method: GET, POST
      body: {ttl_file: ""}
      response: {message: success, status=200}
      description: register clinic
#### - /clinics/view/<br />
      method: GET
      body: none 
      response: {clinics: [], status=200}
      description: view registered clinics 
  
