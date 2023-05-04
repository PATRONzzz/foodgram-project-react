from django.core.validators import MinValueValidator
from django.db import models
from users.models import CustomUser


class Tag(models.Model):
    """Тег"""

    # наименование
    name = models.CharField(
        "Название",
        max_length=200,
        unique=True,
    )
    # цветовой Hex-код
    color = models.CharField(max_length=7, unique=True)
    # slug
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = "Tegs"
        verbose_name_plural = "Теги"


class Ingredient(models.Model):
    """Ингридиент"""

    # наименование
    name = models.CharField(max_length=200, unique=True)
    # единица измерения
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}"

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ингридиент"


class Recipe(models.Model):
    """Рецепт"""

    # автор
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    # название
    name = models.CharField(
        max_length=200,
        unique=True,
    )
    # изображение
    image = models.ImageField(
        "Картинка",
        upload_to="recipes/",
        blank=True,
    )
    # дата публикации
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    # описание
    text = models.TextField()
    # ингридиенты
    ingredients = models.ManyToManyField(
        Ingredient,
        through="Recipe_ingredient",
        through_fields=("recipe", "ingredient"),
        verbose_name="Ингредиенты",
    )
    # теги
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Tags",
    )
    # время приготовления в минутах
    cooking_time = models.IntegerField()

    class Meta:
        ordering = ("-pub_date",)
        verbose_name_plural = "Рецепты"


class Recipe_ingredient(models.Model):
    # рецепты
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_ingredient",
        verbose_name="Рецепт",
    )
    # ингридиенты
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="recipe_ingredient",
        verbose_name="Ингредиенты",
    )
    # количество
    amount = models.IntegerField(
        # "Количество",
        validators=(MinValueValidator(1),),
    )

    def __str__(self):
        return (
            f"{self.recipe.name}: "
            f"{self.ingredient.name} - "
            f"{self.amount} "
            f"{self.ingredient.measurement_unit}"
        )


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
    # пользователь
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="subscriber",
    )
    # автор
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="autors",
        # verbose_name='Автор'
    )


class ShopCard(models.Model):
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
