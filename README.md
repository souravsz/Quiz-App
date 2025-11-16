# Quiz Management System

A Django REST API-based quiz management system with user authentication, quiz creation, and submission tracking.

## Features

- **User Management**: Registration, login, admin promotion
- **Quiz Management**: Create categories, quizzes, and questions
- **Submission System**: Submit answers, track progress, view scores
- **Admin Dashboard**: Monitor all submissions and user performance
- **Real-time Scoring**: Instant feedback and progress tracking
- **API Documentation**: Swagger UI for interactive API testing

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (Simple JWT)
- **Documentation**: drf-spectacular (Swagger)
- **Architecture**: Service Layer Pattern

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Git

## Installation & Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd quiz
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Copy the example environment file and update with your values:
```bash
# Copy example file
cp .env.example .env

# Edit .env file with your database credentials
```

**Required Environment Variables:**
```env
DB_NAME=quiz_db
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 5. Database Setup
```bash
# Create PostgreSQL database
createdb quiz_db

# Run migrations
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

### 8. Access Application
- **API Base URL**: http://localhost:8000/api/
- **Swagger Documentation**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/promote-admin/` - Promote to admin

### Quiz Management (Admin Only)
- `GET/POST /api/quiz/categories/` - Manage categories
- `GET/POST /api/quiz/quizzes/` - Manage quizzes
- `POST /api/quiz/questions/` - Add questions
- `PATCH /api/quiz/quizzes/<id>/toggle-status/` - Activate/deactivate quiz

### Quiz Taking
- `GET /api/quiz/quizzes/<id>/` - View quiz details
- `POST /api/quiz/submit-answer/` - Submit answer
- `GET /api/quiz/quizzes/<id>/my-submission/` - View submission
- `GET /api/quiz/my-submissions/` - View all user submissions

### Admin Analytics
- `GET /api/quiz/quizzes/<id>/submissions/` - Quiz submissions
- `GET /api/quiz/admin/submissions-overview/` - All submissions overview

## Usage Examples

### 1. User Registration
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "password123"}'
```

### 2. Create Category (Admin)
```bash
curl -X POST http://localhost:8000/api/quiz/categories/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Mathematics", "description": "Math quizzes"}'
```

### 3. Create Quiz (Admin)
```bash
curl -X POST http://localhost:8000/api/quiz/quizzes/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Basic Math", "category_id": 1}'
```

### 4. Add Question (Admin)
```bash
curl -X POST http://localhost:8000/api/quiz/questions/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "quiz_id": 1,
    "text": "What is 2+2?",
    "options": [
      {"text": "3", "is_correct": false},
      {"text": "4", "is_correct": true},
      {"text": "5", "is_correct": false}
    ]
  }'
```

### 5. Submit Answer
```bash
curl -X POST http://localhost:8000/api/quiz/submit-answer/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"question_id": 1, "option_id": 2}'
```

## Project Structure

```
quiz/
├── apps/
│   ├── users/          # User management
│   └── quiz/           # Quiz functionality
├── config/             # Django settings
├── utlis/              # Utilities (ResponseHandler)
├── .env               # Environment variables
├── manage.py
└── requirements.txt
```

## Architecture

### Service Layer Pattern
- **Models**: Database entities
- **Services**: Business logic
- **Serializers**: Data validation
- **Views**: API endpoints
- **ResponseHandler**: Consistent API responses

### Key Components
- **CategoryService**: Category management
- **QuizService**: Quiz operations
- **QuestionService**: Question handling
- **SubmissionService**: Answer tracking
- **UserService**: User operations

## Database Schema

### Core Models
- **Category**: Quiz categories
- **Quiz**: Quiz instances
- **Question**: Quiz questions
- **Option**: Answer choices
- **Submission**: User quiz attempts
- **SubmissionAnswer**: Individual answers

### Relationships
- Category → Quiz (1:N)
- Quiz → Question (1:N)
- Question → Option (1:N)
- User → Submission (1:N)
- Submission → SubmissionAnswer (1:N)

## Features

### Quiz Rules
- Maximum 4 questions per quiz
- Exactly one correct answer per question
- No duplicate questions in same quiz
- Real-time score calculation

### User Permissions
- **Public**: Registration, login
- **Authenticated**: Take quizzes, view own submissions
- **Admin**: Create/manage quizzes, view all submissions

### Scoring System
- Format: "correct/total" (e.g., "3/4")
- Real-time updates
- Progress tracking
- Completion detection

## Quick Start Guide

### 1. Register a User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

### 2. Login & Get Token
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

### 3. Promote to Admin
```bash
curl -X POST http://localhost:8000/api/auth/promote-admin/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Create Category (Admin)
```bash
curl -X POST http://localhost:8000/api/quiz/categories/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Mathematics", "description": "Math quizzes"}'
```

## Project Structure

```
quiz/
├── apps/
│   ├── users/              # User management
│   │   ├── models.py       # User model
│   │   ├── serializers.py  # User serializers
│   │   ├── services.py     # User business logic
│   │   ├── views.py        # User API endpoints
│   │   └── urls.py         # User URL patterns
│   └── quiz/               # Quiz functionality
│       ├── models.py       # Quiz, Question, Option models
│       ├── serializers.py  # Quiz serializers
│       ├── services.py     # Quiz business logic
│       ├── views.py        # Quiz API endpoints
│       ├── permissions.py  # Custom permissions
│       └── urls.py         # Quiz URL patterns
├── config/                 # Django configuration
│   ├── settings/
│   │   ├── base.py         # Base settings
│   │   └── dev.py          # Development settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── utlis/                  # Utility modules
│   └── response.py         # Response handler
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies
├── manage.py               # Django management script
└── README.md               # This file
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Make sure virtual environment is activated
2. **Database Connection Error**: Check PostgreSQL is running and credentials in .env
3. **Migration Issues**: Run `python manage.py makemigrations` then `python manage.py migrate`
4. **Permission Denied**: Ensure user has admin role for admin endpoints

### Reset Database
```bash
# Drop and recreate database
dropdb quiz_db
createdb quiz_db
python manage.py migrate
```

## Development

### Running Tests
```bash
python manage.py test
```

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Keep functions small and focused

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - see LICENSE file for details