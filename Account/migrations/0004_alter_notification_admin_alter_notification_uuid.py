# Generated by Django 5.0.4 on 2024-04-26 20:40

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0003_notification_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL, verbose_name='ادمین'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='یو\u200c\u200cیو\u200c\u200cآی\u200c\u200cدی'),
        ),
    ]