# Generated by Django 3.1.2 on 2021-08-10 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_produto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='representada',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.representada'),
        ),
    ]
