# Generated by Django 5.0.4 on 2024-05-09 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0017_alter_pdfexamtempanswer_selected_answer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdfexamdetail',
            name='correct_answer',
            field=models.CharField(choices=[('1', 'گزینه 1'), ('2', 'گزینه 2'), ('3', 'گزینه 3'), ('4', 'گزینه 4')], help_text='متن یکی از فیلد\u200c\u200cهای بالا', max_length=1, verbose_name='گزینه صحیح'),
        ),
        migrations.AlterField(
            model_name='pdfexamtempanswer',
            name='selected_answer',
            field=models.CharField(choices=[('1', 'گزینه 1'), ('2', 'گزینه 2'), ('3', 'گزینه 3'), ('4', 'گزینه 4')], max_length=1, verbose_name='گزینه انتخاب شده'),
        ),
        migrations.AlterField(
            model_name='videoexamdetail',
            name='correct_answer',
            field=models.CharField(choices=[('1', 'گزینه 1'), ('2', 'گزینه 2'), ('3', 'گزینه 3'), ('4', 'گزینه 4')], help_text='متن یکی از فیلد\u200c\u200cهای بالا', max_length=1, verbose_name='گزینه صحیح'),
        ),
        migrations.AlterField(
            model_name='videoexamtempanswer',
            name='selected_answer',
            field=models.CharField(choices=[('1', 'گزینه 1'), ('2', 'گزینه 2'), ('3', 'گزینه 3'), ('4', 'گزینه 4')], max_length=1, verbose_name='گزینه انتخاب شده'),
        ),
    ]
