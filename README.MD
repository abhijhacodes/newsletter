## Newsletter backend

This repository contains code for backend of newsletter project in FastAPI

### Steps to setup and run locally 👇

#### Create python virtual environment

```bash
python -m venv fastapi-env
```

#### Activate virutal environment (Windows)

##### Powershell:

```bash
.\fastapi-env\Scripts\Activate.ps1
```

##### Command prompt:

```bash
fastapi-env\Scripts\activate.bat
```

#### Install all required dependencies

```bash
pip install -r requirements.txt
```

#### Create database

Create `sqlite.db` file in root of your project if you want to use sqlite database <br/>
or update `SQLALCHEMY_DATABASE_URL` in `db/database.py` file to use any other local or remote sql database

#### Run server locally

```bash
uvicorn main:app --reload
```

--reload flag enables live reload as you save files <br/>
This will run your server on http://localhost:8000 <br/>
You can change port by running this command 👇

```bash
uvicorn main:app --port PORT_NUMBER
```
