# BookStore App

A web-based bookstore management system featuring a role-based access control model. The application is built with **Streamlit** for the frontend, **FastAPI** for the backend, and **PostgreSQL** as the database using **SQLAlchemy ORM**.

**Live Application:** https://rithwiks-bookstore.streamlit.app

---

# Tech Stack

| Component        | Technology                        |
| ---------------- | --------------------------------- |
| Frontend         | Streamlit                         |
| Frontend Theme   | https://github.com/streamlit/docs |
| Backend          | FastAPI                           |
| API Hosting      | Render                            |
| ORM              | SQLAlchemy                        |
| Database         | PostgreSQL                        |
| Database Hosting | Supabase                          |

---

# User Roles

The application supports three user roles with different permission levels.

## Admin (Superuser)

The Admin is the highest-privileged account in the system.

* A single admin account is automatically created when the database is initialized.
* Cannot be created through the application interface.

### Permissions

* View all books
* Add books
* Update any book
* Delete any book
* View all registered user information (excluding passwords)

---

## Trial Admin

A Trial Admin is intended for demonstration purposes and has limited administrative privileges.

### Permissions

* View all books
* Add new books
* Update only the books they created
* Delete only the books they created
* Update their own account information
* Delete their own account

---

## User

A regular user account created through the registration process.

### Permissions

* Browse all available books
* Add books to cart
* Purchase books through checkout
* Request refunds for individual books or all purchased books
* Update their own account information
* Delete their own account

---

# Role-Based Permissions

| Feature                | Admin | Trial Admin | User |
| ---------------------- | :---: | :---------: | :--: |
| View all books         |   ✓   |      ✓      |   ✓  |
| Add books              |   ✓   |      ✓      |   ✗  |
| Update any book        |   ✓   |      ✗      |   ✗  |
| Update own books       |   —   |      ✓      |   ✗  |
| Delete any book        |   ✓   |      ✗      |   ✗  |
| Delete own books       |   —   |      ✓      |   ✗  |
| View user information  |   ✓   |      ✗      |   ✗  |
| Update own profile     |   ✗   |      ✓      |   ✓  |
| Delete own account     |   ✗   |      ✓      |   ✓  |
| Add books to cart      |   ✗   |      ✗      |   ✓  |
| Checkout cart          |   ✗   |      ✗      |   ✓  |
| Refund purchased books |   ✗   |      ✗      |   ✓  |

---

# Application Overview

The BookStore App demonstrates a complete full-stack implementation featuring:

* Role-based authentication and authorization
* JWT-based user authentication
* CRUD operations for book management
* Shopping cart functionality
* Checkout and purchase workflow
* Refund management
* PostgreSQL database integration using SQLAlchemy ORM
* RESTful API built with FastAPI
* Interactive frontend developed with Streamlit

---

# Deployment

| Service     | Platform                  |
| ----------- | ------------------------- |
| Frontend    | Streamlit Community Cloud |
| Backend API | Render                    |
| Database    | Supabase PostgreSQL       |
