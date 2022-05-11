# cs360-store
This is the git repository for our CS360 semester project at the University of Idaho.

### DB Structure
Check out the models.py file or the ER Diagram for our DB structure.

### Site Structure & URLS
Check out the urls.py file for the site structure/paths.

## Setup Process
Prereqs: python3, django

1. Clone/Download this repo.
2. Navigate to the folder that contains manage.py
3. You'll need to install Django if you don't have it, we did this in a virtual environment with miniconda: 'conda install django -c conda-forge'
4. Run the following command to start the server:
```bash
	python manage.py runserver
```
5. Navigate to http://127.0.0.1:8000/ or http://127.0.0.1:8000/admin/

Customer Login: 'SampleCustomer' Password: 'scustomer123'

Vendor Login: 'SampleVendor' Password: 'svendor123'

Note: we didn't make a way to create accounts, so these are the only ones available.
