# Generated by Django 4.2 on 2024-11-13 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0026_alter_stockitem_stock_control'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockitem',
            name='stock_control',
            field=models.CharField(blank=True, choices=[('RELAY', 'คลังวิทยุถ่ายทอด'), ('SATT', 'คลังดาวเทียม'), ('FO', 'คลังใยแก้วนำแสง'), ('DATA', 'คลังสื่อสารข้อมูล'), ('AIR', 'คลังเครื่องปรับอากาศ')], max_length=20, null=True),
        ),
    ]