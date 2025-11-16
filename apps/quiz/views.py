from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Category, Quiz, Question
from .serializers import (
    CategorySerializer, QuizSerializer, CreateQuizSerializer, 
    CreateQuestionSerializer, QuestionSerializer
)
from .services import CategoryService, QuizService, QuestionService
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
                    category_id=serializer.validated_data['category_id'],
                    user=request.user
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