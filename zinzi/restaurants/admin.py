from django.contrib import admin

from .models import Restaurant, Menu, ImageForRestaurant, ReservationTable, ReservationInfo

admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(ImageForRestaurant)
admin.site.register(ReservationTable)
admin.site.register(ReservationInfo)
