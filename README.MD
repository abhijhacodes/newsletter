## Newsletter backend

This repository contains code for backend of newsletter project in FastAPI

#### See the code for client side [here](https://github.com/abhijhacodes/newsletter-client)

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

### Steps to deploy to production

You can use any approach to deploy your FastAPI application and Postgresql database to production either using Docker containers or using any cloud server provider. <br/>
I'm using [render.com](https://render.com) to deploy server as well as DB.

- On render, create a new PostgreSQL instance, and copy the <b>external URL</b> from it after it is created.
- change postgres to postgresql in the url
- add the URL in POSTGRESQL_DATABASE_URL varible in your .env file
- Install these dependencies:
  ```bash
  pip install alembic psycopg2 psycopg2-binary
  ```
- Create alembic migration environment
  ```bash
  alembic init alembic
  ```
- Update sqlalchemy.url in <b>alembic.ini</b> file to your postgresql url
- In <b>alembic/env.py</b> file import your Base and all models from your database config files
- Update value of target_metadata to
  ```bash
  target_metadata = Base.metadata
  ```
- Do initial migration
  ```bash
  alembic revision --autogenerate
  ```
- You can now start using this database
- Add alembic.ini and alembic/versions in .gitignore
- Now you can directly connect your code repo on render.com and deploy the app in <b>new web service</b>
- Add all the environment variables of your app on render
- For each subsequent migration of your database you can run the same command
