from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import random

from .models import Character
# Create your views here.

def index(request):
    items = list(Character.objects.all())
    current_character = random.choice(items)
    template = loader.get_template("titleguesser/index.html")
    context = {"current_character": current_character}
    return HttpResponse(template.render(context, request))