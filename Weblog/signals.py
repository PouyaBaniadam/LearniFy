from django.db.models.signals import post_save
from django.dispatch import receiver

from Account.models import NewsLetter
from Weblog.email import send_created_weblog_email_to_news_letter
from Weblog.models import Weblog


@receiver(post_save, sender=Weblog)
def send_weblog_created(sender, instance: Weblog, created, **kwargs):
    if created:
        news_letter_emails = NewsLetter.objects.filter(is_blocked=False)
        emails = list(news_letter_emails.values_list('email', flat=True))

        send_created_weblog_email_to_news_letter(
            emails,
            f'{instance.category.name}',
            # TODO: Change the host name
            f"127.0.0.1:8000/weblog/detail/{instance.slug}"
        )
