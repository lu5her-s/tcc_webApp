# Generated by Django 4.2 on 2023-11-15 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcel', '0009_requestbill_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestitem',
            name='quantity_approve',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
