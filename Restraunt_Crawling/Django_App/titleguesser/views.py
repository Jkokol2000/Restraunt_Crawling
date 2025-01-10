from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
import random

from .models import Character


def index(request):
    # Initialize session state if not already set
    if 'lives' not in request.session or 'score' not in request.session:
        request.session['lives'] = 3
        request.session['score'] = 0
        request.session['current_character_id'] = random.choice(list(Character.objects.all())).id
        request.session.modified = True

    # Retrieve the current character from session
    try:
        current_character = Character.objects.get(id=request.session['current_character_id'])
    except (Character.DoesNotExist, KeyError):
        # If the character ID is invalid, reset it
        current_character = random.choice(list(Character.objects.all()))
        request.session['current_character_id'] = current_character.id
        request.session.modified = True

    if request.method == 'POST':
        player_answer = request.POST.get('answer', '').strip()
        correct_answer = current_character.name

        if player_answer.lower() == correct_answer.lower():
            request.session['score'] += 10  # Increase score on correct answer
        else:
            request.session['lives'] -= 1  # Decrease lives on incorrect answer

        # Update character for the next round
        request.session['current_character_id'] = random.choice(list(Character.objects.all())).id
        request.session.modified = True

        # Prevent form resubmission on refresh
        return redirect('index')

    template = loader.get_template("titleguesser/index.html")
    context = {
        "current_character": current_character,
        "lives": request.session["lives"],
        "score": request.session["score"]
    }

    # Check if game over
    if request.session['lives'] <= 0:
        return render(request, 'titleguesser/game_over.html', {'score': request.session['score']})

    return HttpResponse(template.render(context, request))

def search_characters(request):
    query = request.GET.get('q', '')
    if query:
        results = Character.objects.filter(name__icontains=query)[:5]
        suggestions = [character.name for character in results]
        return JsonResponse({'suggestions': suggestions})
    return JsonResponse({'suggestions': []})