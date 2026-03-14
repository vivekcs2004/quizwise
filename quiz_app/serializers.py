from rest_framework import serializers
from quiz_app.models import (
    User,
    Language,
    Quiz,
    Question,
    Choices,
    QuizAttempt,
    Answer,
    QuizResult
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "phone", "password"]
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self,data):
        return User.objects.create_user(**data)
        


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "language_name"]
        read_only_fields = ["id"]




class QuizSerializer(serializers.ModelSerializer):

    questions = serializers.SerializerMethodField()
    owner = serializers.StringRelatedField()
    language = serializers.StringRelatedField()

    class Meta:
        model = Quiz
        fields = ["id", "title", "language", "level","owner",'questions']
        read_only_fields = ["id","owner"]

    def get_questions(self, obj):  
        questions = obj.questions.all()  
        return QuestionSerializer(questions, many=True).data


class QuestionSerializer(serializers.ModelSerializer):

    choices = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ["id", "text", "quiz",'choices']
        read_only_fields = ["id",'quiz']
    
    def get_choices(self, obj): 
        choices = obj.choices.all()  
        return ChoicesSerializer(choices, many=True).data
    
    def validate(self, data):

        question_text = data.get("text")

        # quiz id comes from URL
        quiz_id = self.context["view"].kwargs.get("pk")
        #self.context["view"].kwargs → URL parameters captured by Django  {"pk": 42}#.get("pk") → grab the value 42

        # check if same question already exists in that quiz
        
        if Question.objects.filter(quiz_id=quiz_id,text=question_text).exists():

            raise serializers.ValidationError(
                "This question already exists in this quiz."
            )

        return data



class ChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = ["id", "question", "option", "is_correct"]
        read_only_fields = ["id",'question']


    def validate(self, data):

        option_text = data.get("option")

        # question id comes from URL
        question_id = self.context["view"].kwargs.get("pk")

        # check duplicate option for same question
        if Choices.objects.filter(question_id=question_id, option=option_text).exists():

            raise serializers.ValidationError(
                "This option already exists for this question.")

        return data


class QuizAttemptSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()
    quiz = serializers.StringRelatedField()
    class Meta:
        model = QuizAttempt
        fields = ["id", "user", "quiz", "started_at"]
        read_only_fields = ["id", "started_at",'user','quiz']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "attempt", "question", "selected_choice"]
        read_only_fields = ["id",'attempt']

    def validate(self, data):

        if data["selected_choice"].question != data["question"]:
            raise serializers.ValidationError("Invalid choice for question")
        
        attempt = self.context["view"].kwargs.get("pk")  
        question = data["question"]

        if Answer.objects.filter(attempt_id=attempt, question=question).exists():
            raise serializers.ValidationError("You already answered this question.")

        return data

      


class QuizResultSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    quiz_title = serializers.SerializerMethodField()
    class Meta:
        model = QuizResult
        fields = ["id", "attempt", "score", "total_questions",'owner','quiz_title']
        read_only_fields = ["id", "owner", "quiz_title"]

    def get_owner(self, obj):
        return obj.attempt.user.username

    def get_quiz_title(self, obj):
        return obj.attempt.quiz.title