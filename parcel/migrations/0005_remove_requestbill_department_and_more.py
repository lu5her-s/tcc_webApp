# Generated by Django 4.2 on 2023-10-30 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcel', '0004_alter_requestbill_department_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestbill',
            name='department',
        ),
        migrations.RemoveField(
            model_name='requestbilldetail',
            name='quantity_approve',
        ),
        migrations.AddField(
            model_name='requestitem',
            name='quantity_approve',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
