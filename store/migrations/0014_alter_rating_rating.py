# Generated by Django 4.1.5 on 2023-01-27 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_rating_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
