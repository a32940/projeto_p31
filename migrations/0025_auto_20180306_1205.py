# Generated by Django 2.0.2 on 2018-03-06 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projeto_p3', '0024_auto_20180306_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relatorios_mensais',
            name='meses',
            field=models.CharField(max_length=10),
        ),
    ]