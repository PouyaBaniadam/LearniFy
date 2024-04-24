# Generated by Django 5.0.4 on 2024-04-24 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0003_alter_newsletter_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='visibility',
            field=models.CharField(choices=[('GL', 'عمومی'), ('PV', 'شخصی')], max_length=2, verbose_name='وضعیت مشاهده'),
        ),
    ]