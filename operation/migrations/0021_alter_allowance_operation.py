# Generated by Django 4.2 on 2024-10-15 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0020_task_note_task_status_delete_placeoperationnote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allowance',
            name='operation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='allowance', to='operation.operation'),
        ),
    ]
