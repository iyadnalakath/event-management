# Generated by Django 4.1.6 on 2023-02-14 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0037_alter_rating_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='name',
            new_name='user',
        ),
    ]