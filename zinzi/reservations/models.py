from django.db import models


# fixme
class Reservation(models.Model):
    requested_date = models.DateTimeField(
        auto_now_add=True,
    )
    reserved_date = models.DateTimeField()
    payment_date = models.DateTimeField()
    price = models.PositiveIntegerField(
        max_length=8,
    )
    party = models.PositiveIntegerField()
    reservation_number = models.PositiveIntegerField(
        unique=True,
        max_length=14,
    )
    is_confirmed = models.BooleanField(
        default=False,
    )
