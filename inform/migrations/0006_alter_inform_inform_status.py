# Generated by Django 4.2 on 2023-07-18 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inform', '0005_inform_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inform',
            name='inform_status',
            field=models.CharField(blank=True, choices=[('INF', 'แจ้งซ่อม'), ('WAT', 'รออนุมัติ'), ('REJ', 'ยกเลิก')], default='INF', max_length=8, null=True),
        ),
    ]
