# Generated by Django 3.2 on 2023-04-30 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20230428_0745'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'Ingredients', 'verbose_name_plural': 'Ингридиенты'},
        ),
        migrations.RenameField(
            model_name='recipe_ingredient',
            old_name='count',
            new_name='amount',
        ),
    ]
