from django import template
from jdatetime import date as jdate

register = template.Library()


@register.filter(name='price_splitter')
def price_splitter(value):
    try:
        value = int(value)
        return "{:,}".format(value)
    except ValueError:
        return value


@register.filter(name='float_to_int_converter')
def float_to_int_converter(value):
    if value == int(value):
        return int(value)
    else:
        return value


@register.filter(name='j_date_formatter')
def j_date_formatter(value):
    day_name = jdate.j_weekdays_fa[value.weekday()]
    day = value.day
    month_name = jdate.j_months_fa[value.month - 1]
    year = value.year
    hour = value.hour
    minute = value.minute

    formatted_date = f'{day_name}، {day} {month_name} {year} ساعت {hour:02d}:{minute:02d}'

    return formatted_date


@register.filter(name='format_seconds_to_time')
def format_seconds_to_time(total_seconds):
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds))
