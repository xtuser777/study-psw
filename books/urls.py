from django.urls import path
from . import views

urlpatterns = [
    path( 'add_books/', views.add_books, name='add_books'),
    path('handout/<int:id>', views.handout, name='handout'),
]