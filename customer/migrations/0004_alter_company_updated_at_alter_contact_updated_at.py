# Generated by Django 5.1 on 2024-08-12 06:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_company_updated_at_contact_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='contact',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]