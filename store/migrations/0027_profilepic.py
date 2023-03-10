# Generated by Django 4.1.5 on 2023-01-31 11:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_remove_popularity_event_management_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfilePic',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('auto_id', models.PositiveIntegerField(db_index=True, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('profile_pic', models.ImageField(blank=True, default='', null=True, upload_to='mediafiles')),
                ('more_photos', models.ImageField(blank=True, default='', null=True, upload_to='mediafiles')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
