from django import forms
from .models import Reservation, ConferenceRoom
from django.utils import timezone


class ReservationForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
        })
    )
    end_time = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
        })
    )

    conference_room = forms.ModelChoiceField(queryset=ConferenceRoom.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control',
        'id': 'id_author'  # Przypisanie identyfikatora 'id_author' do pola wyboru autora
    }))

    class Meta:
        model = Reservation
        fields = ['start_time', 'end_time', 'author', 'conference_room']

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        conference_room = cleaned_data.get('conference_room')

        if start_time and end_time and conference_room:
            conflicting_reservations = Reservation.objects.filter(conference_room=conference_room,
                                                                  start_time__lte=end_time,
                                                                  end_time__gte=start_time,
                                                                  ).exclude(
                pk=self.instance.pk)  # Wyklucz bieżącą rezerwację, jeśli edytujemy
            if conflicting_reservations:
                raise forms.ValidationError("Ta sala jest już zarezerwowana w tym terminie.")

        if start_time >= end_time:
            raise forms.ValidationError("Czas rozpoczęcia musi być wcześniejszy niż czas zakończenia.")

        if start_time < timezone.now():
            raise forms.ValidationError("Nie można zarezerwować sali w przeszłości.")
