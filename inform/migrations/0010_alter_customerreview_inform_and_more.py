# Generated by Django 4.2 on 2023-09-12 14:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inform', '0009_alter_inform_repair_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerreview',
            name='inform',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_review', to='inform.inform'),
        ),
        migrations.AlterField(
            model_name='customerreview',
            name='reviewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewer', to=settings.AUTH_USER_MODEL),
        ),
    ]
