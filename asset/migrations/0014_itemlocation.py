# Generated by Django 4.2 on 2023-09-28 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_profile_department'),
        ('asset', '0013_stockitem_count_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.stockitem')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.department')),
            ],
        ),
    ]
