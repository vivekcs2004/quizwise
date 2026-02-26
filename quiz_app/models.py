from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    phone = models.CharField(max_length=15,unique=True)

class Language(models.Model):

    language_name = models.CharField(max_length=100)

    def __str__(self):
        return self.language_name

class Quiz(models.Model):

    title = models.CharField(max_length=100)

    language = models.ForeignKey(Language,on_delete=models.CASCADE,related_name="quizes")

    LEVEL_OPTIONS = (("easy","easy"),
                     ("medium","medium"),
                     ("hard","hard"))
    level = models.CharField(max_length=100,choices=LEVEL_OPTIONS,default="easy")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes")
    #mark
    def __str__(self):
        return self.title
    
class Question(models.Model):

    text = models.CharField(max_length=200)

    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name="questions")

    def __str__(self):
        return self.text
    
class Choices(models.Model):

    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name="choices")

    option = models.CharField(max_length=100)

    is_correct = models.BooleanField()

    def __str__(self):
        return self.option
    

class QuizAttempt(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="attempts")

    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name="attempts")

    started_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):

    attempt = models.ForeignKey(QuizAttempt,on_delete=models.CASCADE,related_name="answers")

    question = models.ForeignKey(Question,on_delete=models.CASCADE)

    selected_choice = models.ForeignKey(Choices,on_delete=models.CASCADE)

    class Meta:
        unique_together = ("attempt","question")
                       
class QuizResult(models.Model):

    attempt = models.ForeignKey(QuizAttempt,on_delete=models.CASCADE,related_name="results")

    score = models.IntegerField()

    total_questions = models.IntegerField()


  

   





    
