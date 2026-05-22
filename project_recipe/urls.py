from django.contrib import admin
from django.urls import path
from recipe import views


urlpatterns = [
    path('', views.main, name='main'),
    path('categories/', views.category_list, name='category_list'),
    path('admin/', admin.site.urls),
]
