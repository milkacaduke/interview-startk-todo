This is (supposed to be) a full stack todo list.
Disclamer: Work in progress. Incomplete. Didn't get far.

Backend:
FastAPI - beanie (ODM) - Mongodb (using motor)

Frontend:
T.B.D


Launch Instructions:
  Mongodb setup - 
    Using mongodb/community-server

    Official instructions can be found here
    https://www.mongodb.com/docs/manual/tutorial/install-mongodb-community-with-docker/

    1. Pull mongodb docker image
    docker pull mongodb/mongodb-community-server

    2. Run image as container for local dev
    docker run -d --name mongodb -p 27017:27017 mongodb/mongodb-community-server:latest

FastAPI setup - 
  using python 3.12

  Use pip or pipenv to complete package installation.
  Do following:
    1. Install packages 
    pipenv install -r requirements.txt
    
    2. Activate virtual enviroment
    pipenv shell
    (then exit shell)
    
    3. If using vscode, you might need to set python interpretor to the venv. depends on how your python is setup in your local machine.

    4. Create .env at project root myapp/.env and populate with your secret values. see example.env for fields.

    5. Launch uvicorn server
    uvicorn myapp.main:app --reload --port=8080 --host=0.0.0.0


Usage - 
  Server lives at http://localhost:8080/

  Visit http://localhost:8080/docs for interactive api documentation
  
  
    
  
