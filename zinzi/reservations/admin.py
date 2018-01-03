from django.contrib import admin

from reservations.models import Payment, Reservation, PaymentCancel

admin.site.register(Payment)
admin.site.register(Reservation)
admin.site.register(PaymentCancel)
