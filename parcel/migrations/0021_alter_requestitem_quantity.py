# Generated by Django 4.2 on 2023-12-19 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcel', '0020_requestitem_price_alter_requestitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]