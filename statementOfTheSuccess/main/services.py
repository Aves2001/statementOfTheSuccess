import datetime

from django.core.validators import MaxValueValidator


def current_today():
    return datetime.date.today()


def current_year():
    return datetime.date.today().year


@property
def get_year(obj):
    return str(obj.date).split('-')[0][-2:]


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

