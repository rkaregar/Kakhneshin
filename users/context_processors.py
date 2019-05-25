from .models import Member
from django.core.exceptions import ObjectDoesNotExist


def categories_processor(request):
    if request.user is not None and request.user.id is not None:
        members = Member.objects.filter(pk=request.user.id - 1)
        if len(members) > 0:
            return {'member': members.first()}

    return {}
