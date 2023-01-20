# Generated by Django 4.1.5 on 2023-01-20 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_remove_subcatagory_catagory_service_account_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='is_featured',
        ),
        migrations.RemoveField(
            model_name='service',
            name='rating',
        ),
        migrations.AddField(
            model_name='service',
            name='service_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
