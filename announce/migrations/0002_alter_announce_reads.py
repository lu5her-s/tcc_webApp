# Generated by Django 4.1.1 on 2022-09-30 06:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('announce', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announce',
            name='reads',
            field=models.ManyToManyField(blank=True, related_name='readers', to=settings.AUTH_USER_MODEL),
        ),
    ]
