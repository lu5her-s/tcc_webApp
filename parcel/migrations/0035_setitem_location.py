# Generated by Django 4.2 on 2024-01-22 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_profile_options'),
        ('parcel', '0034_setitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='setitem',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.department'),
        ),
    ]
