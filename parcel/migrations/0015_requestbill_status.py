# Generated by Django 4.2 on 2023-11-23 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcel', '0014_billnote_quantity_check_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestbill',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'ร่าง'), ('IN_PROGRESS', 'กำลังดำเนินการ'), ('DONE', 'เสร็จสิ้น')], default='DRAFT', max_length=50),
        ),
    ]
