# Generated by Django 4.1.1 on 2022-10-28 14:40

import assign.models
import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0003_alter_profile_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('body', ckeditor.fields.RichTextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('accepted', models.BooleanField(default=False)),
                ('accepted_on', models.DateTimeField(blank=True, null=True, verbose_name='date accepted')),
                ('note', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_to', to='account.profile')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignAuthor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AssignStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Status',
            },
        ),
        migrations.CreateModel(
            name='AssignProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('assign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assign.assign')),
            ],
            options={
                'verbose_name': 'Progress',
                'verbose_name_plural': 'Progress',
            },
        ),
        migrations.CreateModel(
            name='AssignImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(blank=True, null=True, upload_to=assign.models.get_image_name)),
                ('assign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assign.assign')),
            ],
            options={
                'verbose_name': 'Images',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.AddField(
            model_name='assign',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignStatus', to='assign.assignstatus'),
        ),
    ]