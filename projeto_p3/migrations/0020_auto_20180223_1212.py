# Generated by Django 2.0.2 on 2018-02-23 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projeto_p3', '0019_auto_20180223_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empreiteiros',
            name='subempreiteiro',
            field=models.ManyToManyField(blank=True, null=True, related_name='_empreiteiros_subempreiteiro_+', to='projeto_p3.empreiteiros'),
        ),
    ]