from django.shortcuts import render, redirect
from django.contrib.messages import constants
from django.contrib import messages
from .models import Handout, HandoutView

# Create your views here.
def add_books(request):
    if request.method == 'GET':
        books = Handout.objects.filter(user=request.user)
        # TODO: Create tags
        total_views = HandoutView.objects.filter(handout__user = request.user).count()
        return render(request, 'add_books.html', {'books': books, 'total_views': total_views})
    elif request.method == 'POST':
        title = request.POST.get('titulo')
        file = request.FILES['arquivo']

        handout = Handout(user=request.user, title=title, file=file)
        handout.save()
        messages.add_message(
            request, constants.SUCCESS, 'Apostila adicionada com sucesso.'
        )
        return redirect('/books/add_books/')
    
def handout(request, id):
    handout = Handout.objects.get(id=id)

    view = HandoutView(
        ip=request.META['REMOTE_ADDR'],
        handout=handout
    )
    view.save()

    unit_views = HandoutView.objects.filter(handout=handout).values('ip').distinct().count()
    total_views = HandoutView.objects.filter(handout=handout).count()

    return render(request, 'handout.html', {'handout': handout, 'unit_views': unit_views, 'total_views': total_views})