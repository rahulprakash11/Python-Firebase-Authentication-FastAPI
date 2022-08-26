# FastAPI-Firebase-Authentication
A user authentication system, implementing Google's Firebase_admin auth modeule inside python's FastAPI based backend.


![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=black)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=blue)
![Firebase](https://img.shields.io/badge/firebase-%23039BE5.svg?style=for-the-badge&logo=firebase)
![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=yellow)
<br>
![GitHub](https://img.shields.io/github/license/RahulPrakash11/Python-FastAPI-Firebase-Authentication)


<img src=assets\img\thul-876298A8-C3E1-487D-8AD6920174E16D78.png width="8%" height="8%"><img src="https://firebase.google.com/static/images/homepage/cloud-plus-firebase_1x.png" width="15%" height="15%"><img src=assets\img\thul-876298A8-C3E1-487D-8AD6920174E16D78.png width="8%" height="8%"> 

<br>

# Technologies used in the project:

- Google's firebase-admin:
  - to create/register dummy user, for token generation
  - to authenticate user, for access
- FastAPI:
  - implementing the backend logic to access database
- Poetry:
  - for dependency management of our python environment
- MongoDb:
  - an open source NoSql database storing our user information
- Google Cloud Platform:
  - for deployment on Cloud Run
</br>

# Index

- **[Installation Instructions](#installation-instructions)**<br>
   - **[Using Poetry](#using-poetry)**<br>
- **[Usage Instructions](#usage-instructions)**<br>
- **[Setup FastApi RESTapi](#setup-fastapi-restapi)**<br>
- **[Setup Firebase Auth](#setup-firebase-auth)**<br>
- **[Google Cloud Run Deployment](#google-cloud-run-deployment)**<br>
- **[Further Help](#further-help)**<br>
- **[License](#license)**<br>

<br>

# Installation Instructions #


We will be using [poetry](https://python-poetry.org/docs/) as our python package manager. you can follow the steps to get this project running on your system.
So we will start by setting up poetry on our local machine.
<br>

- First clone the repo to your local machine. In your git bash UI enter the commands:

```bash
> git clone <this-repo>
> cd this-project
> code .
```
### [Using Poetry](https://python-poetry.org/docs/)
- From the root directory we will install poetry if not already present in your system. Click [here](https://python-poetry.org/docs/#windows-powershell-install-instructions) for the windows install command.
- After poetry gets installed, setup your virtual invironment.

```ps
> poetry env use python<version>
> poetry env use 3.8
```

- Next to install dependencies run: 
```ps
> poetry install
```

Note : `Poetry takes care of installing these dependencies in your virtual environment. You don't have to activate your virtual environment manually every time.`

<br>


**Before we could the test the setup we need following to be ready with us :**


- **Mongodb Atlas**, to store user information to authenticate against. You can use [free service](https://www.mongodb.com/docs/atlas/tutorial/deploy-free-tier-cluster/) provided by MongoDb for this project.
- [**Firebase Admin**](https://firebase.google.com/docs/admin/setup#set-up-project-and-service-account) credentials to be able to generate tokens and verify against.
- create an empty **`.env`** file at the base directory of your project and update the [`.env.test`](.env.test) file.
  - provide [mongodb connection string](https://www.mongodb.com/docs/guides/atlas/connection-string/) to `MONGODB_URL`
  - create [firebase credentials.json](google_application_credentials.json) file in the root directory of the project or, otherwise, provide the absolute path to credentials file in .env to `GOOGLE_APPLICATION_CREDENTIALS`

We are all set to run our test.

<br>

# Usage Instructions #

Poetry provides for custom scripts to be run in cli. You can access/write these scripts in [pyproject.toml](pyproject.toml).

To run locally run these commands:

```ps
> poetry run test (to setup environment test)
> poetry run server (to serve uvicorn)
``` 
FastApi provides Swagger UI: served at /docs.
In your bowser go to :
> http://localhost:5000/docs

You can register a dummy user using email and password to authenticate further, via :
>http://localhost:5000/docs#/dummy/create_user_dummy_register_post

Next, login through above credentials to get token from firebase auth provider to authenticate, via :
>http://localhost:5000/docs#/dummy/login

Use the token obtained above to verify/register a user, via :
> http://localhost:5000/docs#/auth/verify

In response you get details of new player created in your database which can be acceesed/modified through token-based authentication only, via :
> http://localhost:5000/docs#/player/{id}


<br>

# <img src="https://fastapi.tiangolo.com/img/icon-white.svg" width="5%" height="5%">  Setup FastApi RESTapi  <img src="https://fastapi.tiangolo.com/img/icon-white.svg" width="5%" height="5%">

  To get more familier with Fastapi you can go through their [docs](https://fastapi.tiangolo.com/).
  
  Here, we will be using **[uvicorn](https://www.uvicorn.org/deployment/)** to serve our FastApi backend.

<br>

# <img src=assets\img\firebase-cloud.png width="5%" height="5%"> Setup Firebase Auth <img src=assets\img\firebase-cloud.png width="5%" height="5%">

One can use the Firebase Admin SDK to manage your users or to manage authentication tokens. As stated in their [**documentation**](https://firebase.google.com/docs/auth/admin), You can also use the service to identify these users on your own server. This lets you securely perform server-side logic on behalf of users that have signed in with Firebase Authentication.

To do this, you can retrieve an ID token from a client application signed in with Firebase Authentication and include the token in a request to your server. Your server then [**verifies the ID token**](python_fastapi_firebase_authentication\utils\dependencies.py) and extracts the claims that identify the user (including their uid, the identity provider they logged in with, etc.). This identity information can then be used by your server to carry out actions on behalf of the user.

<br>

# <img src=assets\img\google-cloud-run-icon.png width="5%" height="5%"> Google Cloud Run Deployment  <img src=assets\img\google-cloud-run-icon.png width="5%" height="5%">

For this project we have used Google's Cloud Run to deploy my Dockerised FastApi.
You can follow this link for more help:
- https://towardsdatascience.com/deploy-a-dockerized-fastapi-app-to-google-cloud-platform-24f72266c7ef

I will list the step-wise process involved in deployment:
- **Pre-requisites :**
  - A Billing Account on GCP/GOOGLE CLOUD PLATFORM(though this setup will cost $0)
- Create [**Dockerfile**](Dockerfile) to dockerise your fastapi code
- Create [**.dockerignore**](.dockerignore) and [**.gcloudignore**](.gcloudignore) files(to enumerate what you need to push and what not)
  - Note : Here we have also used .gitignore to whose restrictions .gcloudignore [automatically inherits](https://cloud.google.com/sdk/gcloud/reference/topic/gcloudignore). 
  - Make sure you have not ignored [.env](.env) and [google_application_credentials.json](google_application_credentials.json)
- Next follow the instruction in the link provided above.
- Also make sure [**gcloud cli**](https://cloud.google.com/sdk/docs/install) is installed and configured on your system.
- gcloud cli commands to be entered for deployment:

Replace PROJECT-ID with your GCP project ID
```ps

TO view your project ID by running the command 
> gcloud config get-value project

TO SET your project ID:
gcloud config set project PROJECT-ID
> gcloud config set project auth-test

TO BUILD:
gcloud builds submit --tag gcr.io/PROJECT-ID/container-name
> gcloud builds submit --tag gcr.io/auth-test/auth-api-container

TO DEPLOY:
gcloud run deploy --image gcr.io/PROJECT-ID/container-name --platform managed
> gcloud run deploy --image gcr.io/auth-test/auth-api-container --platform managed

TO DELETE:
gcloud deployment-manager deployments delete example-deployment --delete-policy=DELETE

```

<br>


# Further Help

This project is an open-source initiative by Junkie Labs team.

For any questions or suggestions send a mail to junkielabs.dev@gmail.com or chat with the core-team on gitter.


[![Gitter](https://badges.gitter.im/nubar-api/django-dynamodb-lambda-function.svg)](https://gitter.im/nubar-api/django-dynamodb-lambda-function?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

<br>

# License

[MIT License](https://github.com/RahulPrakash11/Python-FastAPI-Firebase-Authentication-Google-Cloud-Run-Deploy/blob/main/LICENSE).


<br>



