from django.core.exceptions import ValidationError

from Account.validator_utilities import validate_mobile_phone_handler, validate_username_handler, \
    validate_full_name_handler, validate_email_handler


def validate_username(value):
    has_errors = validate_username_handler(username=value).get("has_errors")
    message = validate_username_handler(username=value).get("message")
    code = validate_username_handler(username=value).get("code")

    if has_errors:
        raise ValidationError(message=message, code=code)


def validate_mobile_phone(value):
    has_errors = validate_mobile_phone_handler(mobile_phone=value).get("has_errors")
    message = validate_mobile_phone_handler(mobile_phone=value).get("message")
    code = validate_mobile_phone_handler(mobile_phone=value).get("code")

    if has_errors:
        raise ValidationError(message=message, code=code)


def validate_email(value):
    has_errors = validate_email_handler(email=value).get("has_errors")
    message = validate_email_handler(email=value).get("message")
    code = validate_email_handler(email=value).get("code")

    if has_errors:
        raise ValidationError(message=message, code=code)


def validate_full_name(value):
    has_errors = validate_full_name_handler(full_name=value).get("has_errors")
    message = validate_full_name_handler(full_name=value).get("message")
    code = validate_full_name_handler(full_name=value).get("code")

    if has_errors:
        raise ValidationError(message=message, code=code)
