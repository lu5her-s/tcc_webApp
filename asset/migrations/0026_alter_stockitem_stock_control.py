# Generated by Django 4.2 on 2024-11-11 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0025_remove_stockitem_dept_used_remove_stockitem_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockitem',
            name='stock_control',
            field=models.CharField(choices=[('RELAY', 'คลังวิทยุถ่ายทอด'), ('SATT', 'คลังดาวเทียม'), ('FO', 'คลังใยแก้วนำแสง'), ('NETWORK', 'คลังสื่อสารข้อมูล'), ('AIR', 'คลังเครื่องปรับอากาศ')], default='RELAY', max_length=20),
        ),
    ]