# Generated by Django 4.1.7 on 2023-04-30 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Entity', '0025_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='HistoryView',
            field=models.DateTimeField(null=True),
        ),
    ]
