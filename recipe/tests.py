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


class CategoryListViewTests(TestCase):
    def test_category_list_view_shows_categories_with_recipe_count(self):
        breakfast = Category.objects.create(name='Breakfast')
        dinner = Category.objects.create(name='Dinner')
        Recipe.objects.create(
            title='Omelette',
            description='Simple breakfast',
            instructions='Cook eggs',
            ingredients='Eggs',
            category=breakfast,
        )
        Recipe.objects.create(
            title='Pancakes',
            description='Sweet breakfast',
            instructions='Cook batter',
            ingredients='Flour',
            category=breakfast,
        )

        response = self.client.get(reverse('category_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_list.html')
        self.assertContains(response, 'Breakfast (2)')
        self.assertContains(response, 'Dinner (0)')
