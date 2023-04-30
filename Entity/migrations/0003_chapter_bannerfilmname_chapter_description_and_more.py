# Generated by Django 4.1.7 on 2023-04-13 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Entity', '0002_alter_chapter_film'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='BannerFilmName',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='chapter',
            name='Description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='chapter',
            name='TrailerFilm',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='film',
            name='BannerFilmName',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='film',
            name='FilmBollen',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AddField(
            model_name='film',
            name='TrailerFilm',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='film',
            name='Video',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='Film',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='Entity.film'),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='Video',
            field=models.TextField(),
        ),
    ]
