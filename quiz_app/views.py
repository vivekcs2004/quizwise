from django.shortcuts import render

from quiz_app.serializers import (
    UserSerializer,
    QuizSerializer,
    QuestionSerializer,
    ChoicesSerializer,
    QuizAttemptSerializer,
    AnswerSerializer,LanguageSerializer,QuizResultSerializer
)

from rest_framework.generics import (
    ListCreateAPIView,
    CreateAPIView,
    RetrieveAPIView,
    DestroyAPIView
)
from  rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import authentication, permissions, serializers

from quiz_app.models import Quiz, Question, Choices, QuizAttempt,Language
from quiz_app.permissions import IsOwner



class SignUpView(CreateAPIView):

    serializer_class = UserSerializer

class LanguageCreateView(CreateAPIView):

    serializer_class = LanguageSerializer

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = Language.objects.all()


class QuizCreateListView(ListCreateAPIView):

    serializer_class = QuizSerializer

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):

        serializer.save(owner=self.request.user)

    def get_queryset(self):

        return Quiz.objects.all()


class QuizRetrieveView(RetrieveAPIView):

    serializer_class = QuizSerializer

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = Quiz.objects.all()


class QuizDestroyView(DestroyAPIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsOwner]

    queryset = Quiz.objects.all()




class QuestionCreateView(CreateAPIView):

    serializer_class = QuestionSerializer

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):

        quiz_id = self.kwargs.get("pk")

        quiz_instance = Quiz.objects.get(id=quiz_id)

        serializer.save(quiz=quiz_instance)




class ChoiceCreateView(CreateAPIView):

    serializer_class = ChoicesSerializer

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsOwner]

    def perform_create(self, serializer):

        question_id = self.kwargs.get("pk")

        question_instance = Question.objects.get(id=question_id)

        serializer.save(question=question_instance)




class QuizAttemptCreateView(CreateAPIView):

    serializer_class = QuizAttemptSerializer

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):

        quiz_id = self.kwargs.get("pk")

        quiz_instance = Quiz.objects.get(id=quiz_id)

        serializer.save(user=self.request.user, quiz=quiz_instance)




class AnswerCreateView(CreateAPIView):

    serializer_class = AnswerSerializer

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):

        attempt_id = self.kwargs.get("pk")

        attempt_instance = QuizAttempt.objects.get(id=attempt_id)

        question_object = serializer.validated_data.get("question")
        choice_object = serializer.validated_data.get("selected_choice")

        
        if choice_object.question != question_object:

            raise serializers.ValidationError("invalid choice for question")

        serializer.save(attempt=attempt_instance)


class QuizResultCreateView(APIView):

    serializer_class = QuizResultSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):

        
        attempt = QuizAttempt.objects.get(id=pk)

        
        if attempt.user != request.user:
            return Response({"user does not match"})

        
        correct_count = attempt.answers.filter(selected_choice__is_correct=True).count()

        
        total_questions = attempt.quiz.questions.count()

        return Response({"attempt_id": attempt.id,
            "score": correct_count,
            "total_questions": total_questions,
            "owner": request.user.username,        
            "quiz_title": attempt.quiz.title       
        })