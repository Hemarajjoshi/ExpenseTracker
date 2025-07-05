# Expense Tracker API
A Restful API for tracking personal expenses and incomes , built using django rest framework which includes
 JWT Authentication , Swagger documentation and Pagination. 


## Features
- User Registration and Login Via JWT
- Add, Update , Delete expense/Income Records
- Tax Calculation
- Personal Data Isolation (User Can only access to their own Expense/Income)
- SuperUser can access to all
- Paginated List Responses
- Swagger Documentation


## Tech Used
- Python 
- Django
- Django Rest Framework
- Simple JWT (djangorestframework-simpleJwt)
- drf-yasg(openAPI/Swagger)
- SQLite


## Setup Instruction

i. Clone the repository

```bash
git clone https://github.com/Hemarajjoshi/ExpenseTracker.git
cd ExpenseTracker
```

ii. Create a virtual environment and activate it

```bash 
python -m venv venv
venv\Scripts\activate #for windows 
source venv/bin/activate #for linux/mac
```

iii. Install dependencies

```bash
pip install -r requirements.txt
```

iv. Create .env file and paste the following 

```bash
    DEBUG = True
```


v. Run the development server

```bash
python manage.py runserver
```

vi. Make Migrations and Migrate

```bash
python manage.py makemigrations
python manage.py migrate
```

vii. Create SuperUser

```bash
python manage.py createsuperuser
```

viii. Run Tests

```bash
python manage.py test
```

ix. Run Swagger

```bash
python manage.py runserver
```

## API Endpoints


### Authentication
- Register User : http://localhost:8000/api/auth/register/
- Login User : http://localhost:8000/api/auth/login/
- Token Refresh : http://localhost:8000/api/auth/refresh/

### Expense
- List Expense : http://localhost:8000/api/expense/
- Create Expense : http://localhost:8000/api/expense/
- Update Expense : http://localhost:8000/api/expense/{id}/
- Delete Expense : http://localhost:8000/api/expense/{id}/


## Sample Create Request

```json
{
    "title": "Sample Expense",
    "description": "This is a sample expense",
    "amount": 100.00,
    "transaction_type": "Expense",
    "tax": 10.00,
    "tax_type": "Flat"
}
```

## Sample Response

```json
{
    "id": 1,
    "title": "Sample Expense",
    "description": "This is a sample expense",
    "amount": 100.00,
    "transaction_type": "Expense",
    "tax": 10.00,
    "tax_type": "Flat",
    "total": 110.00,
    "created_at": "2023-05-01T10:00:00Z",
    "updated_at": "2023-05-01T10:00:00Z",
    "user": 1
}
```

## Author 

- Name : Hemraj Joshi
- Email : hemrajjoshi3211@gmail.com


