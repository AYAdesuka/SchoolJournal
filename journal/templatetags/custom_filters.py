from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_grade(grade_map, args):

    if not grade_map:
        return ""
    try:
        student_id, gradebook_id = args.split(',')
        key = f"{student_id}_{gradebook_id}"
        return grade_map.get(key, "")
    except (ValueError, AttributeError):
        return ""

@register.simple_tag
def active_grade(grade_map, student_id, gradebook_id):
    key = f"{student_id}_{gradebook_id}"
    return grade_map.get(key, "")

@register.filter(name='dict_get')
def dict_get(dictionary, key):
    if dictionary:
        return dictionary.get(key, {'subject_id': None, 'room': ''})
    return {'subject_id': None, 'room': ''}