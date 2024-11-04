from django.contrib.auth.models import Group
from django.db import migrations


def apply_migration(apps, schema_editor):
    group, created = Group.objects.get_or_create(name='Викладачі')
    group, created = Group.objects.get_or_create(name='Деканат')


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(apply_migration)
    ]
