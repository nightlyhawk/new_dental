# Bright_Smile_Management_Systems
## Overview
This project provides an interface for the staff of Bright Smile yo manage their medical services, staff and clients.  
### BaseUrl
- localhost
### Setup Procedure (in terminal)
- clone project to folder > cd to folder through terminal and run:
- pip install -r requirements.txt
- python manage.py makemigrations
- python manage.py migrate
- python manage.py collectstatic
- python manage.py runserver
### Endpoints Available
#### - /patients/add/<br />
      method: GET, POST
      body: {name:'', d_o_b:'', address:'', gender:'', ssn_last_4:'', phone_number:''}
      response: {}
      description: add patient record 
#### - /doctors/add/<br />
      method: GET, POST
      body: {npi:'', name:'', email:'', phone_number:'', office_address:'', specialties:''}
      response: {}
      description: add doctor record 
#### - /clinics/add/<br />
      method: GET, POST
      body: {name:'', phone_number:'', city:'', state:''}
      response: {}
      description: register clinic
#### - /clinics/view/<br />
      method: GET
      body: none 
      response: {}
      description: view registered clinics 
  
