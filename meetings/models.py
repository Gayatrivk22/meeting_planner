from datetime import time, datetime, timedelta
from django.contrib.auth import get_user_model
from django.db import models


class Room(models.Model):
    # Basic room information
    name = models.CharField(max_length=50)
    floor = models.IntegerField()
    room_number = models.IntegerField()
    capacity = models.IntegerField(default=10, help_text="Maximum number of people")
    is_private = models.BooleanField(default=False)
    ROOM_TYPES = [
        ('SMALL', 'Small Meeting Room'),
        ('LARGE', 'Large Meeting Room'),
        ('CONF', 'Conference Room'),
    ]
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES, default='SMALL')
    

class Meeting(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField(default=time(9))
    end_time = models.TimeField(default=time(10))
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    participants = models.ManyToManyField(get_user_model())
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} at {self.start_time} on {self.date}"


class Check(models.Model):
    # Room requirements
    capacity = models.IntegerField(default=10, help_text="Maximum number of people")
    is_private = models.BooleanField(default=False)
    room_type = models.CharField(max_length=10, choices=Room.ROOM_TYPES, default='SMALL')

    # Time requirements
    date = models.DateField(default=datetime.today())
    start_time = models.TimeField(default=time(9))
    end_time = models.TimeField(default=time(10))

    @staticmethod
    def is_available(room, date, start_time, end_time):
        """Check if room is available for given time slot"""
        meetings = Meeting.objects.filter(
            room=room,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        return not meetings.exists()
    
    @staticmethod
    def find_available_rooms(date, start_time, end_time, capacity, room_type, is_private):
        """Find available rooms that match requirements"""
        # Get all rooms that meet basic requirements
        rooms = Room.objects.filter(
            capacity__gte=capacity,
            room_type=room_type,
            is_private=is_private
        )
        
        # Check each room's availability
        available_rooms = []
        for room in rooms:
            if Check.is_available(room, date, start_time, end_time):
                available_rooms.append(room)
                
        return available_rooms
