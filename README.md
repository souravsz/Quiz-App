# Quiz Management System
A Django REST API-based quiz management system with user authentication, quiz creation, and submission tracking.

# use this pip install -r requirements.txt command to install all required dependencies
pip install -r requirements.txt

# Create you env file according to the added .envexample file 
DB_NAME=quiz_db
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432

# Added Swagger API documentation so that anyone who wants to test or verify endpoints can use the documentation at this link for reference
http://127.0.0.1:8000/api/docs/

# Once the user is created, authenticate using the JWT access token and then call this endpoint to have admin access for the user currently enabled like this for easing testing process
http://127.0.0.1:8000/api/auth/promote-to-admin/

# Access token expiry is currently set to 1 hour to simplify testing during development.

# Responses include full object details (including IDs) to make it easier to test subsequent API calls during development.

## Features
- User registration and JWT authentication
- Admin role promotion for quiz management
- Category creation and quiz management
- Question creation with multiple options
- Real-time quiz submission and scoring
- Progress tracking and completion status
- Admin dashboard for monitoring submissions

## Key Endpoints
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/promote-admin/` - Promote to admin
- `POST /api/quiz/categories/` - Create categories (Admin)
- `POST /api/quiz/quizzes/` - Create quizzes (Admin)
- `POST /api/quiz/questions/` - Add questions (Admin)
- `POST /api/quiz/submit-answer/` - Submit answers
- `GET /api/quiz/my-submissions/` - View user scores
- `GET /api/quiz/admin/submissions-overview/` - Admin analytics