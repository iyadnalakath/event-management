# Generated by Django 4.1.5 on 2023-01-30 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_popularity'),
    ]

    operations = [
        migrations.AddField(
            model_name='popularity',
            name='event_management_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='popularity',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
