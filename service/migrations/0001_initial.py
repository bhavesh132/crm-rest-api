# Generated by Django 5.1 on 2024-09-02 05:31

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SubType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('num_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.TextField(max_length=100)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_modifier', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('num_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255)),
                ('subject', models.TextField(choices=[('email', 'Email'), ('call', 'Call'), ('other', 'Other')], max_length=100)),
                ('status', models.TextField(choices=[('completed', 'Completed'), ('in-progress', 'In Progress'), ('new', 'New'), ('cancelled', 'Cancelled')], max_length=50)),
                ('priority', models.TextField(choices=[('p1', 'P1'), ('p2', 'P2'), ('p3', 'P3'), ('p4', 'P4')], default='p2', max_length=20)),
                ('due_date', models.DateField(default=django.utils.timezone.now)),
                ('comments', models.TextField(null=True)),
                ('contact_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.contact')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_modifier', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('num_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('due_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('new', 'New'), ('assigned', 'Assigned'), ('in-progress', 'In-Progress'), ('completed', 'Completed'), ('closed', 'Closed'), ('needs-review', 'Needs Review'), ('cancelled', 'Cancelled')], max_length=50)),
                ('priority', models.TextField(choices=[('p1', 'P1'), ('p2', 'P2'), ('p3', 'P3'), ('p4', 'P4')], default='p2', max_length=20)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('customer_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.contact')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_modifier', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_owner', to=settings.AUTH_USER_MODEL)),
                ('ticket_subtype', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.subtype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('num_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('body', models.TextField()),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_modifier', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_owner', to=settings.AUTH_USER_MODEL)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.ticket')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('num_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.TextField(max_length=50)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_modifier', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.type'),
        ),
        migrations.AddField(
            model_name='subtype',
            name='type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.type'),
        ),
    ]
