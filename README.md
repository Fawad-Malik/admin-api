# Simple Admind API With Fastapi and SQLAlchemy (Python 3)

Tutorial for building Create, Read, Update and Delete using REST Full API with FastAPI and SQLAlchemy

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Make sure you have installed Python 3 on your device

### Project structure
```
* admin-api/
  |--- app/
  |    |--- __init__.py
  |    |--- blueprints.py
  |    |--- manage.py
  |    |--- models.py
  |    |--- schemas.py
  |    |--- settings.py
  |--- .env
  |--- .gitignore
  |--- .requirements.txt
```

### Step to create flask rest api

A step by step series of examples that tell you how to get a development env running

1. Install virtual environment
```
pip install virtualenv
```
2. Create virtual environment and activate inside your admin-api directory according the above structure
```
virtualenv venv
> On windows -> venv\Scripts\activate
> On linux -> . source venv/bin/activate
```
3. Change directory into admin-api folder.
```
cd admin-api
```
4. Install some librares on your virtual environment with pip
```
pip install -r requirements.txt
```
5. Create .env file and set environment variables for database. i.e.
```
DB_URL = localhost
DB_USER = root
DB_PW = 1234
DB_PORT = 3306
DB_NAME = admin
```
5. Run the local server with this command
```
uvicorn app.manage:app --reload
```
6. If successful then hit this endpoint /api/healthchecker(GET) to verify
```
{"message": "Welcome to Admin dashboard"}
```

## Clone or Download

You can clone or download this project
```
> Clone : https://github.com/Fawad-Malik/admin-api.git
```

## Authors

* **Fawad Azher** - *