import string

import Account.models

slug_allowed_characters = string.ascii_letters + string.digits + "-" + "_"


def has_multiple_languages(value):
    persian_alphabet = "ءآأؤإئابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"

    has_english_chars = any(char in string.ascii_letters for char in value)
    has_persian_chars = any(char in persian_alphabet for char in value)

    return has_english_chars == has_persian_chars


def validate_mobile_phone_handler(mobile_phone, mobile_phone_exists_importance=True):
    has_errors = False
    message = None
    code = None

    mobile_phone_exists = Account.models.CustomUser.objects.filter(mobile_phone=mobile_phone).exists()

    if mobile_phone_exists_importance:
        if mobile_phone_exists:
            has_errors = True
            message = "این شماره تلفن از قبل ثبت شده است."
            code = "already_exists"

    if not mobile_phone.isnumeric():
        has_errors = True
        message = "شماره تلفن فقط میتواند از ارقام تشکیل شده باشد."
        code = "characters_not_allowed"

    elif len(mobile_phone) != 11:
        has_errors = True
        message = "شماره تلفن فقط میتواند 11 رقم داشته باشد."
        code = "not_exact_length"

    elif mobile_phone[0] != "0" or mobile_phone[1] != "9":
        has_errors = True
        message = "شماره تلفن نامعتبر است."
        code = "invalid_format"

    elif len(set(mobile_phone)) < 3:
        has_errors = True
        message = "شماره تلفن نامعتبر است."
        code = "invalid_format"

    return {"has_errors": has_errors, "message": message, "code": code}


def validate_username_handler(username, username_exists_importance=True):
    has_errors = False
    message = None
    code = None

    username_exists = Account.models.CustomUser.objects.filter(username=username).exists()

    if username_exists_importance:
        if username_exists:
            has_errors = True
            message = "این نام کاربری قبلا  ثبت شده است."
            code = "already_exists"

    if len(username) < 5:
        has_errors = True
        message = "نام کاربری نمی‌تواند کمتر از 5 کاراکتر داشته باشد."
        code = "length_is_low"

    elif username.isnumeric():
        has_errors = True
        message = "نام کاربری باید حداقل یک حرف انگلیسی داشته باشد."
        code = "at_least_one_letter"

    for character_checker in username:
        if character_checker not in slug_allowed_characters:
            has_errors = True
            message = "این نام کاربری قابل قبول نیست."
            code = "disallowed_characters"
            break

    return {"has_errors": has_errors, "message": message, "code": code}


def validate_passwords_handler(password, password_repeat):
    has_errors = False
    message = None
    code = None

    if password and password_repeat and password != password_repeat:
        has_errors = True
        message = "رمز عبورها با یکدیگر هم‌خوانی ندارند."
        code = "passwords_do_not_match"

    elif len(password) < 4:
        has_errors = True
        message = "رمز عبور باید حداقل 4 کاراکتر داشته باشد."
        code = "length_is_low"

    return {"has_errors": has_errors, "message": message, "code": code}


def validate_full_name_handler(full_name):
    has_errors = False
    message = None
    code = None

    if len(full_name) < 4:
        has_errors = True
        message = "نام و نام خانوادگی باید حداقل 4 حرف داشته باشد."
        code = "length_is_low"

    elif not full_name.replace(" ", "").isalpha():
        has_errors = True
        message = "نام و نام خانوادگی نمی‌تواند شامل رقم باشد."
        code = "digits_not_allowed"

    elif has_multiple_languages(value=full_name):
        has_errors = True
        message = "نام و نام خانوادگی می‌تواند شامل یک زبان باشد."
        code = "only_1_language"

    return {"has_errors": has_errors, "message": message, "code": code}


def validate_email_handler(email):
    has_errors = False
    message = None
    code = None

    email_exists = Account.models.CustomUser.objects.filter(email=email).exists()

    if email_exists:
        has_errors = True
        message = "این آدرس ایمیل قبلا ثبت شده است."
        code = "already_exists"

    return {"has_errors": has_errors, "message": message, "code": code}
