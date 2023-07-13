from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.conf import settings

from www.conference_rooms.models import Device


class DeviceConsumer(JsonWebsocketConsumer):
    device = None

    def connect(self):
        for name, value in self.scope.get('headers', list()):
            name, value = name.decode(), value.decode()
            if name.lower() == 'authorization':
                if value == settings.WEBSOCKET_AUTH_TOKEN:
                    self.accept()
                    return
        self.close()

    def disconnect(self, close_code):
        if self.device and self.device.configured:
            async_to_sync(self.channel_layer.group_discard)(self.device.room.name, self.channel_name)

    def receive_json(self, content, *args):
        message_type = content.get('type')

        print(content)

        if message_type == 'init':
            mac_address = content.get('mac_address')
            self.device, created = Device.objects.get_or_create(mac_address=mac_address)
            if self.device and self.device.configured:
                async_to_sync(self.channel_layer.group_add)(self.device.room.name, self.channel_name)

        if self.device and self.device.configured:
            if message_type == 'presence':
                self.device.room.is_occupied = content.get('presence', False)
                self.device.room.save(update_fields=('is_occupied',))
            elif message_type == 'climate':
                self.device.room.humidity = float(content.get('hum', 0))
                self.device.room.temperature = float(content.get('temp', 0))
                self.device.room.save(update_fields=('humidity', 'temperature'))

    def room_info(self, event):
        self.send_json(event)
