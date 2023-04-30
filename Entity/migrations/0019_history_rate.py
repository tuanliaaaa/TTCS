# Generated by Django 4.1.7 on 2023-04-24 10:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Entity', '0018_alter_chapter_chapterdescription_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='Rate',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]