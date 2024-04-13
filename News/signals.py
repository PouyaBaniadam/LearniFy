from django.db.models.signals import post_save
from django.dispatch import receiver

from Account.models import NewsLetter
from News.email import send_created_news_email_to_news_letter
from News.models import News


@receiver(post_save, sender=News)
def send_news_created(sender, instance: News, created, **kwargs):
    if created:
        news_letter_emails = NewsLetter.objects.filter(is_blocked=False)
        emails = list(news_letter_emails.values_list('email', flat=True))

        send_created_news_email_to_news_letter(
            emails,
            f'{instance.category.name}',
            # TODO: Change the host name
            f"127.0.0.1:8000/news/detail/{instance.slug}"
        )
