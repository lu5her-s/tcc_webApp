# Generated by Django 4.2 on 2024-06-30 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0005_rename_user_teammember_member_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
