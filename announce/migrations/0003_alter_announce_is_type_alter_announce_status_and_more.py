# Generated by Django 4.2 on 2024-11-28 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announce', '0002_alter_announce_reads'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announce',
            name='is_type',
            field=models.CharField(choices=[('INFORM', 'ประชาสัมพันธ์'), ('ORDER', 'สั่งการ'), ('COORDINATE', 'ประสานงาน')], default='INFORM', max_length=200),
        ),
        migrations.AlterField(
            model_name='announce',
            name='status',
            field=models.CharField(choices=[('NEW', 'สร้าง'), ('PUBLISH', 'ประกาศ'), ('DELETE', 'ลบ')], default='NEW', max_length=200),
        ),
        migrations.DeleteModel(
            name='AnnounceStatus',
        ),
        migrations.DeleteModel(
            name='AnnounceType',
        ),
    ]