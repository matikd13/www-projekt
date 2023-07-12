from django.db import models

# Create your models here.
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Device(TimeStampedModel):
    mac_address = models.CharField(max_length=17, default='', blank=True)

    # TODO: add relation to conference room one to one
    # room = models.OneToOneField(Conference_Room, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.mac_address

    @property
    def configured(self) -> bool:
        return hasattr(self, 'room')


class Conference_Room(TimeStampedModel):
    name = models.CharField(max_length=100, default='Name', blank=True)
    temperature = models.FloatField(default=0, blank=True)
    humidity = models.FloatField(default=0, blank=True)

    # TODO: add relation to device one to one
    # device = models.OneToOneField(Device, on_delete=models.CASCADE, null=True, blank=True)

    # TODO: add relation to reservation many conference rooms to one reservation (many to one)
    # reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True, blank=True)
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
    start_timedata = models.DateTimeField()
    end_timedata = models.DateTimeField()
    author = models.CharField(max_length=100, default='Author', blank=True)

    # TODO: add relation to conference room one reservation to many rooms (many to one)
    # room = models.ForeignKey(Conference_Room, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.author + ' ' + str(self.start_timedata) + ' ' + str(self.end_timedata)

