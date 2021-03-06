# Generated by Django 3.1.2 on 2021-08-26 23:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_acabamento_assistencia_cliente_formapagamento_pedido_tecido_transportadora_vendedor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assistencia',
            name='acabamento',
        ),
        migrations.RemoveField(
            model_name='assistencia',
            name='mostruario',
        ),
        migrations.RemoveField(
            model_name='assistencia',
            name='produto',
        ),
        migrations.RemoveField(
            model_name='assistencia',
            name='quantidade',
        ),
        migrations.RemoveField(
            model_name='assistencia',
            name='referencia',
        ),
        migrations.AlterField(
            model_name='assistencia',
            name='observacoes',
            field=models.TextField(max_length=600),
        ),
        migrations.CreateModel(
            name='ItemAssistencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referencia', models.CharField(max_length=200)),
                ('quantidade', models.IntegerField()),
                ('observacoes', models.TextField(max_length=200)),
                ('mostruario', models.BooleanField()),
                ('lastUpdate', models.DateTimeField(auto_now=True)),
                ('acabamento', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.acabamento')),
                ('produto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.produto')),
            ],
        ),
        migrations.AddField(
            model_name='assistencia',
            name='itemAssistencia',
            field=models.ManyToManyField(to='myapp.ItemAssistencia'),
        ),
    ]
