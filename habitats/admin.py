from django.contrib import admin
from .models import Habitat, RoomType, RoomOutOfService

admin.site.register(Habitat)
admin.site.register(RoomType)
admin.site.register(RoomOutOfService)
