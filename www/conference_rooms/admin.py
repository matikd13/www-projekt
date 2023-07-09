from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from www.conference_rooms.models import Device


class DeviceAdmin(ModelAdmin):
    list_display = ('mac_address',)


admin.site.register(Device, DeviceAdmin)
