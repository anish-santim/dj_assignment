# BookStoreAPI

Django based BookStore API Application.

## Table of Contents

- [BookStoreAPIs](#project-title)
- [Table of Contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Migrations](#database-migrations)
- [Creating a Superuser](#creating-a-superuser)
- [Running the Server](#running-the-server)
- [Testing](#testing)
- [API Collection](#api-collection)


## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x
- Django 3.x or later
- pip (Python package installer)

## Installation

1. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

2. Activate the virtual environment:

    - On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Database Migrations

1. Make database migrations for any changes in the models:

      ```bash
    cd bookstore
    ```

    ```bash
    python manage.py makemigrations api
    ```

2. Apply the migrations to the database:

    ```bash
    python manage.py migrate
    ```

## Creating a Superuser

To create an admin (superuser) account for accessing the Django admin interface:

1. Run the following command :

    ```bash
    python manage.py createsuperuser
    ```
    - Follow the prompts to set the email and password
2. (add the role from admin panel : http://127.0.0.1:8000/admin/ ) and log in with creds:
    ```
    Users(Table) > select user > Role : Choose['Member' , 'Admin'] 
    ```

## Running the Server

1. Start the development server:

    ```bash
    python manage.py runserver
    ```

2. Open your web browser and go to `http://127.0.0.1:8000/` to see the project in action.

## Testing

To run the tests, use the following command:

```bash
python manage.py test
```
# API Collection

## Login
- **URL:** `http://127.0.0.1:8000/login/`
- **Method:** POST
- **Request Body:**
  ```json
  {
      "email": "admin@gmail.com",
      "password": "root"
  }
  ```

## Add Categories by Admin
- **URL:** `http://127.0.0.1:8000/manage_categories/`
- **Method:** POST
- **Request Body:**
  ```json
  {
      "name": "Fan Fiction"
  }
  ```

## Get All Categories by Admin
- **URL:** `http://127.0.0.1:8000/manage_categories/`
- **Method:** GET
- page, page_size (query params)
## Update Categories by Admin
- **URL:** `http://127.0.0.1:8000/manage_categories/`
- **Method:** PUT
- **Request Body:**
  ```json
  {
      "old_name": "Horizon",
      "new_name": "New Horizon"
  }
  ```

## Delete Category by Admin
- **URL:** `http://127.0.0.1:8000/manage_categories/`
- **Method:** DELETE
- **Request Body:**
  ```json
  {
      "name": "new"
  }
  ```

## Checkout by Member or Admin
- **URL:** `http://127.0.0.1:8000/checkout/`
- **Method:** PUT

## Add to Cart by Member or Admin
- **URL:** `http://127.0.0.1:8000/cart/add/<int:id of book>/`
- **Method:** POST

## View Books by Anyone
- **URL:** `http://127.0.0.1:8000/books/`
- **Method:** GET
- **Request Body:**
  ```json
  {
      "categories": []
  }
  ```
- - page, page_size (query params)

## Update Books by Admin
- **URL:** `http://127.0.0.1:8000/manage/books/`
- **Method:** PUT
- **Request Body:**
  ```json
  {
      "id": 2,
      "category": "Horror",
      "title": "EVIL Dead",
      "author_name": "samuel jackson",
      "price": 200.00,
      "stock": 3,
      "year_published": 2000
  }
  ```

## Get Books by Admin
- **URL:** `http://127.0.0.1:8000/manage_books/`
- **Method:** GET
- page, page_size (query params)

## Add Books by Admin
- **URL:** `http://127.0.0.1:8000/manage_books/`
- **Method:** POST
- **Request Body:**
  ```json
  {
      "category": "Horror",
      "title": "EVIL Dead",
      "author_name": "samuel jackson",
      "price": 200.00,
      "stock": 3,
      "year_published": 2000
  }
  ```

## Delete Books by Admin
- **URL:** `http://127.0.0.1:8000/manage_books/`
- **Method:** DELETE
- **Request Body:**
  ```json
  {
      "title": "Horizons"
  }
  ```

## View Cart by Admin or Member
- **URL:** `http://127.0.0.1:8000/cart/`
- **Method:** GET

## Register New User
- **URL:** `http://127.0.0.1:8000/create_user/`
- **Method:** POST
  ```json
  {
      "email": "admin@gmail.com",
      "password": "root"
  }
  ```

## Logout
- **URL:** `http://127.0.0.1:8000/logout/`
- **Method:** POST


