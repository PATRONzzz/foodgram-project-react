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
    measurement_unit = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f"{self.name}, {self.unit}"

    class Meta:
        verbose_name = "Ingredients"
        verbose_name_plural = "Ингридиенты"


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
    ingredient = models.ManyToManyField(
        Ingredient,
        through="Recipe_ingredient",
        through_fields=("recipe", "ingredient"),
        verbose_name="Ингредиент",
    )  # множественный выбор из предустоновленного списка
    # теги
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Tegs",
    )  # выбор из предуставновленных
    # время приготовления в минутах
    time_cook = models.IntegerField()

    class Meta:
        ordering = ["-pub_date"]


class Recipe_ingredient(models.Model):
    # рецепты
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Рецепт",
    )
    # ингридиенты
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredients",
        verbose_name="Ингредиенты",
    )
    # количество
    amount = models.IntegerField(
        "Количество",
        validators=(MinValueValidator(1),),
    )
    # дата публикации
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True,
    )

    class Meta:
        ordering = ("-pub_date",)


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
