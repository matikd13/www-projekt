from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import Reservation, ConferenceRoom
from .serializers import ReservationSerializer
from .forms import ReservationForm
import json
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


def main_view(request):
    reservations = Reservation.objects.all()
    rooms = ConferenceRoom.objects.all()

    return render(request, 'main.html', {'reservations': reservations, 'rooms': rooms})


def create_reservations(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()  # Zapisz dane formularza do modelu
            return redirect('main')  # Przekieruj na stronę główną po zapisie
    else:
        form = ReservationForm()
    return render(request, 'create_reservation.html', {'form': form})


def room_status(request):
    rooms = ConferenceRoom.objects.all().order_by('id')
    room_statuses = []

    for i, room in enumerate(rooms, start=1):
        print(f"Room {room.id} status: {room.status}")  # debug
        room_statuses.append({
            "room_id_z_bazy": room.id,
            "room_id": i,
            "room_name": room.name,
            "status": room.status,
        })
        room.notify_device()

    data = json.dumps(room_statuses, indent=4)
    return HttpResponse(data, content_type='application/json')


def reserve_room(request, room_name):
    room = get_object_or_404(ConferenceRoom, name=room_name)
    reservations = room.reservations.filter(end_time__gt=timezone.now()).order_by('start_time')

    if 'delete_reservation' in request.POST:
        reservation_id = request.POST.get('reservation_id')
        reservation = get_object_or_404(Reservation, id=reservation_id)
        reservation.delete()
        messages.success(request, "Rezerwacja została pomyślnie usunięta!")
        return redirect('reserve_room', room_name=room_name)

    if request.method == 'POST':
        form = ReservationForm(request.POST, initial={'conference_room': room})
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.conference_room = room
            reservation.save()
            return redirect('main')
    else:
        form = ReservationForm(initial={'conference_room': room})
        for field_name in form.fields:
            form.fields[field_name].widget.attrs.update({
                'class': 'form-control' + (' is-invalid' if form[field_name].errors else '')
            })
    return render(request, 'reserve_room.html', {'room': room, 'form': form, 'reservations': reservations})
