# Generated by Django 5.0.4 on 2024-04-26 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0005_customuserboughtcourse'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuserboughtcourse',
            options={'verbose_name': 'دوره خریداری شده توسط کاربر', 'verbose_name_plural': 'دوره\u200cهای خریداری شده توسط کاربر'},
        ),
        migrations.AddField(
            model_name='customuserboughtcourse',
            name='cost',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='هزینه'),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='customuserboughtcourse',
            table='account__bought_course',
        ),
    ]