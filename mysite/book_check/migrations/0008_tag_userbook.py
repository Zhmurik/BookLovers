# Generated by Django 4.2.14 on 2024-09-07 00:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book_check', '0007_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_check.book')),
                ('tags', models.ManyToManyField(blank=True, to='book_check.tag')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_check.profile')),
            ],
        ),
    ]
