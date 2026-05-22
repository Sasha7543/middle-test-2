from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Category, Recipe


class MainViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Breakfast')

    def create_recipe(self, title, days_ago):
        recipe = Recipe.objects.create(
            title=title,
            description=f'{title} description',
            instructions=f'{title} instructions',
            ingredients=f'{title} ingredients',
            category=self.category,
        )
        Recipe.objects.filter(pk=recipe.pk).update(
            created_at=timezone.now() - timedelta(days=days_ago)
        )
        recipe.refresh_from_db()
        return recipe

    def test_main_view_shows_last_five_created_recipes(self):
        recipes = [
            self.create_recipe(f'Recipe {index}', days_ago=6 - index)
            for index in range(6)
        ]

        response = self.client.get(reverse('main'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        self.assertQuerySetEqual(
            response.context['recipes'],
            list(reversed(recipes[1:])),
            transform=lambda recipe: recipe,
        )
        self.assertContains(response, 'Recipe 5')
        self.assertNotContains(response, 'Recipe 0')
