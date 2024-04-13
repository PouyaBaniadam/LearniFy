import django_filters

from Course.models import Exam


class ExamFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains', label='دسته بندی')
    level = django_filters.ChoiceFilter(field_name='level', choices=Exam.level_choices_types, label='میزان سختی')
    payment_type = django_filters.ChoiceFilter(field_name='type', choices=Exam.exam_payment_types, label='نوع آزمون')
    has_discount = django_filters.BooleanFilter(field_name='has_discount', label='تخفیف')

    class Meta:
        model = Exam
        fields = ['category', 'level', 'type', 'has_discount']
