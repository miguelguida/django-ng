# Generated by Django 3.1.2 on 2021-08-17 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20210817_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='valor',
            field=models.CharField(max_length=200),
        ),
    ]
