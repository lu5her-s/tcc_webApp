# Generated by Django 4.2 on 2023-08-22 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inform', '0006_alter_inform_inform_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='inform',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]
