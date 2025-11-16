from django.urls import path
from .views import (
    CategoryListCreateView, QuizListCreateView, 
    QuestionCreateView, QuizDetailView, QuizToggleStatusView,
    SubmitAnswerView, UserSubmissionView, QuizSubmissionsView,
    UserAllSubmissionsView, AdminSubmissionOverviewView
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('quizzes/', QuizListCreateView.as_view(), name='quiz-list-create'),
    path('questions/', QuestionCreateView.as_view(), name='question-create'),
    path('quizzes/<int:quiz_id>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quizzes/<int:quiz_id>/toggle-status/', QuizToggleStatusView.as_view(), name='quiz-toggle-status'),
    path('submit-answer/', SubmitAnswerView.as_view(), name='submit-answer'),
    path('quizzes/<int:quiz_id>/my-submission/', UserSubmissionView.as_view(), name='user-submission'),
    path('my-submissions/', UserAllSubmissionsView.as_view(), name='user-all-submissions'),
    path('quizzes/<int:quiz_id>/submissions/', QuizSubmissionsView.as_view(), name='quiz-submissions'),
    path('admin/submissions-overview/', AdminSubmissionOverviewView.as_view(), name='admin-submissions-overview'),
]