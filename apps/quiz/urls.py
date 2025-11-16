from django.urls import path
from .views import (
    CategoryListCreateView, QuizListCreateView, 
    QuestionCreateView, QuizDetailView
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('quizzes/', QuizListCreateView.as_view(), name='quiz-list-create'),
    path('questions/', QuestionCreateView.as_view(), name='question-create'),
    path('quizzes/<int:quiz_id>/', QuizDetailView.as_view(), name='quiz-detail'),
]