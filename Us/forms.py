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

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        mobile_phone = cleaned_data.get('mobile_phone')

        if not self.request.user.is_authenticated and not (email or mobile_phone):
            raise forms.ValidationError("لطفا حداقل یکی از فیلد‌های شماره تلفن یا آدرس ایمیل را پر کنید.")

        return cleaned_data
