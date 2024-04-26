# Generated by Django 5.0.4 on 2024-04-26 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0004_alter_notification_admin_alter_notification_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='usage',
            field=models.CharField(choices=[('INC', 'افزایشی'), ('DEC', 'کاهشی')], default=1, max_length=3, verbose_name='حالت استفاده'),
            preserve_default=False,
        ),
    ]