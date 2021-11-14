# Generated by Django 3.2.9 on 2021-11-14 05:51

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20211114_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalteachermore',
            name='expert_in',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='historicalteachermore',
            name='last_institution',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='historicalteachermore',
            name='resume',
            field=models.TextField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='teachermore',
            name='expert_in',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='teachermore',
            name='last_institution',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='teachermore',
            name='resume',
            field=models.FileField(default=None, upload_to=accounts.models.user_directory_path),
        ),
    ]