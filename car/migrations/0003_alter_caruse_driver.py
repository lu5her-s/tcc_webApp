# Generated by Django 4.1.1 on 2022-11-02 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_profile_user'),
        ('car', '0002_alter_car_responsible_man'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caruse',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='driver', to='account.profile'),
        ),
    ]