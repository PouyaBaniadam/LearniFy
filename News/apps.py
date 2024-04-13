from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'News'
    verbose_name = 'اخبار'

    def ready(self):
        import News.signals
