# Generated by Django 4.2 on 2023-10-30 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcel', '0005_remove_requestbill_department_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requestbilldetail',
            old_name='is_paid',
            new_name='is_done',
        ),
        migrations.AddField(
            model_name='requestitem',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='requestitem',
            name='paid_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
