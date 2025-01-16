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
    
    # Room types will be determined automatically based on capacity
    ROOM_TYPES = [
        ('SMALL', 'Small Meeting Room (2 or less people)'),
        ('LARGE', 'Large Meeting Room (3-10 people)'),
        ('CONF', 'Conference Room (11+ people)'),
    ]
    
    # Amenities
    AMENITIES = [
        ('PROJ', 'Projector'),
        ('TV', 'TV Screen'),
        ('WHBD', 'Whiteboard'),
        ('VC', 'Video Conferencing'),
        ('PHONE', 'Conference Phone'),
        ('COFFEE', 'Coffee Machine'),
        ('WATER', 'Water Dispenser'),
    ]
    amenities = models.JSONField(default=list, help_text="List of amenities available in the room")
    
    @property
    def room_type(self):
        if self.capacity <= 2:
            return 'SMALL'
        elif self.capacity <= 10:
            return 'LARGE'
        else:
            return 'CONF'
            
    @property
    def room_type_display(self):
        return dict(self.ROOM_TYPES)[self.room_type]
    
    def __str__(self):
        return f"{self.name} on floor {self.floor}: room no. {self.room_number}"
    

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
    capacity = models.IntegerField(default=2, help_text="Number of people")
    is_private = models.BooleanField(default=False)
    required_amenities = models.JSONField(default=list, help_text="List of required amenities")

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
    def find_available_rooms(date, start_time, end_time, capacity, is_private, required_amenities):
        """Find available rooms that match requirements"""
        # Get all rooms that meet basic requirements
        rooms = Room.objects.filter(
            capacity__gte=capacity,
            is_private=is_private
        )
        
        # Filter rooms by required amenities
        if required_amenities:
            rooms = [room for room in rooms if all(amenity in room.amenities for amenity in required_amenities)]
        
        # Check each room's availability
        available_rooms = []
        for room in rooms:
            if Check.is_available(room, date, start_time, end_time):
                available_rooms.append(room)
                
        return available_rooms
