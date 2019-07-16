from django.contrib import admin

from places.models import Place, DistanceHabitatToPlace, PlaceComment, PlaceCommentPhoto, PlaceCommentVideo

admin.site.register(Place)
admin.site.register(DistanceHabitatToPlace)
admin.site.register(PlaceComment)
admin.site.register(PlaceCommentPhoto)
admin.site.register(PlaceCommentVideo)
