from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import Group
from django.utils.translation import ugettext as _
from projeto_p3.validators import validate_file_extension,validate_image
from django.urls import reverse
from PIL import Image as Img
from io import BytesIO,StringIO
from smart_selects.db_fields import ChainedForeignKey
from django.core.exceptions import ValidationError


estados = (
		('Em curso','Em curso'),
		('Terminado','Terminado'),
		('Suspenso','Suspenso'),
		('A iniciar','A iniciar'),
		('Parado','Parado'),
		('Pós venda','Pós venda'),
		('Anulada','Anulada')
	)
	
empresas = (
		('Jamefabs','Jamefabs'),
		('P3','P3')
	)
	
class obras(models.Model):
	num = models.CharField(max_length=20)
	designacao = models.CharField(max_length=500)
	concelho = models.CharField(max_length=500)
	num_cliente = models.CharField(max_length=500,blank=True)
	funcao = models.CharField(max_length=500)
	empresa = models.CharField(max_length=500,choices=empresas)
	cliente = models.CharField(max_length=500,blank=True)
	requerente = models.CharField(max_length=500,blank=True)
	dono_de_obra = models.CharField(max_length=500,blank=True)
	nif_dono_de_obra = models.CharField(max_length=500,blank=True)
	empreiteiro = models.CharField(max_length=500,blank=True)
	estado = models.CharField(max_length=500,choices=estados)
	periodicidade = models.CharField(max_length=500)
	tecnico = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=False,related_name="tecnico")
	auditor = models.ForeignKey(settings.AUTH_USER_MODEL,blank=False,on_delete=models.CASCADE,related_name="auditor")
	data_inicio = models.DateField()
	data_fim = models.DateField(blank=True,null=True)
	observacoes = models.CharField(max_length=500,blank=True)
	avaliacao = models.CharField(max_length=20,blank=True)
	num_at = models.CharField(max_length=20,blank=True)
	def __str__(self):
		return (self.designacao)
	class Meta:
		verbose_name = _("Obra")
		verbose_name_plural = _("Obras")
	def get_absolute_url(self):
		return reverse('obras_ver')

	
class auditorias(models.Model):
	tecnico = models.ForeignKey(settings.AUTH_USER_MODEL,blank=False,on_delete=models.CASCADE,related_name="tecnicos")
	auditor = models.ForeignKey(settings.AUTH_USER_MODEL,blank=False,on_delete=models.CASCADE,related_name="auditores")
	num = models.AutoField(primary_key=True)
	data = models.DateField()
	obra = models.ForeignKey(obras,related_name='obras',on_delete=models.CASCADE)
	trabalhos = models.CharField(max_length=1000)
	recomendacoes = models.CharField(max_length=1000)
	empresa = models.CharField(max_length=1000)
	#solicitado_cumprido = models.CharField(max_length = 1000)
	#solicitado_nao_cumprido = models.CharField(max_length = 1000)
	num_trabalhadores = models.CharField(max_length = 20)
	#num_acidentes = models.CharField(max_length = 20)
	def __str__(self):
		return str((self.obra)) + " " +str((self.num))+ " "+str((self.data))
	class Meta:
		verbose_name = _("Auditoria")
		verbose_name_plural = _("Auditorias")
	def get_absolute_url(self):
		return reverse('ver-auditoria')






class lista_conformidades(models.Model):
	numero = models.CharField(max_length=20)
	descricao = models.CharField(max_length=500)
	
	def __str__(self):
		return str((self.id)) + " " +str((self.descricao))
	def get_absolute_url(self):
		return reverse('lista_conformidades_ver')

class descricao_conformidades(models.Model):
	numero = models.CharField(max_length=20)
	descricao = models.CharField(max_length=500)
	lista = models.ForeignKey(lista_conformidades, default=None,on_delete=models.CASCADE)
	def __str__(self):
		return str((self.id)) + " " +str((self.descricao))
	def get_absolute_url(self):
		return reverse('descricao_conformidades_ver')

conforme = (
    ('certo.jpg', 'Conforme'),
    ('errado.jpg', 'Não conforme'),
)

"""lista_conformidades = (
    ('Guarda em falta', 'Guarda em falta'),
    ('Escada sem proteção', 'Escada sem proteção'),
    (' ', ' '),
)"""

lista_tarifario = (
    ('Assinatura', 'Assinatura'),
    ('Carregamento', 'Carregamento'),
    ('Nº proprio', 'Nº proprio'),
)
from sorl.thumbnail import ImageField, get_thumbnail
from django.core.files import File

class fotos(models.Model):
	auditoria = models.ForeignKey(auditorias, default=None,on_delete=models.CASCADE)
	imagem = models.ImageField(upload_to='img')
	conformidade = models.FileField(choices=conforme)
	conformidade_texto = models.ForeignKey(lista_conformidades, default=None,on_delete=models.CASCADE,related_name="descri")
	descricao = ChainedForeignKey(descricao_conformidades, chained_field="conformidade_texto",chained_model_field="lista",)
	#descricao = models.ForeignKey(descricao_conformidades, default=None,on_delete=models.CASCADE)
	conformidade_texto2 = models.CharField(max_length=500,blank=True,null=True)
	def save(self, *args, **kwargs):
		if self.imagem:
			image = Img.open(BytesIO(self.imagem.read()))
			image.thumbnail((700,700), Img.ANTIALIAS)
			output = BytesIO()
			image.save(output, format='JPEG', quality=70)
			output.seek(0)
			tipo = ".png"
			if self.imagem.name.endswith(tipo):
				self.imagem.name = self.imagem.name.replace("png", "jpg")
			self.imagem = File(output, self.imagem.name)
		super(fotos, self).save(*args, **kwargs)

class carros (models.Model):
	modelo = models.CharField(max_length=500)
	matricula = models.CharField(max_length=500)
	data_matricula = models.DateField()
	apolice_seguro = models.CharField(max_length=500)########
	data_seguro = models.DateField()#######
	def __str__(self):
		return str((self.matricula)) + " " +str((self.modelo))
	def get_absolute_url(self):
		return reverse('carros_ver')

class portatil (models.Model):
	modelo = models.CharField(max_length=500)
	serial_number = models.CharField(max_length=500)
	def __str__(self):
		return str((self.modelo))
	def get_absolute_url(self):
		return reverse('portatil_ver')

class telemovel (models.Model):
	modelo = models.CharField(max_length=500)
	serial_number = models.CharField(max_length=500)
	tarifario = models.CharField(max_length=500,choices=lista_tarifario,default=" ")
	numero = models.CharField(max_length=10)
	def __str__(self):
		return str(self.modelo) + " " +str(self.numero)
	def get_absolute_url(self):
		return reverse('telemovel_ver')

class cartao_comb (models.Model):
	numero = models.CharField(max_length=500)
	def __str__(self):
		return str((self.numero))
	def get_absolute_url(self):
		return reverse('cartao_comb_ver')



class equipamentos(models.Model):
	utilizador = models.ForeignKey(settings.AUTH_USER_MODEL,blank=False,on_delete=models.CASCADE,related_name="utilizador")
	carro = models.ForeignKey(carros,on_delete=models.CASCADE,related_name="carros1", blank=True, null=True)
	telemovel = models.ForeignKey(telemovel,on_delete=models.CASCADE,related_name="tele", blank=True, null=True)
	portatil = models.ForeignKey(portatil,on_delete=models.CASCADE,related_name="pc",blank=True, null=True)
	cartao_combustivel = models.ForeignKey(cartao_comb,on_delete=models.CASCADE,related_name="pc", blank=True, null=True)
	outros = models.CharField(max_length=500,blank=True)
	def __str__(self):
		return str((self.utilizador))
	def get_absolute_url(self):
		return reverse('equipamentos_ver')


sim_nao = (
    ('Sim', 'Sim'),
    ('Não', 'Não'),
)
apto_nao = (
    ('Apto', 'Apto'),
    ('Não', 'Não'),
)
sim_nao_ap = (
    ('Sim', 'Sim'),
    ('Não', 'Não'),
    ('Não aplicavél', 'Não aplicavél'),
)

meses = (
    ('Janeiro', 'Janeiro'),
    ('Fevereiro', 'Fevereiro'),
    ('Março', 'Março'),
    ('Abril', 'Abril'),
    ('Maio', 'Maio'),
    ('Junho', 'Junho'),
    ('Julho', 'Julho'),
    ('Agosto', 'Agosto'),
    ('Setembro', 'Setembro'),
    ('Outubro', 'Outubro'),
    ('Novembro', 'Novembro'),
    ('Dezembro', 'Dezembro'),
)
class empreiteiros(models.Model):
	subempreiteiro = models.ManyToManyField("self", blank=True)
	obra = models.ForeignKey(obras,on_delete=models.CASCADE,related_name="obras1", blank=True, null=True)
	nome_empresa = models.CharField(max_length=500)
	morada = models.CharField(max_length=500)
	cp = models.CharField(max_length=500)
	localidade = models.CharField(max_length=500)
	atividade = models.CharField(max_length=500)
	alvara = models.CharField(max_length=500)
	nif = models.CharField(max_length=500)
	nome_representante = models.CharField(max_length=500)
	contacto_representante = models.CharField(max_length=500)
	num_ap_seguro_resp_civil = models.CharField(max_length=500)
	data_seguro_resp_civil = models.DateField()
	validade_seguro_resp_civil = models.CharField(max_length=500)
	data_decl_ss = models.DateField()
	validade_decl_ss = models.CharField(max_length=500)
	data_cert_financas = models.DateField()
	validade_cert_financas = models.CharField(max_length=500)
	mes_folha_ferias = models.CharField(max_length=500,choices=meses)
	recibo_folha_ferias = models.CharField(max_length=500,choices=sim_nao)
	horario_trabalho = models.CharField(max_length=500,choices=sim_nao)
	declaracao_pss = models.CharField(max_length=500,choices=sim_nao)
	declaracao_imigrantes = models.CharField(max_length=500,choices=sim_nao)
	contrato_subempreitada =  models.CharField(max_length=500,choices=sim_nao)
	companhia_seguro_trabalho = models.CharField(max_length=500)
	apolice_seguro_trabalho = models.CharField(max_length=500)
	modalidade_seguro_trabalho = models.CharField(max_length=500)
	valdade_seguro_trabalho = models.CharField(max_length=500)
	def __str__(self):
		return str((self.nome_empresa))
	def get_absolute_url(self):
		return reverse('empreiteiros_ver')

class subempreiteiros(models.Model):
	emp_geral = models.ForeignKey(empreiteiros,on_delete=models.CASCADE,related_name="trabas")
	subempreiteiro = models.ManyToManyField(empreiteiros)

class trabalhadores(models.Model):
	empreiteiro = models.ForeignKey(empreiteiros,on_delete=models.CASCADE,related_name="trab")
	nome = models.CharField(max_length=500)
	num_di = models.CharField(max_length=500)
	validade_di = models.DateField()
	dn = models.CharField(max_length=500)
	nif = models.CharField(max_length=500)
	niss = models.CharField(max_length=500)
	resultado_insp_med = models.CharField(max_length=500,choices=apto_nao)
	data_insp_med = models.DateField()
	validade_insp_med = models.CharField(max_length=500)
	registo_epis = models.CharField(max_length=500,choices=sim_nao_ap)
	registo_formacao = models.CharField(max_length=500,choices=sim_nao_ap)
	cp = models.CharField(max_length=500)
	contrato_act = models.CharField(max_length=500,choices=sim_nao_ap)
	seguro_at = models.CharField(max_length=500,choices=sim_nao_ap)
	declaracao_manobrador = models.CharField(max_length=500,choices=sim_nao_ap)
	carta_riscos = models.CharField(max_length=500,choices=sim_nao_ap)
	idade = models.CharField(max_length=3)
	data_entrada_obra = models.DateField()
	data_saida_obra =  models.DateField()
	def __str__(self):
		return str((self.nome))
	def get_absolute_url(self):
		return reverse('trabalhadores_ver')

class equipamentos_empresa(models.Model):
	empreiteiro = models.ForeignKey(empreiteiros,on_delete=models.CASCADE,related_name="emp1")
	def __str__(self):
		return str((self.empreiteiro))
	def get_absolute_url(self):
		return reverse('equipamentos_empresa_ver')




class sub_empreiteiros(models.Model):
	empreiteiros = models.ForeignKey(empreiteiros,on_delete=models.CASCADE,related_name="empre2")
	nome_empresa = models.CharField(max_length=500)
	morada = models.CharField(max_length=500)
	atividade = models.CharField(max_length=500)
	alvara = models.CharField(max_length=500)
	nif = models.CharField(max_length=500)
	nome_representante = models.CharField(max_length=500)
	contacto_representante = models.CharField(max_length=500)
	num_ap_seguro_resp_civil = models.CharField(max_length=500)
	data_seguro_resp_civil = models.DateField()
	validade_seguro_resp_civil = models.CharField(max_length=500)
	data_decl_ss = models.DateField()
	validade_decl_ss = models.CharField(max_length=500)
	data_cert_financas = models.DateField()
	validade_cert_financas = models.CharField(max_length=500)
	mes_folha_ferias = models.CharField(max_length=500,choices=meses)
	recibo_folha_ferias = models.CharField(max_length=500,choices=sim_nao)
	horario_trabalho = models.CharField(max_length=500,choices=sim_nao)
	declaracao_pss = models.CharField(max_length=500,choices=sim_nao)
	declaracao_imigrantes = models.CharField(max_length=500,choices=sim_nao)
	contrato_subempreitada =  models.CharField(max_length=500,choices=sim_nao)
	def __str__(self):
		return str((self.nome_empresa))
	def get_absolute_url(self):
		return reverse('sub_empreiteiros_ver')

class empreitada(models.Model):
	empresa = models.ForeignKey(empreiteiros,on_delete=models.CASCADE,related_name="emp")
	sub_empresa = models.ForeignKey(sub_empreiteiros,on_delete=models.CASCADE,related_name="sub_emp")
	trabalhadores = models.ForeignKey(trabalhadores,on_delete=models.CASCADE,related_name="trab1")
	equipamentos = models.ForeignKey(equipamentos,on_delete=models.CASCADE,related_name="equips")
	def __str__(self):
		return str((self.empresa))
	def get_absolute_url(self):
		return reverse('empreitada_ver')

def validate_only_one_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 12 and
            obj.id != model.objects.get().id):
        raise ValidationError("Can only create 1 %s instance" % model.__name__)

class relatorios_mensais(models.Model):
	obras = models.ForeignKey(obras,on_delete=models.CASCADE,related_name="rel_mens")
	meses = models.CharField(max_length=10)#, unique=True
	avaliacao = models.CharField(max_length=10)
	def __str__(self):
		return str((self.avaliacao))
	def clean(self):
		validate_only_one_instance(self)