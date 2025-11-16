from .models import Category, Quiz, Question, Option
from django.contrib.auth import get_user_model

User = get_user_model()

class CategoryService:
    @staticmethod
    def create_category(name, description=""):
        return Category.objects.create(name=name, description=description)
    
    @staticmethod
    def get_all_categories():
        return Category.objects.all()
    
    @staticmethod
    def get_category_by_id(category_id):
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return None

class QuizService:
    @staticmethod
    def create_quiz(title, description, category_id, user):
        category = CategoryService.get_category_by_id(category_id)
        if not category:
            raise ValueError("Category not found")
        
        return Quiz.objects.create(
            title=title,
            description=description,
            category=category,
            created_by=user
        )
    
    @staticmethod
    def get_all_quizzes():
        return Quiz.objects.select_related('category', 'created_by').filter(is_active=True)
    
    @staticmethod
    def get_quiz_by_id(quiz_id):
        try:
            return Quiz.objects.select_related('category').prefetch_related('questions__options').get(id=quiz_id, is_active=True)
        except Quiz.DoesNotExist:
            return None

class QuestionService:
    @staticmethod
    def create_question_with_options(quiz_id, text, options_data):
        quiz = QuizService.get_quiz_by_id(quiz_id)
        if not quiz:
            raise ValueError("Quiz not found")
        
        # Check if quiz already has 4 questions
        if quiz.questions.count() >= 4:
            raise ValueError("Quiz already has maximum 4 questions")
        
        # Create question
        question = Question.objects.create(quiz=quiz, text=text)
        
        # Create options
        correct_count = 0
        for option_data in options_data:
            if option_data.get('is_correct', False):
                correct_count += 1
        
        if correct_count != 1:
            question.delete()
            raise ValueError("Exactly one option must be correct")
        
        for option_data in options_data:
            Option.objects.create(
                question=question,
                text=option_data['text'],
                is_correct=option_data.get('is_correct', False)
            )
        
        return question
    
    @staticmethod
    def get_questions_by_quiz(quiz_id):
        return Question.objects.filter(quiz_id=quiz_id).prefetch_related('options')