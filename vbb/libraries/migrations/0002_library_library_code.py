# Generated by Django 4.0.3 on 2022-04-15 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='library',
            name='library_code',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
