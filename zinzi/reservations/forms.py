from django import forms

from reservations.models import Reservation, PaymentCancel
from restaurants.models import ReservationInfo


class ReservationForm(forms.ModelForm):
    def __init__(self, restaurant, date, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['information'].queryset = ReservationInfo.check_acceptable_time(restaurant.pk, date)

    class Meta:
        model = Reservation
        fields = (
            'information',
            'name',
            'party',
            'phone_number',
            'email',
        )


class PaymentCancelForm(forms.ModelForm):
    class Meta:
        model = PaymentCancel
        fields = (
            'reason',
        )
