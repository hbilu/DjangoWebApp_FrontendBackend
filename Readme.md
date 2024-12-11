# Hacer Bilu Guresci SnT Assignment

## Overview
This project is a Dockerized Django web application (Frontend and Backend) using Python, REST API, a MySQL database, JavaScript, HTML and CSS. 

---

## Project Structure
```
DjangoWebApp_FrontendBackend/
├── assignment_project/       # Django project folder
│   ├── manage.py             # Django entry point
│   ├── assignment_project/   # Inner project folder (settings, wsgi, etc.)
│   │   ├── settings.py
│   │   ├── urls.py
│   ├── films                 # Films app for ./charts page
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── templates
│   │   │   ├── films
│   │   │   │   ├── dashboard.html
│   ├── users                 # Users app for ./user page
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── templates
│   │   │   ├── users
│   │   │   │   ├── user_list.html
│   ├── staticfiles           # Necessary static files including files enabling drag-and-drop functionality           
│   ├── templates
│   │   ├── main_page.html    # HTML page for main page which directs ./user and ./charts page via buttons
├── Dockerfile                # Docker image for the web service
├── docker-compose.yml        # Orchestration of web and database containers
├── .env                      # Environment variables
├── sql_files/                
│   ├── schema.sql            # Database schema
│   ├── data.sql              # Initial data
│   ├── requirements.txt      # Requirements for python virtual environment
```

---

## Build and Run Process

### Step 1: Build Docker Images
```bash
docker-compose build
```
### Step 2: Start Containers
```bash
docker-compose up
```
### Step 3: Verify Services
- Web service: [http://localhost:8000](http://localhost:8000)
- Main Page is accessible at http://localhost:8000
- ./user page is accessible at http://localhost:8000/users/user/
- ./charts page is accessible at http://localhost:8000/films/charts/

### Step 4: Stop Containers
```bash
docker-compose down
```

---

## Notes
- This setup uses `mysql.connector.django` as the database backend (`settings.py`). It is also added to the `requirements.txt`
- The `time.sleep(20)` wait in `manage.py` ensures Django waits for the database to initialize web service.
- Charts are enlarged when clicked on each of them and detailed data are shown when mouse is over the related part.