from django import forms

from reservations.models import Reservation
from restaurants.models import ReservationInfo


class ReservationForm(forms.ModelForm):
    def __init__(self, restaurant, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['information'].queryset = ReservationInfo.objects.filter(restaurant=restaurant)

    class Meta:
        model = Reservation
        fields = (
            'information',
            'name',
            'party',
            'phone_number',
            'email',
        )
