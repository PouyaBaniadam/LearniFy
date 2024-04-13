import string

from django.core.exceptions import ValidationError


def english_language_validator(value):
    allowed_characters = string.ascii_letters + string.digits + "-_+"

    if any(value not in allowed_characters for value in value):
        raise ValidationError('فقط انگلیسی مجاز است.')
