# Generated by Django 4.2.17 on 2025-01-16 00:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0010_remove_check_room_alter_check_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='check',
            name='room_type',
        ),
        migrations.RemoveField(
            model_name='room',
            name='room_type',
        ),
        migrations.AddField(
            model_name='check',
            name='required_amenities',
            field=models.JSONField(default=list, help_text='List of required amenities'),
        ),
        migrations.AddField(
            model_name='room',
            name='amenities',
            field=models.JSONField(default=list, help_text='List of amenities available in the room'),
        ),
        migrations.AlterField(
            model_name='check',
            name='capacity',
            field=models.IntegerField(default=2, help_text='Number of people'),
        ),
        migrations.AlterField(
            model_name='check',
            name='date',
            field=models.DateField(default=datetime.datetime(2025, 1, 16, 9, 33, 13, 737704)),
        ),
    ]
