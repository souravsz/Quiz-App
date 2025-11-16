from rest_framework import serializers
from .models import Category, Quiz, Question, Option, Submission, SubmissionAnswer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'options']

class QuizSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)
    questions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'category', 'questions', 'questions_count']
    
    def get_questions_count(self, obj):
        return obj.questions.count()

class CreateQuizSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)
    category_id = serializers.IntegerField()

class CreateOptionSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=200)
    is_correct = serializers.BooleanField(default=False)

class CreateQuestionSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    text = serializers.CharField()
    options = CreateOptionSerializer(many=True)

class ToggleQuizStatusSerializer(serializers.Serializer):
    pass

class SubmitAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    option_id = serializers.IntegerField()

class SubmissionAnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.text', read_only=True)
    selected_option_text = serializers.CharField(source='selected_option.text', read_only=True)
    
    class Meta:
        model = SubmissionAnswer
        fields = ['question_text', 'selected_option_text', 'is_correct']

class SubmissionSerializer(serializers.ModelSerializer):
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    answers = SubmissionAnswerSerializer(many=True, read_only=True)
    score_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Submission
        fields = ['id', 'quiz_title', 'username', 'attempted_count', 'correct_count', 
                 'is_completed', 'score_percentage', 'answers']
    
    def get_score_percentage(self, obj):
        if obj.attempted_count == 0:
            return 0
        return round((obj.correct_count / obj.attempted_count) * 100, 2)

class SimpleUserScoreSerializer(serializers.ModelSerializer):
    quiz_score = serializers.SerializerMethodField()
    
    class Meta:
        model = Submission
        fields = ['quiz_score']
    
    def get_quiz_score(self, obj):
        return f"{obj.quiz.title}: {obj.correct_count} marks"

class AdminSubmissionOverviewSerializer(serializers.ModelSerializer):
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    category_name = serializers.CharField(source='quiz.category.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    score_percentage = serializers.SerializerMethodField()
    completion_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Submission
        fields = ['id', 'user_id', 'username', 'quiz_title', 'category_name', 
                 'attempted_count', 'correct_count', 'is_completed', 'completion_status',
                 'score_percentage']
    
    def get_score_percentage(self, obj):
        if obj.attempted_count == 0:
            return 0
        return round((obj.correct_count / obj.attempted_count) * 100, 2)
    
    def get_completion_status(self, obj):
        if obj.is_completed:
            return "Completed"
        elif obj.attempted_count > 0:
            return "In Progress"
        else:
            return "Not Started"