# Generated by Django 4.2 on 2023-05-11 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0009_alter_stockitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockitemimage',
            name='stock_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='asset.stockitem'),
        ),
    ]