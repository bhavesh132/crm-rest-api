# Generated by Django 5.1 on 2024-10-27 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='updated_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='contact',
            name='updated_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='newsfeed',
            name='updated_at',
            field=models.DateTimeField(),
        ),
    ]
