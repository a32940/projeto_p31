# Generated by Django 2.0.2 on 2018-03-06 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projeto_p3', '0021_auto_20180226_1146'),
    ]

    operations = [
        migrations.CreateModel(
            name='relatorio_mensal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meses', models.CharField(max_length=10)),
                ('avaliacao', models.CharField(max_length=10)),
                ('obras', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_mens', to='projeto_p3.obras')),
            ],
        ),
    ]
