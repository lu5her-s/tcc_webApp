# Generated by Django 4.1.1 on 2022-12-15 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0017_refuel_mile_refuel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carfix',
            name='cost_expect',
        ),
        migrations.AlterField(
            model_name='carfix',
            name='cost_use',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
