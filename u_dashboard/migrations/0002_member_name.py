# Generated by Django 3.2 on 2021-11-16 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('u_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='name',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
