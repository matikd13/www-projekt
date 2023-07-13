# Create your models here.
from django.db import models
from django_extensions.db.models import TimeStampedModel
from datetime import timezone


class ConferenceRoom(TimeStampedModel):
    name = models.CharField(max_length=100, default='Name', blank=True)
    temperature = models.FloatField(default=0, blank=True)
    humidity = models.FloatField(default=0, blank=True)

    def __str__(self):
        return self.name

    @property
    def occupied(self):
        now = timezone.now()
        return self.reservations.filter(start_time__lte=now, end_time__gte=now).exists()

    @property
    def reserved_now(self) -> bool:
        return hasattr(self, 'reservation')

    @property
    def reserved_soon(self):
        in_one_hour = timezone.now() + timezone.timedelta(hours=1)
        return self.reservations.filter(start_time__lte=in_one_hour).exists()


class Device(TimeStampedModel):
    mac_address = models.CharField(max_length=17, default='', blank=True)

    conference_room = models.OneToOneField(ConferenceRoom, on_delete=models.CASCADE, related_name='device', null=True,
                                           blank=True)

    def __str__(self):
        return self.mac_address

    @property
    def configured(self) -> bool:
        return hasattr(self, 'room')


class Reservation(TimeStampedModel):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    conference_room = models.ForeignKey(ConferenceRoom, on_delete=models.CASCADE, related_name='reservations')

    def __str__(self):
        return f"{self.author} {self.start_time} {self.end_time}"
