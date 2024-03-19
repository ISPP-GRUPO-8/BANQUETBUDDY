# Generated by Django 4.2.7 on 2024-03-18 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Particular',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='ParticularUsername', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('preferences', models.TextField(blank=True)),
                ('address', models.TextField(blank=True)),
                ('is_subscribed', models.BooleanField(default=False)),
            ],
        ),
    ]
