from django.contrib import admin

from .models import Reservation, ReservationComment, ReservationCommentPhoto, ReservationCommentVideo

admin.site.register(Reservation)
admin.site.register(ReservationComment)
admin.site.register(ReservationCommentPhoto)
admin.site.register(ReservationCommentVideo)


