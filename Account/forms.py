from django import forms
from django.core.exceptions import ValidationError

from Account.models import CustomUser
from Account.validator_utilities import validate_mobile_phone_handler, validate_username_handler, \
    validate_passwords_handler


class OTPRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور")
    password_repeat = forms.CharField(widget=forms.PasswordInput, label="تکرار رمز عبور")

    class Meta:
        model = CustomUser
        fields = ("username", "mobile_phone", "password", "password_repeat")

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data.get("mobile_phone")

        has_errors = validate_mobile_phone_handler(mobile_phone=mobile_phone).get("has_errors")
        message = validate_mobile_phone_handler(mobile_phone=mobile_phone).get("message")
        code = validate_mobile_phone_handler(mobile_phone=mobile_phone).get("code")

        if has_errors:
            raise ValidationError(message=message, code=code)
        else:
            return mobile_phone

    def clean_username(self):
        username = self.cleaned_data.get("username")

        has_errors = validate_username_handler(username=username).get("has_errors")
        message = validate_username_handler(username=username).get("message")
        code = validate_username_handler(username=username).get("code")

        if has_errors:
            raise ValidationError(message=message, code=code)
        else:
            return username

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")

        has_errors = validate_passwords_handler(password=password, password_repeat=password_repeat).get("has_errors")
        message = validate_passwords_handler(password=password, password_repeat=password_repeat).get("message")
        code = validate_passwords_handler(password=password, password_repeat=password_repeat).get("code")

        if has_errors:
            raise ValidationError(message=message, code=code)


class RegularLogin(forms.Form):
    mobile_phone_or_username = forms.CharField(max_length=75, widget=forms.TextInput(),
                                               label="شماره تفلن یا نام کاربری")
    password = forms.CharField(
        widget=forms.PasswordInput(), label="رمز عبور")

    def clean(self):
        mobile_phone_or_username = self.cleaned_data.get("mobile_phone_or_username")

        mobile_phone = username = None

        if mobile_phone_or_username.isdigit():
            mobile_phone = mobile_phone_or_username
            field_name = "mobile_phone"

        else:
            username = mobile_phone_or_username
            field_name = "username"

        try:
            if field_name == "mobile_phone":
                CustomUser.objects.get(mobile_phone=mobile_phone_or_username)

                has_errors = validate_mobile_phone_handler(mobile_phone=mobile_phone,
                                                           mobile_phone_exists_importance=False).get("has_errors")
                message = validate_mobile_phone_handler(mobile_phone=mobile_phone,
                                                        mobile_phone_exists_importance=False).get("message")
                code = validate_mobile_phone_handler(mobile_phone=mobile_phone,
                                                     mobile_phone_exists_importance=False).get("code")

            else:
                CustomUser.objects.get(username=mobile_phone_or_username)

                has_errors = validate_username_handler(username=username, username_exists_importance=False).get(
                    "has_errors")

                message = validate_username_handler(username=username, username_exists_importance=False).get("message")

                code = validate_username_handler(username=username, username_exists_importance=False).get("code")

            if has_errors:
                raise ValidationError(message=message, code=code)

        except CustomUser.DoesNotExist:
            message = "کاربری با این مشخصات یافت نشد."
            code = "does_not_exist"

            raise ValidationError(message=message, code=code)


class CheckOTPForm(forms.Form):
    sms_code = forms.CharField(max_length=4, widget=forms.TextInput(
        attrs={'pattern': '[0-9]*', 'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")'}), label="کد تایید")


class ForgetPasswordForm(forms.Form):
    mobile_phone_or_username = forms.CharField(max_length=75, widget=forms.TextInput(),
                                               label="شماره تلفن یا نام کاربری")

    def clean(self):
        mobile_phone_or_username = self.cleaned_data.get("mobile_phone_or_username")

        mobile_phone = username = None

        if mobile_phone_or_username.isdigit():
            mobile_phone = mobile_phone_or_username
            field_name = "mobile_phone"

        else:
            username = mobile_phone_or_username
            field_name = "username"

        try:
            if mobile_phone:
                CustomUser.objects.get(mobile_phone=mobile_phone_or_username)

                has_errors = validate_mobile_phone_handler(mobile_phone=mobile_phone,
                                                           mobile_phone_exists_importance=False).get("has_errors")
                message = validate_mobile_phone_handler(mobile_phone=mobile_phone,
                                                        mobile_phone_exists_importance=False).get("message")
                code = validate_mobile_phone_handler(mobile_phone=mobile_phone,
                                                     mobile_phone_exists_importance=False).get("code")

            else:
                CustomUser.objects.get(username=mobile_phone_or_username)

                has_errors = validate_username_handler(username=username, username_exists_importance=False).get(
                    "has_errors")

                message = validate_username_handler(username=username, username_exists_importance=False).get("message")

                code = validate_username_handler(username=username, username_exists_importance=False).get("code")

            if has_errors:
                raise ValidationError(message=message, code=code)

        except CustomUser.DoesNotExist:
            message = "کاربری با این مشخصات یافت نشد."
            code = "does_not_exist"

            raise ValidationError(message=message, code=code)


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(), label="رمز عبور")

    password_repeat = forms.CharField(
        widget=forms.PasswordInput(), label="تکرار رمز عبور")

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")

        has_errors = validate_passwords_handler(password=password, password_repeat=password_repeat).get("has_errors")
        message = validate_passwords_handler(password=password, password_repeat=password_repeat).get("message")
        code = validate_passwords_handler(password=password, password_repeat=password_repeat).get("code")

        if has_errors:
            raise ValidationError(message=message, code=code)
