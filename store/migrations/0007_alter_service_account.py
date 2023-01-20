# Generated by Django 4.1.5 on 2023-01-20 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0006_rename_event_team_service_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='event_team', to=settings.AUTH_USER_MODEL),
        ),
    ]
