from pyexpat import model
from turtle import mode
from django.contrib.auth import get_user_model
from django.db import models

# from django.urls import reverse

User = get_user_model()  # временное решение


class Teg(models.Model):
    """Тег"""

    # наименование
    title = models.CharField(max_length=200, unique=True)
    # цветовой Hex-код
    color = models.CharField(max_length=7, unique=True)
    # slug
    slug = models.SlugField(unique=True)

    # class Meta:
    #     verbose_name = "Тег"
    #     verbose_name_plural = "Теги"


class Ingredient(models.Model):
    """Ингридиент"""

    # наименование
    title = models.CharField(max_length=200, unique=True)
    # количество
    count = models.IntegerField(unique=True)
    # единица измерения
    unit = models.CharField(unique=True)


class Recipe(models.Model):
    """Рецепт"""
    
    # автор
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    # название 
    title = models.CharField(max_length=200, unique=True)
    # изображение
    image = 
    # описание
    description = models.TextField()
    # ингридиенты 
    ingredient = models.ManyToManyField() # множественный выбор из предустоновленного списка
    # теги (выбор  из предустоновленных)
    tags = models.ManyToManyField() # выбор из предуставновленных
    # время приготовления в минутах
    time_cook = models.IntegerField()
    
    

class Favorite(models.Model):
    """Избранное"""
    # пользователь
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    # рецепт
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    
class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        # verbose_name='Автор'
    )

