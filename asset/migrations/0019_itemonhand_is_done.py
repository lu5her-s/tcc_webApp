# Generated by Django 4.2 on 2024-02-08 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0018_itemhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemonhand',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
    ]
