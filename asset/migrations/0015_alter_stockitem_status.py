# Generated by Django 4.2 on 2023-10-30 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0014_itemlocation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockitem',
            name='status',
            field=models.CharField(choices=[('AVAILABLE', 'พร้อมใช้งาน'), ('IN_USE', 'กำลังใช้งาน'), ('UNDER_MAINTENANCE', 'ซ่อมบำรุง'), ('DISPOSED', 'จำหน่าย'), ('CHECK', 'ตรวจสอบ'), ('HOLD', 'จอง'), ('ON_HAND', 'เคลื่อนไหว')], default='AVAILABLE', max_length=20),
        ),
    ]
