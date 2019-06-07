from django.contrib import admin
from .models import Habitat, RoomType, Room, RoomOutOfService

# Register your models here.
admin.site.register(Habitat)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(RoomOutOfService)
