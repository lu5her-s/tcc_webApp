# Generated by Django 4.2 on 2023-11-10 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_profile_department'),
        ('parcel', '0008_rename_qauntity_requestitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestbill',
            name='stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.department'),
        ),
    ]