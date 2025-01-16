from django.core.management.base import BaseCommand
from meetings.models import Room

class Command(BaseCommand):
    help = 'Sets up default amenities for rooms based on their type'

    def handle(self, *args, **kwargs):
        # Update small rooms
        Room.objects.filter(capacity__lte=2).update(
            amenities=['WHBD', 'PHONE', 'WATER']  # Basic amenities for small rooms
        )

        # Update large rooms
        Room.objects.filter(capacity__gt=2, capacity__lte=10).update(
            amenities=['PROJ', 'WHBD', 'PHONE', 'WATER', 'COFFEE']  # More amenities for large rooms
        )

        # Update conference rooms
        Room.objects.filter(capacity__gt=10).update(
            amenities=['PROJ', 'TV', 'WHBD', 'VC', 'PHONE', 'COFFEE', 'WATER']  # All amenities for conference rooms
        )

        self.stdout.write(self.style.SUCCESS('Successfully updated room amenities'))
