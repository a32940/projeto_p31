# Generated by Django 2.0.2 on 2018-02-26 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projeto_p3', '0020_auto_20180223_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trabalhadores',
            name='idade',
            field=models.CharField(max_length=3),
        ),
    ]
