# Generated by Django 3.1.2 on 2021-08-17 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20210817_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='lastUpdate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='representada',
            name='lastUpdate',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
