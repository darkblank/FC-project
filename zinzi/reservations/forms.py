from django import forms

from reservations.models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = (
            'information',
            'name',
            'party',
            'phone_number',
            'email',
        )
