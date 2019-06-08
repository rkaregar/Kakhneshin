from django import template

register = template.Library()


@register.filter(name='group_by')
def group_by(objects, count=1):
    ret = []
    for i in range(0, len(objects), count):
        ret.append(objects[i:i + count])
    return ret


@register.filter(name='add_str')
def add_str(objects, s=''):
    objects=list(objects)
    objects.append(s)
    return objects
