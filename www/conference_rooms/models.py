from django.db import models

# Create your models here.
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Device(TimeStampedModel):
    mac_address = models.CharField(max_length=17, default='', blank=True)

    def __str__(self):
        return self.mac_address

    @property
    def configured(self) -> bool:
        return hasattr(self, 'room')
