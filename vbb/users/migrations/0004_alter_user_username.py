# Generated by Django 4.0.3 on 2022-05-05 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, error_messages={'unique': 'A user with that username already exists.'}, max_length=150, null=True, unique=True, verbose_name='username'),
        ),
    ]
