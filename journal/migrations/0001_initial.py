# Generated by Django 4.1.1 on 2022-10-27 13:21

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
            name='Journal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('body', ckeditor.fields.RichTextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JournalStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='JournalType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='JournalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(blank=True, null=True, upload_to='get_image_name')),
                ('journal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journal.journal')),
            ],
            options={
                'verbose_name': 'JournalImage',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.AddField(
            model_name='journal',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journal.journaltype'),
        ),
        migrations.AddField(
            model_name='journal',
            name='header',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='header_journal', to='account.profile'),
        ),
        migrations.AddField(
            model_name='journal',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journal.journalstatus'),
        ),
    ]