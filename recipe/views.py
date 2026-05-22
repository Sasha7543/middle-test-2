
from django.shortcuts import render

from .models import Recipe


def main(request):
    recipes = Recipe.objects.order_by('-created_at')[:5]
    return render(request, 'main.html', {'recipes': recipes})
