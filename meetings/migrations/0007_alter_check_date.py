# Generated by Django 4.2.17 on 2025-01-15 05:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0006_remove_meeting_duration_check_date_check_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='date',
            field=models.DateField(default=datetime.datetime(2025, 1, 15, 14, 28, 29, 198907)),
        ),
    ]
