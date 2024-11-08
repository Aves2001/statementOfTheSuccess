import datetime
import os

from django.core.validators import MaxValueValidator

from statementOfTheSuccess import settings


def current_today():
    return datetime.date.today()


def current_year():
    return datetime.date.today().year


@property
def get_year(obj):
    return str(obj.date).split('-')[0][-2:]


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


def get_grade_ECTS_and_5(grade, system_grane="ECTS"):
    if not grade:
        return ""
    rezult: tuple
    if 90 <= grade <= 100:
        rezult = "A", "5"
    elif 82 <= grade <= 89:
        rezult = "B", "4"
    elif 74 <= grade <= 81:
        rezult = "C", "4"
    elif 64 <= grade <= 73:
        rezult = "D", "3"
    elif 60 <= grade <= 63:
        rezult = "E", "3"
    elif 35 <= grade <= 59:
        rezult = "FX", "2"
    elif 1 <= grade <= 34:
        rezult = "F", "2"
    else:
        return None

    try:
        if system_grane == "ECTS":
            return rezult[0]
        elif system_grane == 5:
            return rezult[1]
    except:
        return None

def fetch_pdf_resources(uri, rel):
    # ��������, �� � URI ���������� ����������
    if uri.startswith("http"):
        return uri

    # ���� ��� ���������
    if settings.MEDIA_URL in uri:
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
    # ���� ��� ��������� �����
    elif settings.STATIC_URL in uri:
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ''))
    else:
        # ���������� None, ���� URI �� ������� ������� ������� �������
        path = None

    # �������� ��������� �����
    if path and os.path.isfile(path):
        return path
    return None