from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Material, Test, Question, Choice
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    choice_set = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'test', 'text', 'choice_set']

class TestSerializer(serializers.ModelSerializer):
    question_set = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ['id', 'material', 'title', 'question_set']

class MaterialSerializer(serializers.ModelSerializer):
    test_set = TestSerializer(many=True)

    class Meta:
        model = Material
        fields = ['id', 'section', 'title', 'content', 'test_set']
