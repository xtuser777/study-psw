from django.http import Http404
from django.shortcuts import render, redirect
from .models import Category, Flashcard, Challenge, FlashcardChallenge
from django.contrib.messages import constants
from django.contrib import messages

# Create your views here.
def new_flashcard(request):
    if not request.user.is_authenticated:
        return redirect('/users/login')

    if request.method == 'GET':
        categories = Category.objects.all()
        dificulties = Flashcard.DIFICULDADE_CHOICES
        flashcards = Flashcard.objects.filter(user=request.user)

        categoria_filtrar = request.GET.get('categoria')
        dificuldade_filtrar = request.GET.get('dificuldade')

        if categoria_filtrar:
            flashcards = flashcards.filter(category__id=categoria_filtrar)

        if dificuldade_filtrar:
            flashcards = flashcards.filter(dificulty=dificuldade_filtrar)

        return render(
            request,
            'new_flashcard.html',
            {
                'categories': categories,
                'dificulties': dificulties,
                'flashcards': flashcards,
            }
        )
    elif request.method == 'POST':
        pergunta = request.POST.get('pergunta')
        resposta = request.POST.get('resposta')
        categoria = request.POST.get('categoria')
        dificuldade = request.POST.get('dificuldade')

        if len(pergunta.strip()) == 0 or len(resposta.strip()) == 0:
            messages.add_message(
                request,
                constants.ERROR,
                'Preencha os campos de pergunta e resposta',
            )
            return redirect('/flashcard/new_flashcard')

        flashcard = Flashcard(
            user=request.user,
            question=pergunta,
            answer=resposta,
            category_id=categoria,
            dificulty=dificuldade,
        )

        flashcard.save()

        messages.add_message(
            request, constants.SUCCESS, 'Flashcard criado com sucesso'
        )
        return redirect('/flashcard/new_flashcard')
    
def delete_flashcard(request, id):
    flashcard = Flashcard.objects.get(id=id)
    flashcard.delete()
    messages.add_message(
        request, constants.SUCCESS, 'Flashcard deletado com sucesso!'
    )
    return redirect('/flashcard/new_flashcard')

def start_challenge(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        dificulties = Flashcard.DIFICULDADE_CHOICES
        return render(
            request,
            'start_challenge.html',
            {'categories': categories, 'dificulties': dificulties},
        )
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        categorias = request.POST.getlist('categoria')
        dificuldade = request.POST.get('dificuldade')
        qtd_perguntas = request.POST.get('qtd_perguntas')

        challenge = Challenge(
            user=request.user,
            title=titulo,
            questions_quantity=qtd_perguntas,
            dificulty=dificuldade,
        )
        challenge.save()

        challenge.category.add(*categorias)

        flashcards = (
            Flashcard.objects.filter(user=request.user)
            .filter(dificulty=dificuldade)
            .filter(category_id__in=categorias)
            .order_by('?')
        )

        if flashcards.count() < int(qtd_perguntas):
            return redirect('/flashcard/start_challenge/')

        flashcards = flashcards[: int(qtd_perguntas)]

        for f in flashcards:
            flashcard_challenge = FlashcardChallenge(
                flashcard=f,
            )
            flashcard_challenge.save()
            challenge.flashcards.add(flashcard_challenge)

        challenge.save()

        return redirect(f'/flashcard/challenge/{challenge.id}')
    
def list_challenges(request):
    challenges = Challenge.objects.filter(user=request.user)
    return render(
        request,
        'list_challenges.html',
        {
            'challenges': challenges,
        },
    )

def challenge(request, id):
    challenge = Challenge.objects.get(id=id)

    if not challenge.user == request.user:
        raise Http404()

    rights = challenge.flashcards.filter(answered=True).filter(right=True).count()
    errors = challenge.flashcards.filter(answered=True).filter(right=False).count()
    missing = challenge.flashcards.filter(answered=False).count()

    if request.method == 'GET':
        return render(
            request,
            'challenge.html',
            {
                'challenge': challenge,
                'rights': rights,
                'errors': errors,
                'missing': missing,
            },
        )
    
def answer_flashcard(request, id):
    flashcard_challenge = FlashcardChallenge.objects.get(id=id)
    if not flashcard_challenge.flashcard.user == request.user:
        raise Http404()
    right = request.GET.get('right')
    challenge_id = request.GET.get('challenge_id')

    flashcard_challenge.answered = True
    flashcard_challenge.right = True if right == '1' else False
    flashcard_challenge.save()
    return redirect(f'/flashcard/challenge/{challenge_id}/')