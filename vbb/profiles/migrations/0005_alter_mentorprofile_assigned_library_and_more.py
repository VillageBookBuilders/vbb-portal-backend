# Generated by Django 4.0.3 on 2022-04-15 00:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0002_library_library_code'),
        ('profiles', '0004_studentprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentorprofile',
            name='assigned_library',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='libraries.library'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='assigned_library',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='libraries.library'),
        ),
    ]
