from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Flashcard(models.Model):
    DIFICULDADE_CHOICES = (('D', 'Difícil'), ('M', 'Médio'), ('F', 'Fácil'))
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question = models.CharField(max_length=100)
    answer = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    dificulty = models.CharField(max_length=1, choices=DIFICULDADE_CHOICES)

    @property
    def css_dificuldade(self):
        if self.dificulty == 'F':
            return 'flashcard-facil'
        elif self.dificulty == 'M':
            return 'flashcard-medio'
        elif self.dificulty == 'D':
            return 'flashcard-dificil'

    def __str__(self):
        return self.question
    
class FlashcardChallenge(models.Model):
    flashcard = models.ForeignKey(Flashcard, on_delete=models.DO_NOTHING)
    answered = models.BooleanField(default=False)
    right = models.BooleanField(default=False)

    def __str__(self):
        return self.flashcard.question


class Challenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    category = models.ManyToManyField(Category)
    questions_quantity = models.IntegerField()
    dificulty = models.CharField(
        max_length=1, choices=Flashcard.DIFICULDADE_CHOICES
    )
    flashcards = models.ManyToManyField(FlashcardChallenge)

    def __str__(self):
        return self.title