# Generated by Django 4.2 on 2024-11-03 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inform', '0013_alter_inform_options'),
        ('operation', '0025_operation_inform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='inform',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inform', to='inform.inform'),
        ),
    ]
