from django import forms
from .models import Reservation


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

    class Meta:
        model = Reservation
        fields = ['start_time', 'end_time', 'author', 'conference_room']