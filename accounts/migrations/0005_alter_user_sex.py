# Generated by Django 3.2 on 2021-11-14 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20211114_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ('P', 'Do not want say!')], default='P', max_length=1, verbose_name='SexChoices'),
        ),
    ]