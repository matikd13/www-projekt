from django.db import models

# Create your models here.
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Device(TimeStampedModel):
    mac_address = models.CharField(max_length=17, default='', blank=True)

    conference_room = models.OneToOneField('conferenceroom', on_delete=models.CASCADE, related_name='device', null=True, blank=True)

    def __str__(self):
        return self.mac_address

    @property
    def configured(self) -> bool:
        return hasattr(self, 'room')


class ConferenceRoom(TimeStampedModel):
    name = models.CharField(max_length=100, default='Name', blank=True)
    temperature = models.FloatField(default=0, blank=True)
    humidity = models.FloatField(default=0, blank=True)

    def __str__(self):
        return self.name + ' ' + str(self.temperature) + ' ' + str(self.humidity)

    @property
    def occupied(self) -> bool:
        return hasattr(self, 'device')

    @property
    def reserved_now(self) -> bool:
        return hasattr(self, 'reservation')

    @property
    def reserved_soon(self) -> bool:
        return hasattr(self, 'soon_reservation')


class Reservation(TimeStampedModel):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    conference_room = models.ForeignKey('conferenceroom', on_delete=models.CASCADE, related_name='reservations')

    def __str__(self):
        return self.author + ' ' + str(self.start_timedata) + ' ' + str(self.end_timedata)

