# Finance Data Processing and Access Control Backend

A RESTful backend API built with **FastAPI** for managing financial records with role-based access control. Supports user management, transaction CRUD, and dashboard summary analytics.

---

## Tech Stack

| Layer            |  Technology       |
|------------------|-------------------|
| Framework        | FastAPI           |
| ORM              | SQLAlchemy        |
| Database         | MySQL             |
| Auth             | JWT (python-jose) |
| Password Hashing | bcrypt (passlib)  |
| Validation       | Pydantic v2       |

---

## Features

- JWT-based authentication with role-aware tokens
- Role-based access control (Viewer / Analyst / Admin)
- Full CRUD for financial transactions
- Transaction filtering by type and category
- Dashboard APIs: income/expense summary, category totals, monthly trends, recent activity
- Input validation and descriptive error responses
- User management: create, activate/deactivate, role assignment (admin only)

---

| Action                         | Viewer | Analyst | Admin |
| ------------------------------ | :----:  | :-----: | :---: |
| Register / Login               |    ✅   |    ✅    |   ✅   |
| View own transactions          |    ✅   |    ✅    |   ✅   |
| View dashboard summary         |    ✅   |    ✅    |   ✅   |
| View category / monthly trends |    ✅   |    ✅    |   ✅   |
| Create transactions            |    ❌   |    ❌    |   ✅   |
| Update transactions            |    ❌   |    ❌    |   ✅   |
| Delete transactions            |    ❌   |    ❌    |   ✅   |
| List all users                 |    ❌   |    ❌    |   ✅   |
| Update user role               |    ❌   |    ❌    |   ✅   |
| Activate / deactivate user     |    ❌   |    ❌    |   ✅   |


> New users default to the **viewer** role. An admin must manually promote them.

---

## Project Structure

```
app/
├── main.py               # App entry point, router registration
├── database.py           # SQLAlchemy engine and session setup
├── models/
│   ├── user.py           # User ORM model
│   └── transaction.py    # Transaction ORM model
├── schemas/
│   ├── user.py           # Pydantic schemas for users
│   └── transaction.py    # Pydantic schemas for transactions
├── routes/
│   ├── auth.py           # Auth and user management endpoints
│   ├── transaction.py    # Transaction CRUD endpoints
│   └── dashboard.py      # Summary and analytics endpoints
└── core/
    ├── jwt.py            # Token creation
    ├── security.py       # Password hashing and verification
    └── deps.py           # Auth dependencies and role guards
```

---

## Prerequisites

- Python 3.10+
- MySQL server running locally
- pip

---

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/finance-backend.git
cd finance-backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy pymysql python-jose passlib bcrypt pydantic[email]
```

### 4. Set up the database

Log in to MySQL and create the database:

```sql
CREATE DATABASE finance_db;
```

### 5. Configure environment

Open `app/database.py` and update the connection string to match your MySQL credentials:

```python
DATABASE_URL = "mysql+pymysql://YOUR_USER:YOUR_PASSWORD@localhost:3306/finance_db"
```

> **Note:** For production, move this to a `.env` file using `python-dotenv`.

### 6. Run the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

---

## API Documentation

FastAPI generates interactive docs automatically once the server is running:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints

### Auth

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/auth/register` | Public | Register a new user (defaults to viewer) |
| POST | `/auth/login` | Public | Login and receive a JWT token |
| GET | `/auth/me` | Any logged-in user | Get current user profile |
| GET | `/auth/users` | Admin | List all users |
| PATCH | `/auth/users/{id}/role` | Admin | Update a user's role |
| PATCH | `/auth/users/{id}/status` | Admin | Activate or deactivate a user |

### Transactions

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/transactions/` | Admin | Create a new transaction |
| GET | `/transactions/` | Any logged-in user | List own transactions (paginated) |
| GET | `/transactions/{id}` | Any logged-in user | Get a single transaction |
| PUT | `/transactions/{id}` | Admin | Update a transaction |
| DELETE | `/transactions/{id}` | Admin | Delete a transaction |
| GET | `/transactions/filter` | Any logged-in user | Filter by `?type=` and `?category=` |

### Dashboard

| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/dashboard/summary` | Any logged-in user | Total income, expenses, net balance |
| GET | `/dashboard/category` | Any logged-in user | Totals grouped by category |
| GET | `/dashboard/recent` | Any logged-in user | Last 5 transactions |
| GET | `/dashboard/monthly` | Any logged-in user | Monthly totals |

---

## Example Requests

### Register a user

```json
POST /auth/register
{
  "name": "Ajay Gellu",
  "email": "ajay@example.com",
  "password": "securepassword"
}
```

### Login

Use the `/auth/login` endpoint via Swagger (OAuth2 form) or send:

```
username: ajay@example.com
password: securepassword
```

Returns:
```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

Pass the token in all subsequent requests as:
```
Authorization: Bearer <jwt_token>
```

### Create a transaction (admin only)

```json
POST /transactions/
{
  "amount": 5000.00,
  "type": "income",
  "category": "Salary",
  "description": "Monthly salary"
}
```

---

## Data Models

### User

| Field | Type | Notes |
|---|---|---|
| id | Integer | Primary key |
| name | String | Required |
| email | String | Unique |
| password | String | bcrypt hashed |
| role | String | viewer / analyst / admin |
| is_active | Boolean | Default: true |

### Transaction

| Field | Type | Notes |
|---|---|---|
| id | Integer | Primary key |
| amount | Float | Must be > 0 |
| type | String | income or expense |
| category | String | e.g. Salary, Rent |
| description | String | Optional |
| date | DateTime | Defaults to creation time |
| user_id | Integer | Foreign key → users |


