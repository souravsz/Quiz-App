from rest_framework import serializers
from .models import Category, Quiz, Question, Option

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'options', 'created_at']

class QuizSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)
    questions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'category', 'created_at', 'questions', 'questions_count']
    
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