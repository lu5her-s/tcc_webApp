# Generated by Django 4.2 on 2024-07-03 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0008_operation_other_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='team',
            name='accepted_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]