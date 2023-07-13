from django.shortcuts import render, redirect

# Create your views here.
from rest_framework import viewsets
from .models import Reservation
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
