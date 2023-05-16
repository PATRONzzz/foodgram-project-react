from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.html import format_html
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
    color = models.CharField(
        "Цвет",
        max_length=7,
        unique=True,
        validators=[
            RegexValidator(
                '^#([a-fA-F0-9]{6})',
                message='Не верный формат цвета.'
            )
        ]
    )
    # slug
    slug = models.SlugField(
        "Слаг",
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ингридиент"""

    # наименование
    name = models.CharField(
        "Название",
        max_length=200,
        unique=True,
        )
    # единица измерения
    measurement_unit = models.CharField(
        "Единица измерения",
        max_length=200,
        )

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}"

    class Meta:
        verbose_name = "ингридиент"
        verbose_name_plural = "ингридиенты"


class Recipe(models.Model):
    """Рецепт"""

    # автор
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="автор",
    )
    # название
    name = models.CharField(
        "Название",
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
    text = models.TextField("Описание")
    # ингридиенты
    ingredients = models.ManyToManyField(
        Ingredient,
        through="Recipe_ingredient",
        through_fields=("recipe", "ingredient"),
        verbose_name="ингредиенты",
    )
    # теги
    tags = models.ManyToManyField(
        Tag,
        verbose_name="тег",
        
    )
    # время приготовления в минутах
    cooking_time = models.IntegerField(
        "Время приготовления",
        validators=(MinValueValidator(1),),
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name_plural = "рецепты"


class Recipe_ingredient(models.Model):
    # рецепты
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_ingredient",
        verbose_name="рецепт",
    )
    # ингридиенты
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="recipe_ingredient",
        verbose_name="ингредиенты",
    )
    # количество
    amount = models.IntegerField(
        "Количество",
        validators=(MinValueValidator(1),),
    )

    class Meta:
        verbose_name = "Ingredients in the recipe"
        verbose_name_plural = "Ингредиенты в рецептах"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_ingredient_recipe",
            )
        ]


class Favorite(models.Model):
    """Избранное"""

    # пользователь
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorite_user',
    )
    # рецепт
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
    )

    class Meta:
        verbose_name = "избранное"
        verbose_name_plural = "избранное"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_favorite",
            )
        ]


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
        verbose_name="автор",
    )


class ShopCart(models.Model):
    """Корзина"""

    # пользователь
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="carts",
    )
    # рецепт
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopcart_recipe",
    )

    class Meta:
        verbose_name = "корзина"
        verbose_name_plural = "списки покупок"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_shopping_cart"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.recipe.name}"
