# Generated by Django 4.1.1 on 2022-12-07 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0015_carbooking_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carbooking',
            old_name='mile_current',
            new_name='mile_in',
        ),
        migrations.AddField(
            model_name='carbooking',
            name='mile_out',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
