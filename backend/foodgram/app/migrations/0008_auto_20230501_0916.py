# Generated by Django 3.2 on 2023-05-01 09:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_rename_description_recipe_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='time_cook',
            new_name='cooking_time',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredient',
            field=models.ManyToManyField(through='app.Recipe_ingredient', to='app.Ingredient', verbose_name='Ингредиент'),
        ),
        migrations.AlterField(
            model_name='recipe_ingredient',
            name='amount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество'),
        ),
    ]
