from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Category, Quiz, Question
from .serializers import (
    CategorySerializer, QuizSerializer, CreateQuizSerializer, 
    CreateQuestionSerializer, QuestionSerializer, ToggleQuizStatusSerializer,
    SubmitAnswerSerializer, SubmissionSerializer, SimpleUserScoreSerializer, AdminSubmissionOverviewSerializer
)
from .services import CategoryService, QuizService, QuestionService, SubmissionService
from .permissions import IsAdminUser
from utlis.response import ResponseHandler

class CategoryListCreateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        categories = CategoryService.get_all_categories()
        serializer = CategorySerializer(categories, many=True)
        return ResponseHandler.success(data=serializer.data, message="Categories retrieved successfully")
    
    def post(self, request):
        if not request.data:
            return ResponseHandler.error(error="Category name is required")
        
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            try:
                category = CategoryService.create_category(
                    name=serializer.validated_data['name'],
                    description=serializer.validated_data.get('description', '')
                )
                return ResponseHandler.success(
                    data=CategorySerializer(category).data,
                    message="Category created successfully"
                )
            except Exception as e:
                return ResponseHandler.error(error=str(e))
        return ResponseHandler.error(error=ResponseHandler.get_error_message(serializer.errors))

class QuizListCreateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        quizzes = QuizService.get_all_quizzes()
        serializer = QuizSerializer(quizzes, many=True)
        return ResponseHandler.success(data=serializer.data, message="Quizzes retrieved successfully")
    
    def post(self, request):
        if not request.data:
            return ResponseHandler.error(error="Quiz data is required")
        
        serializer = CreateQuizSerializer(data=request.data)
        if serializer.is_valid():
            try:
                quiz = QuizService.create_quiz(
                    title=serializer.validated_data['title'],
                    description=serializer.validated_data.get('description', ''),
                    category_id=serializer.validated_data['category_id']
                )
                return ResponseHandler.success(
                    data=QuizSerializer(quiz).data,
                    message="Quiz created successfully"
                )
            except ValueError as e:
                return ResponseHandler.error(error=str(e))
            except Exception as e:
                return ResponseHandler.error(error="Failed to create quiz")
        return ResponseHandler.error(error=ResponseHandler.get_error_message(serializer.errors))

class QuestionCreateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request):
        if not request.data:
            return ResponseHandler.error(error="Question data is required")
        
        serializer = CreateQuestionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                question = QuestionService.create_question_with_options(
                    quiz_id=serializer.validated_data['quiz_id'],
                    text=serializer.validated_data['text'],
                    options_data=serializer.validated_data['options']
                )
                return ResponseHandler.success(
                    data=QuestionSerializer(question).data,
                    message="Question created successfully"
                )
            except ValueError as e:
                return ResponseHandler.error(error=str(e))
            except Exception as e:
                return ResponseHandler.error(error="Failed to create question")
        return ResponseHandler.error(error=ResponseHandler.get_error_message(serializer.errors))

class QuizDetailView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, quiz_id):
        quiz = QuizService.get_quiz_by_id(quiz_id)
        if not quiz:
            return ResponseHandler.error(error="Quiz not found", status=404)
        
        serializer = QuizSerializer(quiz)
        return ResponseHandler.success(data=serializer.data, message="Quiz retrieved successfully")

class QuizToggleStatusView(generics.GenericAPIView):
    serializer_class = ToggleQuizStatusSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def patch(self, request, quiz_id):
        try:
            quiz = QuizService.toggle_quiz_status(quiz_id)
            status_text = "activated" if quiz.is_active else "deactivated"
            return ResponseHandler.success(
                data={"id": quiz.id, "is_active": quiz.is_active},
                message=f"Quiz {status_text} successfully"
            )
        except ValueError as e:
            return ResponseHandler.error(error=str(e), status=404)
        except Exception as e:
            return ResponseHandler.error(error="Failed to toggle quiz status")

class SubmitAnswerView(generics.GenericAPIView):
    serializer_class = SubmitAnswerSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if not request.data:
            return ResponseHandler.error(error="Question ID and option ID are required")
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                submission = SubmissionService.submit_answer(
                    user=request.user,
                    question_id=serializer.validated_data['question_id'],
                    option_id=serializer.validated_data['option_id']
                )
                return ResponseHandler.success(
                    data=SubmissionSerializer(submission).data,
                    message="Answer submitted successfully"
                )
            except ValueError as e:
                return ResponseHandler.error(error=str(e))
            except Exception as e:
                return ResponseHandler.error(error="Failed to submit answer")
        return ResponseHandler.error(error=ResponseHandler.get_error_message(serializer.errors))

class UserSubmissionView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, quiz_id):
        submission = SubmissionService.get_user_submission(request.user, quiz_id)
        if not submission:
            return ResponseHandler.error(error="No submission found for this quiz", status=404)
        
        serializer = SubmissionSerializer(submission)
        return ResponseHandler.success(data=serializer.data, message="Submission retrieved successfully")

class QuizSubmissionsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request, quiz_id):
        submissions = SubmissionService.get_quiz_submissions(quiz_id)
        serializer = SubmissionSerializer(submissions, many=True)
        return ResponseHandler.success(data=serializer.data, message="Quiz submissions retrieved successfully")

class UserAllSubmissionsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        quiz_overview = SubmissionService.get_user_quiz_overview(request.user)
        
        # Format attended quizzes
        attended = [f"{quiz['quiz_title']}: {quiz['score']} ({quiz['status']})" 
                   for quiz in quiz_overview['attended']]
        
        # Format not attended quizzes
        not_attended = [f"{quiz['quiz_title']}: {quiz['status']}" 
                       for quiz in quiz_overview['not_attended']]
        
        return ResponseHandler.success(
            data={
                "attended_quizzes": attended,
                "not_attended_quizzes": not_attended,
                "summary": {
                    "total_quizzes": len(attended) + len(not_attended),
                    "attended_count": len(attended),
                    "not_attended_count": len(not_attended)
                }
            },
            message="User quiz overview retrieved successfully"
        )

class AdminSubmissionOverviewView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        submissions = SubmissionService.get_all_submissions()
        serializer = AdminSubmissionOverviewSerializer(submissions, many=True)
        
        # Calculate summary statistics
        total_submissions = submissions.count()
        completed_submissions = submissions.filter(is_completed=True).count()
        in_progress_submissions = submissions.filter(is_completed=False, attempted_count__gt=0).count()
        
        summary = {
            "total_submissions": total_submissions,
            "completed_submissions": completed_submissions,
            "in_progress_submissions": in_progress_submissions,
            "completion_rate": round((completed_submissions / total_submissions * 100), 2) if total_submissions > 0 else 0
        }
        
        return ResponseHandler.success(
            data={
                "summary": summary,
                "submissions": serializer.data
            },
            message="Admin submission overview retrieved successfully"
        )