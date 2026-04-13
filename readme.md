# Flask CRUD API (User Management)

This is a simple Flask-based backend project to understand how APIs are structured in real-world applications.

The project follows a clean architecture approach where responsibilities are divided into different layers such as routes, services, schemas, and models.

## What this project covers

* Creating REST APIs using Flask
* Using Blueprints for modular routing
* Input validation using Pydantic
* Separating business logic from routes
* Basic in-memory data storage

## Project Structure

* routes: Handles incoming requests
* services: Contains business logic
* schemas: Validates request data
* models: Stores data (temporary)

## API Implemented

### Create User

POST /user

Request Body:
{
"name": "John",
"age": 25
}

## Notes

This project is built for learning purposes. Database integration is not included yet, and data is stored in memory.

Further CRUD operations like Get, Update, and Delete will be added step by step.
