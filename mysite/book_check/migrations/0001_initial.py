# Generated by Django 4.1.5 on 2023-01-18 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(db_index=True, max_length=200, verbose_name='Book name')),
                ('author', models.CharField(max_length=200, verbose_name='Author')),
                ('year_published', models.CharField(max_length=30, verbose_name='Originally published')),
                ('genres', models.IntegerField(choices=[(1, 'Classics'), (2, 'Action and Adventure'), (3, 'Fantasy'), (4, 'Horror'), (5, 'Novel'), (6, 'Historical Fiction'), (7, 'Dystopian'), (8, 'Detective and Mystery')], verbose_name='Genres')),
                ('description', models.CharField(max_length=500, verbose_name='Book description')),
            ],
        ),
    ]
