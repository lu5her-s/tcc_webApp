# Generated by Django 4.2 on 2024-04-08 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0022_alter_itemonhand_item'),
        ('parcel', '0041_parcelreturn_rejectreturnbillnote_parcelreturndetail_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParcelReturnItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='return_bill', to='parcel.parcelreturn')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='return_item', to='asset.stockitem')),
            ],
        ),
    ]
