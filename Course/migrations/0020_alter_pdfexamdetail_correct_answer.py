# Generated by Django 5.0.4 on 2024-05-10 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0019_alter_pdfexamdetail_correct_answer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdfexamdetail',
            name='correct_answer',
            field=models.CharField(help_text='دقیقا متن یکی از فیلد\u200c\u200cهای بالا', max_length=200, verbose_name='گزینه صحیح'),
        ),
    ]