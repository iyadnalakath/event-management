# Generated by Django 4.1.5 on 2023-01-31 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectaccount', '0006_alter_account_work_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='profile_pic',
        ),
    ]
