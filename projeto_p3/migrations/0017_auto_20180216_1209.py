# Generated by Django 2.0 on 2018-02-16 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projeto_p3', '0016_obras_nif_dono_de_obra'),
    ]

    operations = [
        migrations.AddField(
            model_name='empreiteiros',
            name='cp',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empreiteiros',
            name='localidade',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
    ]
