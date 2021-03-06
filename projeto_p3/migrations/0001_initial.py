# Generated by Django 2.0 on 2018-01-16 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import projeto_p3.validators
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='auditorias',
            fields=[
                ('num', models.AutoField(primary_key=True, serialize=False)),
                ('data', models.DateField()),
                ('trabalhos', models.CharField(max_length=1000)),
                ('recomendacoes', models.CharField(max_length=1000)),
                ('empresa', models.CharField(max_length=1000)),
                ('num_trabalhadores', models.CharField(max_length=20)),
                ('auditor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auditores', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Auditoria',
                'verbose_name_plural': 'Auditorias',
            },
        ),
        migrations.CreateModel(
            name='carros',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.CharField(max_length=500)),
                ('matricula', models.CharField(max_length=500)),
                ('data_matricula', models.DateField()),
                ('apolice_seguro', models.CharField(max_length=500)),
                ('data_seguro', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='cartao_comb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='descricao_conformidades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=20)),
                ('descricao', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='equipamentos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outros', models.CharField(blank=True, max_length=500)),
                ('carro', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='carros1', to='projeto_p3.carros')),
                ('cartao_combustivel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pc', to='projeto_p3.cartao_comb')),
            ],
        ),
        migrations.CreateModel(
            name='fotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(blank=True, default='img/tensao.jpg', upload_to='img', validators=[projeto_p3.validators.validate_file_extension, projeto_p3.validators.validate_image])),
                ('conformidade', models.FileField(choices=[('certo.jpg', 'Conforme'), ('errado.jpg', 'Não conforme')], upload_to='')),
                ('conformidade_texto2', models.CharField(blank=True, max_length=500, null=True)),
                ('auditoria', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='projeto_p3.auditorias')),
            ],
        ),
        migrations.CreateModel(
            name='lista_conformidades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=20)),
                ('descricao', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='obras',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(max_length=20)),
                ('designacao', models.CharField(max_length=500)),
                ('concelho', models.CharField(max_length=500)),
                ('num_cliente', models.CharField(blank=True, max_length=500)),
                ('funcao', models.CharField(max_length=500)),
                ('empresa', models.CharField(choices=[('Jamefabs', 'Jamefabs'), ('P3', 'P3')], max_length=500)),
                ('cliente', models.CharField(blank=True, max_length=500)),
                ('requerente', models.CharField(blank=True, max_length=500)),
                ('dono_de_obra', models.CharField(blank=True, max_length=500)),
                ('empreiteiro', models.CharField(blank=True, max_length=500)),
                ('estado', models.CharField(choices=[('Em curso', 'Em curso'), ('Terminado', 'Terminado'), ('Suspenso', 'Suspenso'), ('A iniciar', 'A iniciar'), ('Parado', 'Parado'), ('Pós venda', 'Pós venda'), ('Anulada', 'Anulada')], max_length=500)),
                ('periodicidade', models.CharField(max_length=500)),
                ('data_inicio', models.DateField()),
                ('data_fim', models.DateField(blank=True, null=True)),
                ('observacoes', models.CharField(blank=True, max_length=500)),
                ('avaliacao', models.CharField(blank=True, max_length=20)),
                ('num_at', models.CharField(blank=True, max_length=20)),
                ('auditor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auditor', to=settings.AUTH_USER_MODEL)),
                ('tecnico', models.ManyToManyField(related_name='tecnico', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Obra',
                'verbose_name_plural': 'Obras',
            },
        ),
        migrations.CreateModel(
            name='portatil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.CharField(max_length=500)),
                ('serial_number', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='telemovel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.CharField(max_length=500)),
                ('serial_number', models.CharField(max_length=500)),
                ('tarifario', models.CharField(choices=[('Assinatura', 'Assinatura'), ('Carregamento', 'Carregamento'), ('Nº proprio', 'Nº proprio')], default=' ', max_length=500)),
                ('numero', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='fotos',
            name='conformidade_texto',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='descri', to='projeto_p3.lista_conformidades'),
        ),
        migrations.AddField(
            model_name='fotos',
            name='descricao',
            field=smart_selects.db_fields.ChainedForeignKey(chained_field='conformidade_texto', chained_model_field='lista', on_delete=django.db.models.deletion.CASCADE, to='projeto_p3.descricao_conformidades'),
        ),
        migrations.AddField(
            model_name='equipamentos',
            name='portatil',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pc', to='projeto_p3.portatil'),
        ),
        migrations.AddField(
            model_name='equipamentos',
            name='telemovel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tele', to='projeto_p3.telemovel'),
        ),
        migrations.AddField(
            model_name='equipamentos',
            name='utilizador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='utilizador', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='descricao_conformidades',
            name='lista',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='projeto_p3.lista_conformidades'),
        ),
        migrations.AddField(
            model_name='auditorias',
            name='obra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='obras', to='projeto_p3.obras'),
        ),
        migrations.AddField(
            model_name='auditorias',
            name='tecnico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tecnicos', to=settings.AUTH_USER_MODEL),
        ),
    ]
