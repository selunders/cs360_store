# cs360-store
This is the git repository for our CS360 semester project at UIdaho.

## Site Structure
cs360-store/
    db.sqlite3
    manage.py
    cs360-store/
    storeApp/

## URLs
store/ — Home page, shows user's past views and purchases
store/vendors/<unique_name> — show all the products/services related to the vendor
store/vendors/<name>/products/<product_id> — Show detailed information for a specific product 
store/vendors/<name>/services/<service_id> — Show detailed information for a specific service

## Setup Process
Prereqs: python3, django

1. Clone/Download this repo.
2. Navigate to the cs360-store/cs360store/ folder
3. Run the following command to start the server:

```bash
	python manage.py runserver
```

4. Navigate to http://127.0.0.1:8000/store/ or http://127.0.0.1:8000/admin/
