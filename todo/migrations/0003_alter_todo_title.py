# Generated by Django 5.0.4 on 2024-05-03 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_todo_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='title',
            field=models.CharField(max_length=150),
        ),
    ]
