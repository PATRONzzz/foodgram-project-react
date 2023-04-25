from django.db import models
from users.models import CustomUser


class Tag(models.Model):
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
    # единица измерения
    unit = models.CharField(max_length=200, unique=True)


class Recipe(models.Model):
    """Рецепт"""

    # автор
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    # название
    title = models.CharField(max_length=200, unique=True)
    # изображение
    image = models.ImageField(
        "Картинка",
        upload_to="recipes/",
        blank=True,
    )
    # дата публикации
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    # описание
    description = models.TextField()
    # ингридиенты
    ingredient = models.ManyToManyField(
        Ingredient,
        through="Recipe_ingredient",
        through_fields=("recipe", "ingredient"),
        verbose_name="Ингредиенты",
    )  # множественный выбор из предустоновленного списка
    # теги
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Теги",
    )  # выбор из предуставновленных
    # время приготовления в минутах
    time_cook = models.IntegerField()

    # class Meta:
    #     # сортировка
    #     pass


class Recipe_ingredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredients",
        verbose_name="Ингредиент",
    )
    count = models.IntegerField()


class Favorite(models.Model):
    """Избранное"""

    # пользователь
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    # рецепт
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )


class Subscribe(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="subscriber",
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="autors",
        # verbose_name='Автор'
    )


class Shopping_card(models.Model):
    """Корзина"""

    # пользователь
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="cards",
    )
    # рецепт
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
