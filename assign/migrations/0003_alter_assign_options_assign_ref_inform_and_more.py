# Generated by Django 4.2 on 2024-12-04 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inform', '0013_alter_inform_options'),
        ('assign', '0002_assignprogress_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assign',
            options={'verbose_name': 'Assign', 'verbose_name_plural': 'Assign'},
        ),
        migrations.AddField(
            model_name='assign',
            name='ref_inform',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_ref_inform', to='inform.inform'),
        ),
        migrations.AlterField(
            model_name='assign',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='assign',
            name='status',
            field=models.CharField(choices=[('Pending', 'รอตอบรับ'), ('Accepted', 'ตอบรับแล้ว'), ('Rejected', 'ปฏิเสธ'), ('Done', 'เสร็จสมบูรณ์')], default='Pending', max_length=20),
        ),
        migrations.DeleteModel(
            name='AssignStatus',
        ),
    ]
