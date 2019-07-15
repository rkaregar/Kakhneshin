from django.contrib import admin

from .models import Reservation, ReservationComment

admin.site.register(Reservation)
admin.site.register(ReservationComment)


