# Generated by Django 4.2 on 2024-10-09 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0019_alter_team_operation'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('PD', 'รอดำเนินการ'), ('CL', 'ปิด')], default='PD', max_length=2),
        ),
        migrations.DeleteModel(
            name='PlaceOperationNote',
        ),
    ]