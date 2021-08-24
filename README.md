# Full Stack Nano Degree Final Project
## Full Stack Capstone

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer
within the company and are creating a system to simplify and streamline your process. 

That's where you come in! Help them finish the capstone app so they can start holding capstone and seeing who's the most knowledgeable of the bunch. The 
application must:

1. Get actors.
2. Get movies.
3. Post actors.
4. Post movies.
5. Delete actors.
6. Delete movies.
7. Patch actors.
8. Patch movies.

Completing this capstone app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to
communicate with others.

## About the stack

We started the full stack application for you. It is designed with some key functional areas:

# Backend
1. *./Capstone/`app.py`*
2. *./Capstone/`app_test.py`*

### Pre-requisites
* Developers using this project should already have Python3, pip and node installed on their local machines.
#### Install requirements
To install all reuirements, navigate to the `/Capstone` folder and run the folllowing command:
```bash
    pip install -r requirements.txt
```
requirements.txt is a file which includes all required modules and packages for API

Then to run application run the following commands:
```bash
    export FLASK_APP=app.py
    export FLASK_ENV=development
    flask run
```

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:actor`
   - `get:movie`
   - `delete:actor`
   - `delete:movie`
   - `post:actor`
   - `post:movie`
   - `patch:actor`
   - `patch:movie`
6. Create new roles for:
   - Assistant
     - can `get:actor`
     - can `get:movie`
   - Director
     - can all permission a Assistant and ...
     - can `delete:actor`
     - can `post:actor`
     - can `patch:actor`
     - can `patch:movie`
   - Producer
     - can all permission a Director and ...
     - can `delete:movie`
     - can `post:movie` 
7. Test your endpoints and RBAC test: 
   - Now enter the following line in your terminal: 
   ```bash
       python3 app_test.py
   ```
 API Reference

## Getting Started
* Base URL: At present this app can be run locally and it hosted by default. Default local url: ` http://127.0.0.1:5000 `
* Authentication: This version of API does not require :D

## Error Handling
Errors are returned as JSON objects in folloving format:
```json
    {
        "error": <error_code>,
        "message": <error_message>,
        "success": false
    }
```

### The API will return three types of errors: <br>
* 400: Bad request 
* 404: Resource not found 
* 405: Method now allowed 

## Endpoints

## `GET /actors`
    ```
        {
          "actors": [
            {
              "age": 45,
              "gender": "M",
              "id": 1,
              "name": "Leonardo De Kaprio"
            }
          ],
          "success": true,
          "total_actors": 1
        }
    ```
    
## `GET /movies`
    ```
        {
          "movies": [
            {
              "id": 1,
              "release_date": "January 19",
              "title": "Titanik"
            }
          ],
          "success": true,
          "total_movies": 1
        }
    ```
    
* ### ⚠️ Warning
    * If  in your request give a actors page which does not exists in database, API returns error with message "actors not found"
    * Example:
        * Request: ` http://127.0.0.1:5000/actors?page=12515 `
        * Response:
        ```
            {
                "message": "actors not found",
                "success": false
            }
        ```
        
## `POST /actors`
    * JSON data should include:
    ```
        "age" - new age
        "gender" - new gender
        "name" - new name
    ```
    * Then API reutrns data which includes:
    ```
        "added" - id of new actor,
        "success" - true,
        "total_actors" - number of all actors
    ```

## `POST /movies`
    * JSON data should include:
    ```
        "release_date" - new release date
        "title" - new title
    ```
    * Then API reutrns data which includes:
    ```
        "added" - id of new movies,
        "success" - true,
        "total_movies" - number of all movies
    ```
    
# Heroku Link: 
### https://abdulloh-fsnd-capstone.herokuapp.com/
