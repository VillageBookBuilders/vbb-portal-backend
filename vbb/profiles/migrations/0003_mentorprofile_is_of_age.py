# Generated by Django 4.0.3 on 2022-04-08 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentorprofile',
            name='is_of_age',
            field=models.BooleanField(default=False),
        ),
    ]