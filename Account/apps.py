from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Account'
    verbose_name = "حساب کاربری"

    def ready(self):
        import Account.signals
