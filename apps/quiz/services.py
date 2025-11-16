from .models import Category, Quiz, Question, Option, Submission, SubmissionAnswer
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
    def create_quiz(title, description, category_id):
        category = CategoryService.get_category_by_id(category_id)
        if not category:
            raise ValueError("Category not found")
        
        return Quiz.objects.create(
            title=title,
            description=description,
            category=category
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
        
        # Check if question with same text already exists in this quiz
        if Question.objects.filter(quiz=quiz, text=text).exists():
            raise ValueError("Question with this text already exists in this quiz")
        
        # Validate options
        correct_count = 0
        for option_data in options_data:
            if option_data.get('is_correct', False):
                correct_count += 1
        
        if correct_count != 1:
            raise ValueError("Exactly one option must be correct")
        
        # Create question
        question = Question.objects.create(quiz=quiz, text=text)
        
        
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
    
    @staticmethod
    def toggle_quiz_status(quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
            quiz.is_active = not quiz.is_active
            quiz.save()
            return quiz
        except Quiz.DoesNotExist:
            raise ValueError("Quiz not found")

class SubmissionService:
    @staticmethod
    def submit_answer(user, question_id, option_id):
        try:
            question = Question.objects.get(id=question_id)
            option = Option.objects.get(id=option_id, question=question)
        except (Question.DoesNotExist, Option.DoesNotExist):
            raise ValueError("Question or option not found")
        
        # Get or create submission
        submission, created = Submission.objects.get_or_create(
            user=user,
            quiz=question.quiz,
            defaults={'attempted_count': 0, 'correct_count': 0}
        )
        
        # Check if answer already exists
        answer, answer_created = SubmissionAnswer.objects.get_or_create(
            submission=submission,
            question=question,
            defaults={
                'selected_option': option,
                'is_correct': option.is_correct
            }
        )
        
        # If answer already exists, update it
        if not answer_created:
            # Remove previous correct count if it was correct
            if answer.is_correct:
                submission.correct_count -= 1
            
            answer.selected_option = option
            answer.is_correct = option.is_correct
            answer.save()
        else:
            submission.attempted_count += 1
        
        # Update correct count
        if option.is_correct:
            submission.correct_count += 1
        
        # Check if quiz is completed
        total_questions = question.quiz.questions.count()
        submission.is_completed = submission.attempted_count == total_questions
        submission.save()
        
        return submission
    
    @staticmethod
    def get_user_submission(user, quiz_id):
        try:
            return Submission.objects.prefetch_related('answers__question', 'answers__selected_option').get(
                user=user, quiz_id=quiz_id
            )
        except Submission.DoesNotExist:
            return None
    
    @staticmethod
    def get_quiz_submissions(quiz_id):
        return Submission.objects.filter(quiz_id=quiz_id).select_related('user', 'quiz')
    
    @staticmethod
    def get_all_submissions():
        return Submission.objects.select_related('user', 'quiz', 'quiz__category').order_by('-updated_at')
    
    @staticmethod
    def get_user_all_submissions(user):
        return Submission.objects.filter(user=user).select_related('quiz', 'quiz__category')
    
    @staticmethod
    def get_user_quiz_overview(user):
        # Get all active quizzes with question count
        all_quizzes = Quiz.objects.filter(is_active=True).select_related('category').prefetch_related('questions')
        
        # Get user submissions
        user_submissions = Submission.objects.filter(user=user).select_related('quiz')
        submitted_quiz_ids = set(user_submissions.values_list('quiz_id', flat=True))
        
        attended_quizzes = []
        not_attended_quizzes = []
        
        for quiz in all_quizzes:
            total_questions = quiz.questions.count()
            if quiz.id in submitted_quiz_ids:
                submission = user_submissions.get(quiz=quiz)
                attended_quizzes.append({
                    'quiz_title': quiz.title,
                    'score': f"{submission.correct_count}/{total_questions}",
                    'status': 'Completed' if submission.is_completed else 'In Progress'
                })
            else:
                not_attended_quizzes.append({
                    'quiz_title': quiz.title,
                    'status': 'Not Attended'
                })
        
        return {
            'attended': attended_quizzes,
            'not_attended': not_attended_quizzes
        }