# Generated by Django 4.0.2 on 2022-03-03 09:11

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PostLike',
            new_name='Like',
        ),
    ]
