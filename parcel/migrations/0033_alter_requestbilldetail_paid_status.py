# Generated by Django 4.2 on 2024-01-15 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcel', '0032_alter_requestbilldetail_paid_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestbilldetail',
            name='paid_status',
            field=models.CharField(blank=True, choices=[('PAID', 'เตรียมจ่ายพัสดุ'), ('RECEIVED', 'รับพัสดุแล้ว')], max_length=50, null=True),
        ),
    ]