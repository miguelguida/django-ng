# Generated by Django 3.1.2 on 2021-09-09 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_auto_20210826_2048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assistencia',
            name='itemAssistencia',
        ),
    ]
