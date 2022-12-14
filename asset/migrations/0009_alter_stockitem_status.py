# Generated by Django 4.1.1 on 2022-12-22 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0008_alter_stockitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockitem',
            name='status',
            field=models.CharField(choices=[('AVAILABLE', 'พร้อมใช้งาน'), ('IN_USE', 'กำลังใช้งาน'), ('UNDER_MAINTENANCE', 'ซ่อมบำรุง'), ('DISPOSED', 'จำหน่าย')], default='AVAILABLE', max_length=20),
        ),
    ]
