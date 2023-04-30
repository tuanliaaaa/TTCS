# Generated by Django 4.1.7 on 2023-04-25 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Entity', '0020_actor_actorfilm'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actorfilm',
            name='Film',
        ),
        migrations.AddField(
            model_name='actorfilm',
            name='Chapter',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Entity.chapter'),
        ),
    ]