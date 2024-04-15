from django.forms import ModelForm, forms

from Us.models import Message

from django import forms


class ContactForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ContactForm, self).__init__(*args, **kwargs)

    def clean_message(self):
        message = self.cleaned_data.get("message")

        if len(message) > 250:
            raise forms.ValidationError(
                message="متن پیام نمی‌تواند بیش‌تر از 250 کاراکتر داشته باشد.",
                code="too_long_message")

        return message

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        mobile_phone = cleaned_data.get('mobile_phone')

        if not self.request.user.is_authenticated and not (email or mobile_phone):
            raise forms.ValidationError("لطفا حداقل یکی از فیلد‌های شماره تلفن یا آدرس ایمیل را پر کنید.")

        return cleaned_data
