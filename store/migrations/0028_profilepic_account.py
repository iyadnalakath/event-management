# Generated by Django 4.1.5 on 2023-01-31 11:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0027_profilepic'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilepic',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
