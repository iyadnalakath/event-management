# Generated by Django 4.1.5 on 2023-01-31 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectaccount', '0010_account_more_photos_account_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='more_photos',
        ),
        migrations.RemoveField(
            model_name='account',
            name='profile_pic',
        ),
    ]
