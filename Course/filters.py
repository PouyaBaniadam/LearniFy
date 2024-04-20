import django_filters

from Course.models import VideoCourse, PDFCourse


class VideoCourseFilter(django_filters.FilterSet):
    PAYMENT_TYPE_CHOICES = (
        ('F', 'رایگان'),
        ('P', 'پولی'),
    )

    HOLDING_STATUS_CHOICES = (
        ('NS', 'هنوز شروع نشده'),
        ('IP', 'در حال برگزاری'),
        ('F', 'به اتمام رسیده'),
    )

    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='exact', label='دسته بندی')
    payment_type = django_filters.ChoiceFilter(choices=PAYMENT_TYPE_CHOICES, label='نوع دوره')
    holding_status = django_filters.ChoiceFilter(choices=HOLDING_STATUS_CHOICES, label='وضعیت برگزاری دوره')
    has_discount = django_filters.BooleanFilter(field_name='has_discount', label='تخفیف')

    class Meta:
        model = VideoCourse
        fields = ['category', 'payment_type', 'holding_status', 'has_discount']


class PDFCourseFilter(django_filters.FilterSet):
    PAYMENT_TYPE_CHOICES = (
        ('F', 'رایگان'),
        ('P', 'پولی'),
    )

    HOLDING_STATUS_CHOICES = (
        ('NS', 'هنوز شروع نشده'),
        ('IP', 'در حال برگزاری'),
        ('F', 'به اتمام رسیده'),
    )

    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='exact', label='دسته بندی')
    payment_type = django_filters.ChoiceFilter(choices=PAYMENT_TYPE_CHOICES, label='نوع دوره')
    holding_status = django_filters.ChoiceFilter(choices=HOLDING_STATUS_CHOICES, label='وضعیت برگزاری دوره')
    has_discount = django_filters.BooleanFilter(field_name='has_discount', label='تخفیف')

    class Meta:
        model = PDFCourse
        fields = ['category', 'payment_type', 'holding_status', 'has_discount']
