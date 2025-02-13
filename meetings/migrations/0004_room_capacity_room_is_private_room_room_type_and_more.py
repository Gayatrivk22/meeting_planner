# Generated by Django 4.2.17 on 2025-01-15 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0003_meeting_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='capacity',
            field=models.IntegerField(default=10, help_text='Maximum number of people'),
        ),
        migrations.AddField(
            model_name='room',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='room',
            name='room_type',
            field=models.CharField(choices=[('SMALL', 'Small Meeting Room'), ('LARGE', 'Large Meeting Room'), ('CONF', 'Conference Room')], default='SMALL', max_length=10),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='duration',
            field=models.IntegerField(default=1, help_text='Duration in hours'),
        ),
    ]
