# Generated by Django 2.0 on 2018-02-15 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projeto_p3', '0015_auto_20180214_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='obras',
            name='nif_dono_de_obra',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]