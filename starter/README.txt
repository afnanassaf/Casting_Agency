# Casting Agency API Backend

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. 

This project had been devloped to fulfill graduation requirement of Full Stack Nano Dgree by Udacity

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < castingagency.psql
```

## Running the server

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## Roles & Users
- Casting Assistant
    - Can view actors and movies
    Email: assistant@castingagency.com
    Pwd: 123-castingagency
- Casting Director
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies
    Email: director@castingagency.com
    Pwd: 123-castingagency
- Executive Producer
    - All permissions a Casting Director has and…
    - Add or delete a movie from the database
    Email: producer@castingagency.com
    Pwd: 123-castingagency

## Authorization

Auth0 has been used as an authentecation provider

To login: https://asting-agency-fsnd.au.auth0.com/authorize?audience=casting&response_type=token&client_id=aQ0EHXOmFYAyRV21VoYLrqjX9VKfC1xb&redirect_uri=https://fsnd-casting-agency-a.herokuapp.com/home

## Live App

Casting Agency API is running and hosted by Heroku at: https://fsnd-casting-agency-a.herokuapp.com


## API 

GET '/home'
GET '/actors'
GET '/movies'
POST '/actors'
POST '/movies'
PATCH '/actors/<int:actor_id>'
PATCH '/movies/<int:movie_id>'
DELETE '/actors/<int:actor_id>'
DELETE '/movies/<int:movie_id>'


GET '/home'
- A welcome message to Casting Agency
- Request Arguments: None
- Returns: Wlcoming message 
{
    "message": "Welcome To Casting Agency"
}


GET '/actors'
- Fetches a list of actoes.
- Request Arguments: None
- Returns: actors objects with totalActors which the the count of actors in DB. 
{
    "actors": [
        {
            "age": 44,
            "gender": "Female",
            "id": 1,
            "name": "Kate Winslet"
        }],
    "totalActors": 1
}


GET '/POST '/movies'
- Fetches a list of movies.
- Request Arguments: None
- Returns: movies objects with totalMovies which the the count of movies in DB. 
{
    "movies": [
        {
            "id": 1,
            "release_date": "31-10-2017",
            "title": "Crooked House"
        },
    "totalMovies": 3
}


POST '/actors'
- Create a new actor.
- Request Body: 
{
     "age": 35,
     "gender": "Female",
     "name": "Keira Knightley"
 }

- Returns: Success status of the request and list of all actors along whith thier count.
           {
    "actors": [
        {
            "age": 44,
            "gender": "Female",
            "id": 1,
            "name": "Kate Winslet"
        },
        {
            "age": 35,
            "gender": "Female",
            "id": 2,
            "name": "Keira Knightley"
        }
    ],
    "success": true,
    "totalActors": 2
}


POST '/movies'
- Create a new movie.
- Request Body: 
{
    "title": "The Imitation Game",
    "release_date": "28-11-2014"
}

- Returns: Success status of the request and list of all movies along whith thier count.
{
    "movie": [
        {
            "id": 1,
            "release_date": "18-11-1997",
            "title": "Titanic"
        },
        {
            "id": 2,
            "release_date": "28-11-2014",
            "title": "The Imitation Game"
        }
    ],
    "success": true,
    "totalMovies": 2
}


PATCH '/actors/<int:actor_id>'
- Edit actor information based on the provided id.
- Request Arguments: actor_id, witch is the actor id
- Request Body: 
{
     "age": 45
 }

- Returns: Success status of the request and list of all actors along whith thier count.
           {
    "actors": [
        {
            "age": 45,
            "gender": "Female",
            "id": 1,
            "name": "Kate Winslet"
        },
        {
            "age": 35,
            "gender": "Female",
            "id": 2,
            "name": "Keira Knightley"
        }
    ],
    "success": true,
    "totalActors": 2
}


PATCH '/movies/<int:movie_id>'
- Edit movie information based on the provided id.
- Request Arguments: movie_id, witch is the movie id
- Request Body: 
{
    "release_date": "28-10-2014"
}

- Returns: Success status of the request and list of all movies along whith thier count.
{
    "movie": [
        {
            "id": 1,
            "release_date": "18-11-1997",
            "title": "Titanic"
        },
        {
            "id": 2,
            "release_date": "28-10-2014",
            "title": "The Imitation Game"
        }
    ],
    "success": true,
    "totalMovies": 2
}



DELETE '/actors/<int:actor_id>'
- Delete a actor based on the provided id.
- Request Arguments: actor_id, witch is the actors id
- Returns: Success status of the request and list of all actors along whith thier count.
{
    "actors": [
        {
            "age": 45,
            "gender": "Female",
            "id": 1,
            "name": "Kate Winslet"
        }
    ],
    "success": true,
    "totalActors": 1
}


DELETE '/movies/<int:movie_id>'
- Delete a movie based on the provided id.
- Request Arguments: movie_id, witch is the movie id
- Returns: Success status of the request and list of all movies along whith thier count.
{
    "movie": [
        {
            "id": 1,
            "release_date": "18-11-1997",
            "title": "Titanic"
        }
    ],
    "success": true,
    "totalMovies": 1
}

```


## Testing
To run the tests, run
```
dropdb casting_agency_test
createdb casting_agency_test
psql trivia < castingagency.psql
python test_app.py
```