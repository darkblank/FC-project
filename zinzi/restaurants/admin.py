from django.contrib import admin
from django_google_maps import fields as map_fields

from utils import widgets
from .models import Restaurant, ImageForRestaurant, ReservationInfo, Comment


class RestaurantAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {'widget': widgets.GoogleMapsAddressWidget},
    }


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(ImageForRestaurant)
admin.site.register(ReservationInfo)
admin.site.register(Comment)
