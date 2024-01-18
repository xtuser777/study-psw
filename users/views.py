from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth

# Create your views here.
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            messages.add_message(
                request, constants.ERROR, 'As senhas não coincídem'
            )
            return redirect('/users/register')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(
                request,
                constants.ERROR,
                'Já existe um usuário com o mesmo username',
            )
            return redirect('/users/register')

        try:
            user = User.objects.create_user(
                username=username,
                password=confirmar_senha,
            )
            messages.add_message(
                request, constants.ERROR, 'Usuário cadastrado com sucesso.'
            )
            return redirect('/users/login')
        except:
            messages.add_message(
                request, constants.ERROR, 'Erro interno do sistema'
            )
            return redirect('/users/register')
        
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(request, username=username, password=senha)
        print(user)
        if user:
            auth.login(request, user)
            messages.add_message(request, constants.SUCCESS, 'Logado!')
            return redirect('/flashcard/new_flashcard/')
        else:
            messages.add_message(
                request, constants.ERROR, 'Username ou senha inválidos'
            )
            return redirect('/users/login')
        
def logout(request):
    auth.logout(request)
    return redirect('/users/login')