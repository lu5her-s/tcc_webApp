# Generated by Django 4.1.1 on 2022-11-11 13:58

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0003_alter_profile_user'),
        ('car', '0007_carfiximage'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CarUse',
            new_name='CarBooking',
        ),
    ]
