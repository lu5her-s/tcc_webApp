# Generated by Django 4.1.1 on 2022-11-30 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0012_alter_carfix_car'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refuel',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_refuel', to='car.car'),
        ),
    ]