# Generated by Django 4.2 on 2023-12-27 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parcel', '0022_alter_requestbill_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestitem',
            name='serial_no',
        ),
    ]