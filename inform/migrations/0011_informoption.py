# Generated by Django 4.2 on 2023-09-18 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0022_alter_carafterfiximage_images'),
        ('inform', '0010_alter_customerreview_inform_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InformOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='car.carbooking')),
                ('inform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inform.inform')),
            ],
        ),
    ]