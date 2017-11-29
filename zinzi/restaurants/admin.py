from django.contrib import admin
from django_google_maps import fields as map_fields
from django_google_maps import widgets as map_widgets

from .models import Restaurant, Menu, ImageForRestaurant, ReservationTable, ReservationInfo


class RestaurantAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Menu)
admin.site.register(ImageForRestaurant)
admin.site.register(ReservationTable)
admin.site.register(ReservationInfo)
