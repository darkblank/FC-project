from django.contrib import admin

from reservations.models import Payment, Reservation

admin.site.register(Payment)
admin.site.register(Reservation)
