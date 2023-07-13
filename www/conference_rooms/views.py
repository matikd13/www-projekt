from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from rest_framework import viewsets
from .models import Reservation, ConferenceRoom
from .serializers import ReservationSerializer
from .forms import ReservationForm
from django.http import JsonResponse
from .models import ConferenceRoom
from django.shortcuts import get_object_or_404
import json
from django.http import HttpResponse


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


def main_view(request):
    reservations = Reservation.objects.all()
    rooms = ConferenceRoom.objects.all()
    names = []
    for room in rooms:
        names.append(room.name)
    return render(request, 'main.html', {'reservations': reservations, 'rooms': rooms, 'names': names})


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

    data = json.dumps(room_statuses, indent=4)
    return HttpResponse(data, content_type='application/json')


def reserve_room(request, room_name):
    room = get_object_or_404(ConferenceRoom, name=room_name)
    if request.method == 'POST':
        form = ReservationForm(request.POST, initial={'conference_room': room})
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.conference_room = room
            reservation.save()
            return redirect('main')
        return render(request, 'reserve_room.html', {'room': room, 'form': form})
    else:
        form = ReservationForm(initial={'conference_room': room})
        form.fields['conference_room'].disabled = True
    return render(request, 'reserve_room.html', {'room': room, 'form': form})
