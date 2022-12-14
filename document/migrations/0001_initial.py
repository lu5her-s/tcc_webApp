# Generated by Django 4.1.1 on 2022-10-17 08:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0003_alter_profile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recieve_number', models.CharField(max_length=200)),
                ('doc_sector', models.CharField(blank=True, max_length=200, null=True)),
                ('doc_number', models.CharField(max_length=200)),
                ('doc_date', models.DateField()),
                ('urgency', models.CharField(choices=[('ปกติ', 'ปกติ'), ('ด่วน', 'ด่วน'), ('ด่วนมาก', 'ด่วนมาก'), ('ด่วนที่สุด', 'ด่วนที่สุด')], default='ปกติ', max_length=200)),
                ('title', models.TextField()),
                ('detail', models.TextField()),
                ('report_to', models.CharField(blank=True, max_length=200, null=True)),
                ('operation', models.CharField(choices=[('ปฏิบัติ', 'ปฏิบัติ'), ('เพื่อทราบ', 'เพื่อทราบ')], default='เพื่อทราบ', max_length=200)),
                ('status', models.CharField(choices=[('รอการปฏิบัติ', 'รอการปฏิบัติ'), ('แผนกรับแล้ว', 'แผนกรับแล้ว'), ('จนท.กำลังดำเนินการ', 'จนท.กำลังดำเนินการ'), ('ดำเนินการแล้ว', 'ดำเนินการแล้ว'), ('เสร็จสิ้น', 'เสร็จสิ้น')], default='รอการปฏิบัติ', max_length=200)),
                ('file', models.FileField(upload_to='Document/%Y/%m/%d/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('assigned_sector', models.ManyToManyField(related_name='assigned_sector', to='account.sector')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='document.category')),
            ],
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recieved_at', models.DateTimeField(auto_now_add=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document.document')),
                ('reciever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recieved_at', models.DateTimeField(auto_now_add=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('assigned_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.profile')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document.document')),
                ('reciever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
