# Generated by Django 4.1.6 on 2023-02-16 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0045_rename_profile_pic_service_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='profile',
        ),
    ]