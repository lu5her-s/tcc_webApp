# Generated by Django 4.2 on 2024-03-27 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_profile_options'),
        ('asset', '0019_itemonhand_is_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockitem',
            name='location_setup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='location_setup', to='account.department'),
        ),
    ]
