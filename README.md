# Secure_authentication_system
A secure login system with JWT authentication and encryption.

# Secure Authentication System
Folder Structure
Secure_Authentication_System/
│
├─ app.py
├─ User_model.py
├─ requirements.txt
└─ README.md    
   - Project Description

   - A secure authentication system built with Python, Flask, PostgreSQL, and JWT.
   - It allows users to register, login, and access protected routes with token-based authentication.
   - Passwords are hashed using bcrypt for security.

This project demonstrates secure user registration, authentication, and session management using JWT tokens.

Technologies Used

   - Python 3.12
   - Flask
   - Flask-SQLAlchemy
   - PostgreSQL
   - PyJWT (JWT authentication)
   - bcrypt (password hashing)
   - Waitress (production-ready server)

Features

   - User registration with unique email
   - Password hashing for security
   - Login with email & password
   - JWT-based authentication for session management
   - Protected routes accessible only with a valid token

Setup Instructions

1. Clone the repository

    git clone <your-repo-url>
    cd Secure_Authentication_System


2. Create virtual environment

    python -m venv venv


3. Activate virtual environment

      - Windows (PowerShell):

    .\venv\Scripts\Activate.ps1

       - Linux/Mac:

        source venv/bin/activate


4. Install dependencies

    pip install -r requirements.txt


5. Configure database

        Make sure PostgreSQL is installed and running
        Create a database (example: Secure_auth_db)
        Update app.py with your database credentials:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:YOUR_PASSWORD@localhost:5432/Secure_auth_db'


6. Run the application

    python app.py

    Server will run on http://localhost:9090
_____________________________________________________________

API Endpoints
1. Register User

    URL: POST /register

    Body (JSON):

    {
    "name": "<Your Name Here>",
    "email": "Your Email Here",
    "password": "Your Pass Here"
    }


Response:

    {"message": "User registered successfully"}

 2. Login User

    URL: POST /login

    Body (JSON):

    {
    "email": "",
    "password": "<Your Pass here>"
    }


Response:

    {
    "message": "Login successful",
    "token": "<JWT token here>"
    }

3. Dashboard (Protected Route)

    URL: GET /dashboard

    Headers:

    Key: Authorization
    Value: <JWT token from login>


Response:

{
  "message": "Welcome Admin! This is your dashboard."
}


- Users must include a valid JWT token in the request header to access this route.

Notes
- Emails must be unique for each user
- Passwords are stored securely with bcrypt
- JWT token expires in 1 hour, after which users need to re-login
