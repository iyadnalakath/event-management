# Generated by Django 4.1.5 on 2023-02-03 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectaccount', '0014_account_pin_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='district',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
