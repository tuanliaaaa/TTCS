# Generated by Django 4.1.7 on 2023-04-19 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Entity', '0011_alter_categoryfilm_category_alter_categoryfilm_film_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='WatchedTime',
            field=models.FloatField(null=True),
        ),
    ]
