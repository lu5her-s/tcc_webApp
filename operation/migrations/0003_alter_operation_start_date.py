# Generated by Django 4.2 on 2024-06-30 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0002_task_rename_job_description_operation_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
