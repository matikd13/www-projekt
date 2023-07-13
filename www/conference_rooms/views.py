from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from rest_framework import viewsets
from .models import Reservation, ConferenceRoom
from .serializers import ReservationSerializer
from .forms import ReservationForm


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


def main_view(request):
    reservations = Reservation.objects.all()
    grid_range = list(range(48))
    return render(request, 'main.html', {'reservations': reservations, 'grid_range': grid_range})


def create_reservations(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()  # Zapisz dane formularza do modelu
            return redirect('main')  # Przekieruj na stronę główną po zapisie
    else:
        form = ReservationForm()
    return render(request, 'create_reservation.html', {'form': form})


def reserve_room(request, room_id):
    room = get_object_or_404(ConferenceRoom, id=room_id)
    form = ReservationForm(initial={'conference_room': room})
    form.fields['conference_room'].disabled = True
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.conference_room = room
            reservation.save()
            return redirect('main')
    else:
        form = ReservationForm()
    return render(request, 'reserve_room.html', {'room': room, 'form': form})