import os
import secrets
import string
from datetime import datetime

import pytz


def generate_token(token_length):
    url_safe_alphabet = string.ascii_letters + string.digits + '-_~'
    url_safe_password = ''.join(secrets.choice(url_safe_alphabet) for i in range(token_length))
    return url_safe_password


def humanize_video_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)


def duration_hour_to_seconds(duration_str):
    hours, minutes, seconds = map(int, duration_str.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


def get_file_size(file_path):
    return os.path.getsize(file_path)



def get_time_difference(date_1, date_2):
    """
    Calculates the time difference in seconds between two dates,
    handling potential timezone information.

    Args:
        date_1 (datetime): The first date.
        date_2 (datetime): The second date.

    Returns:
        float: The time difference in seconds.

    Raises:
        TypeError: If either input is not a datetime object.
    """

    if not isinstance(date_1, datetime) or not isinstance(date_2, datetime):
        raise TypeError("ورودی‌ها از یک نوع نمی‌باشد.")

    if not date_1.tzinfo:
        date_1 = date_1.replace(tzinfo=pytz.utc)

    if not date_2.tzinfo:
        date_2 = date_2.replace(tzinfo=pytz.utc)

    date1_utc = date_1.astimezone(pytz.utc)
    date2_utc = date_2.astimezone(pytz.utc)

    time_difference = (date2_utc - date1_utc).total_seconds()

    return time_difference
