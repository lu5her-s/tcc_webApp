# Generated by Django 4.2 on 2023-11-16 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcel', '0011_remove_requestbill_receiver_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestbilldetail',
            name='is_done',
        ),
        migrations.AddField(
            model_name='requestbill',
            name='date_done',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='requestbill',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='requestitem',
            name='recieved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='requestitem',
            name='recieved_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]