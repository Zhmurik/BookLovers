# Generated by Django 4.2.14 on 2024-10-06 00:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book_check', '0010_rename_userbook_userbookinteraction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userbookinteraction',
            old_name='user_profile',
            new_name='profile',
        ),
    ]
