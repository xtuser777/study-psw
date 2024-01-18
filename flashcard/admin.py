from django.contrib import admin

# Register your models here.
from .models import Category, Flashcard, Challenge, FlashcardChallenge
admin.site.register(Category)
admin.site.register(Flashcard)
admin.site.register(Challenge)
admin.site.register(FlashcardChallenge)