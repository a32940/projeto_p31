# Generated by Django 2.0 on 2018-01-19 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projeto_p3', '0002_auto_20180117_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fotos',
            name='descricao',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='projeto_p3.descricao_conformidades'),
        ),
    ]