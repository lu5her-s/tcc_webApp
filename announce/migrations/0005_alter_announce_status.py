# Generated by Django 4.2 on 2024-11-28 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announce', '0004_alter_announce_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announce',
            name='status',
            field=models.CharField(choices=[('PUBLISH', 'ประกาศ'), ('DONE', 'เสร็จสิ้น'), ('DELETE', 'ลบ')], default='PUBLISH', max_length=200),
        ),
    ]