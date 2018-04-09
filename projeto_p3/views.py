from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect,render_to_response
import json
from django.http import JsonResponse
from django.http import Http404
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext as _
from django.utils.translation import activate
from django.utils import translation
from django.core.files import File
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.auth.models import Permission
from django.contrib.auth import logout
from django.utils import translation
from django.contrib import auth
from django.contrib.auth import (authenticate,get_user_model,login,logout)
from django.contrib.auth.models import Group
from django.contrib.admin.models import LogEntry
from django.contrib.auth.decorators import permission_required,user_passes_test,login_required
from django.core.mail import EmailMessage
from django.views.decorators.cache import cache_control
from projeto_p3.forms import Descricao_conformidadesForm,EmpreitadaForm,Sub_empreiteirosForm,TrabalhadoresForm,EmpreiteirosForm,Lista_conformidadesForm,UserLoginForm,ObraForm,AuditoriaForm,FotosForm,SetPasswordForm,PasswordResetRequestForm,EquipamentosForm,CarrosForm,PortatilForm,TelemovelForm,CataoCombForm,Lista_conformidadesForm
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas
from projeto_p3.models import relatorios_mensais,descricao_conformidades,empreitada,sub_empreiteiros,trabalhadores,empreiteiros,obras,auditorias,fotos,equipamentos,cartao_comb,telemovel,portatil,carros,lista_conformidades,descricao_conformidades
import tempfile
from django.template.loader import render_to_string
from django.core.mail import EmailMessage,send_mail
import pdfkit
import os
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image,Frame,PageTemplate,BaseDocTemplate
from django.contrib.auth.models import User
from django.forms import modelformset_factory
import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch,cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from extra_views import CreateWithInlinesView,InlineFormSet,InlineFormSetView,UpdateWithInlinesView
from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import permission_required,user_passes_test,login_required
from django.utils.decorators import method_decorator
from django_addanother.views import CreatePopupMixin
from functools import partial
from reportlab.lib.pagesizes import A4
from django.views.generic.edit import FormView
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.views.generic import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
import csv
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import (black,purple,white,yellow,blue,gray,lightblue,HexColor)
from reportlab.platypus import PageBreak
import time
import locale
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from django.db import IntegrityError

#import locale
#locale.setlocale(locale.LC_ALL, 'pt_BR')
locale.setlocale(locale.LC_ALL, 'pt-PT')
#locale.setlocale(locale.LC_ALL, 'deu_deu')
#locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')

pdfmetrics.registerFont(TTFont('Calibri', 'projeto_p3/static/fonts/calibri.ttf'))
pdfmetrics.registerFont(TTFont('Calibri_Bold', 'projeto_p3/static/fonts/calibri_bold.ttf'))
pdfmetrics.registerFont(TTFont('Calibri_Italic', 'projeto_p3/static/fonts/calibri_italic.ttf'))
pdfmetrics.registerFont(TTFont('Calibri_Bold_Italic', 'projeto_p3/static/fonts/calibri_bold_italic.ttf'))

	
recomendacoes_seguranca = ('A entidade executante deverá elaborar e enviar o Desenvolvimento do Plano de Segurança e Saúde, de acordo com o previsto no DL de 29 de Outubro. O DPSS deverá contemplar um Plano de Trabalhos com Riscos Especiais (PTRE) para a atividade de Demolição; Estedocumento deverá estar em obra disponível para consulta; (urgente)A EE deverá remeter à CSO toda a documentação das empresas presentesem obra; A CSO identificará periodicamente trabalhadores em obra com ointuito de verificar se possuem toda a documentação legal obrigatória;')


def login_page(request):
	titulo = ("Login")
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username=form.cleaned_data.get("username")
		password=form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				return redirect('/')
	return render (request ,"meu_login.html",{"form" : form , "titulo" : titulo})


def logout_page(request):
	logout(request)
	request.session.flush()
	return HttpResponseRedirect(request.GET.get('next', '/'))


def relatorios(request):
	pdfkit.from_file('/home/patrick/projeto_p3/projeto_p3/templates/teste.html', 'projeto_p3/templates/pdf/teste.pdf')
	email = EmailMessage(
	'Subject here', 'Here is the message.', 'patrickarsenio@hotmail.com', ["patrickarsenio@gmail.com"])
	email.attach_file('projeto_p3/templates/pdf/teste.pdf')
	email.send()
	return HttpResponse("relatorio exportado.")


def ver_obras(request):
	#user = User.objects.get(username=request.user.get_username())
	obra = obras.objects.all()
	return render (request ,"obra/obras_ver.html",{'obra':obra})
	############################ ver o que acrescentar


class Obra_add(CreatePopupMixin,CreateWithInlinesView):
	model = obras
	fields='__all__'
	template_name='obra/obra_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(Obra_add,self).get_form(ObraForm)
		return form
			

class Obra_Update(UpdateWithInlinesView):
	model = obras
	fields='__all__'
	template_name='obra/obra_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(Obra_Update,self).get_form(ObraForm)
		return form



class Obra_Delete(DeleteView):
    model = obras
    success_url = reverse_lazy('obras_ver')
    
    
def exportar_obra(request):
	utilizador = request.user
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="lista_obras.csv"'
	writer = csv.writer(response)
	writer.writerow(['Nº Obra','Designação','Concelho','Nº Cliente','Função',
		'Empresa','Cliente','Requerente','Empreiteiro','Estado','Periodicidade','Técnico','Auditor',
		'Data de inicio','Data de fim','Observações','Avaliação','Num at'])
	minhas_obras = obras.objects.filter(tecnico=utilizador).values_list('num','designacao','concelho','num_cliente','funcao',
		'empresa','cliente','requerente','empreiteiro','estado','periodicidade','tecnico','auditor',
		'data_inicio','data_fim','observacoes','avaliacao','num_at')
	for x in minhas_obras:
		tecnico = User.objects.get(id=x[11])
		auditor = User.objects.get(id=x[12])
		writer.writerow([x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],tecnico,auditor,x[13],x[14],x[15],x[16],x[17] ])
	return response


def index(request):
	return render (request ,"index.html")


def add_obra(request):
	if request.method == 'POST':
		form = ObraForm(request.POST)
		if form.is_valid():
			print ("")
	else:
		form = ObraForm()
	return render(request,"obra/obra_add_form.html",{'form': form})


def guardar_obra(request):
	if request.method == 'POST':
		form = ObraForm(request.POST)
		if form.is_valid():
			num_obra     = request.POST.get('num', '')
			nome_obra     = request.POST.get('designacao', '')
			concelho_obra = request.POST.get('concelho','')
			num_cliente_obra     = request.POST.get('num_cliente', '')
			funcao_obra     = request.POST.get('funcao', '')
			empresa_obra = request.POST.get('empresa','')
			cliente_obra     = request.POST.get('cliente', '')
			requerente_obra     = request.POST.get('requerente', '')
			empreiteiro_obra = request.POST.get('empreiteiro','')
			estado_obra   = request.POST.get('estado', '')
			periodicidade_obra     = request.POST.get('periodicidade', '')
			tecnico_obra = request.POST.get('tecnico','')
			auditor_obra = request.POST.get('auditor','')
			audit_obra = User.objects.get(id=auditor_obra)
			utili = User.objects.get(id=tecnico_obra)
			data_inicio_obra     = request.POST.get('data_inicio', '')
			data_fim_obra     = request.POST.get('data_fim', '')
			observacoes_obra = request.POST.get('observacoes','')
			avaliacao_obra     = request.POST.get('avaliacao', '')
			num_at_obra     = request.POST.get('num_at', '')
		
			add_obra = obras.objects.create(num=num_obra, designacao=nome_obra,concelho=concelho_obra,num_cliente=num_cliente_obra,funcao=funcao_obra,
			empresa=empresa_obra,cliente=cliente_obra,requerente=requerente_obra,empreiteiro=empreiteiro_obra,estado=estado_obra,
			periodicidade=periodicidade_obra,data_inicio=data_inicio_obra,data_fim=data_fim_obra,
			observacoes=observacoes_obra,avaliacao=avaliacao_obra,num_at=num_at_obra,auditor=audit_obra)
			add_obra.tecnico.add(utili)
			
			return HttpResponseRedirect('/')
	else:
		form = ObraForm()
	return HttpResponse("obra criada.")


def add_auditoria(request):
	ImageFormSet = modelformset_factory(fotos,form=FotosForm,extra=1)
	if request.method == 'POST':
		postForm = AuditoriaForm(initial={"recomendacoes": recomendacoes_seguranca})
		postForm.fields["auditor"] = models.forms.ModelMultipleChoiceField(queryset=obras.objects.filter(auditor=request.user))
		formset = ImageFormSet(queryset=fotos.objects.none())
	else:
		postForm = AuditoriaForm(initial={"recomendacoes": recomendacoes_seguranca})
		postForm.fields["obra"].queryset = obras.objects.filter(auditor__username=request.user)
		formset = ImageFormSet(queryset=fotos.objects.none())
	return render(request, 'adicionar_auditoria.html',{'postForm': postForm, 'formset': formset},)


def guardar_auditoria(request):
	if request.method == 'POST':
		form = AuditoriaForm(request.POST)
		auditor_obra = request.user
		num_auditoria = request.POST.get('num', '')
		data_obra = request.POST.get('data', '')
		utilizador = request.user
		o_obra = request.POST.get('obra', '')
		o_obra2 = obras.objects.get(id=o_obra)
		recomendacoes_obra = request.POST.get('recomendacoes', '')
		trabalhos_obra = request.POST.get('trabalhos','')
		add_auditoria = auditorias(auditor=auditor_obra,data=data_obra,obra=o_obra2,recomendacoes=recomendacoes_obra,
		trabalhos=trabalhos_obra)
		add_auditoria.save()
		num_auditoria2 = auditorias.objects.get(num=add_auditoria.num)		
		for f,x in zip(request.FILES.getlist('form-0-imagem'),request.POST.getlist('form-0-descricao', '')):
			foto_add= fotos(auditoria=num_auditoria2,imagem=f,descricao=x)
			foto_add.save()
		return HttpResponseRedirect('/ver_auditoria')
	else:
		form = AuditoriaForm()
	return HttpResponse("auditoria criada.")



def ver(request, idi):
	if request.method == 'POST':
		form = ObraForm(request.POST)
		if form.is_valid():
			form = ObraForm(initial={'num': idi}) 
	else:
		form = ObraForm(initial={'num': idi}) 
	return render(request,"adicionar_obra.html",{'form': form})


def ver_auditoria(request):
	user = User.objects.get(username=request.user.get_username())
	auditoria_obra = auditorias.objects.filter(auditor=user)
	foto = []
	for x in auditoria_obra:
		foto.append(fotos.objects.filter(auditoria=x))
	return render (request ,"ver_auditoria.html",{'auditoria':auditoria_obra,'fotos':foto})

from reportlab.lib.units import mm
import time


class PageNumCanvas(canvas.Canvas):
	
 
	def __init__(self, *args, **kwargs):
		"""Constructor"""
		canvas.Canvas.__init__(self, *args, **kwargs)
		self.pages = []
 
	def showPage(self):
		"""
		On a page break, add information to the list
		"""
		self.pages.append(dict(self.__dict__))
		self._startPage()
 
	def save(self):
		"""
		Add the page number to each page (page x of y)
		"""
		page_count = len(self.pages)
 
		for page in self.pages:
			self.__dict__.update(page)
			self.draw_page_number(page_count)
			canvas.Canvas.showPage(self)
 
		canvas.Canvas.save(self)
 
	def draw_page_number(self, page_count):
		"""
		Add the page number
		"""
		page = "%s / %s" % (self._pageNumber, page_count)
		self.setFont("Calibri", 9)
		if self._pageNumber == 1:
			self.drawRightString(100*mm, 20*mm, "Junta-se em anexo o registo fotográfico da visita à obra.")
		if self._pageNumber !=1:
		#self.drawRightString(50*mm, 240*mm, "Cliente: ")
		#self.drawRightString(65*mm, 240*mm, cliente)
			self.drawRightString(20*mm, 10*mm, "Obra: ")
			self.drawRightString(35*mm, 10*mm, str(nome_obra))
		self.drawRightString(170*mm, 260*mm, "Data: " + (time.strftime("%d/%m/%Y")))
		self.drawRightString(167*mm, 250*mm, "Auditor: " + (str(auditor)))
		self.drawRightString(200*mm, 10*mm, page)


def gerar_relatorio(request,idi):

	global data_obra,nome_obra,cliente,auditor,outfilepath
	
	cinzaclaro = HexColor('#cdcdb1')
	
	auditoria_obra = auditorias.objects.get(num=idi)
	cliente = auditoria_obra.obra.cliente
	empreiteiro = auditoria_obra.obra.empreiteiro
	auditor = (auditoria_obra.auditor)
	data_obra = (auditoria_obra.data)
	nome_obra = (auditoria_obra.obra)
	trabalhos = (auditoria_obra.trabalhos)
	recomendacoes = (auditoria_obra.recomendacoes)
	foto = fotos.objects.filter(auditoria=auditoria_obra)
	foto2 = fotos.objects.filter(auditoria=auditoria_obra,conformidade="certo.jpg")
	foto3 = fotos.objects.filter(auditoria=auditoria_obra,conformidade="errado.jpg")
	trabalhadores = auditoria_obra.num_trabalhadores
	
	"""acidentes = auditoria_obra.num_acidentes
	solicitado_cump = auditoria_obra.solicitado_cumprido
	solicitado_nao_cump = auditoria_obra.solicitado_nao_cumprido
	nao_conformes = []
	for x in foto3:
		nao_cumprido = x.conformidade_texto
		nao_conformes.append(nao_cumprido)

	conformes = []
	for x in foto2:
		cumprido = x.conformidade_texto
		conformes.append(nao_cumprido)
	"""
	logo_empresa = auditoria_obra.empresa


	pasta_pessoal = str(request.user)
	if not os.path.exists("relatorios/"+pasta_pessoal):
		pp = os.makedirs("relatorios/" + pasta_pessoal)
	ficheiro_pdf = "relatorio_auditoria_"+str(auditoria_obra)+".pdf"
	outfiledir = str("relatorios/"+pasta_pessoal)
	outfilepath = os.path.join( outfiledir, ficheiro_pdf )
	styleSheet = getSampleStyleSheet()
	styleSheet.add(ParagraphStyle(name='TestStyle',
							   fontName='Calibri',
							   fontSize=12,
							   textColor= black,
							   leading=12))
							   
	styleSheet2 = getSampleStyleSheet()
	styleSheet2.add(ParagraphStyle(name='TestStyle2',
							   fontName='Calibri_Bold',
							   fontSize=14,
							   textColor= black,
							   leading=12))
	styleSheet2.add(ParagraphStyle(name='TestStyle3',
							   fontName='Calibri_Bold',
							   fontSize=12,
							   textColor= black,
							   leading=12))
	styleSheet2.add(ParagraphStyle(name='TestStyle4',
							   fontName='Calibri_Bold',
							   fontSize=12,
							   textColor= black,
							   leading=12))
	
	styleN = styleSheet2["TestStyle2"]
	styleN.alignment = TA_CENTER
	
	styleB12 = styleSheet2["TestStyle3"]
	styleB12.alignment = TA_LEFT
	
	styleB12c = styleSheet2["TestStyle4"]
	styleB12c.alignment = TA_CENTER
	
	styleA = styleSheet["TestStyle"]
	styleA.alignment = TA_LEFT
	
	doc = BaseDocTemplate(outfilepath, pagesize=letter)
	texto_branco = Paragraph("<br />",styleN)
	
	"""
	def footer(canvas, doc):
		canvas.saveState()
		P = Paragraph("This is a multi-line footer.  It goes on every page.  ",styleN)
		w, h = P.wrap(doc.width, doc.bottomMargin)
		P.drawOn(canvas, doc.leftMargin, h)
		canvas.restoreState()
		
	
    
	frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,id='normal')
	template = PageTemplate(id='test', frames=frame, onPage=footer)
	doc.addPageTemplates([template])
	"""
	
	def header(canvas, doc, content,img2):
		canvas.saveState()
		w, h = content.wrap(doc.width, doc.topMargin)
		
		w2, h2 = img2.wrap(doc.width, doc.topMargin)
		
		content.drawOn(canvas, 20, doc.height + doc.topMargin - 30)
		
		img2.drawOn(canvas, 200, doc.height + doc.topMargin - 400)
		canvas.restoreState()


	
	frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
	
	
	img_empresa = Image("media/"+logo_empresa)
	img_empresa.drawHeight = 30*mm
	img_empresa.drawWidth = 80*mm
	
	header_content = img_empresa
	###### conseguir imagem transparente para fazer marca de agua
	template = PageTemplate(id='test', frames=frame, onPage=partial(header , content=header_content,img2=header_content))
	
	
	doc.addPageTemplates([template])

	
	elements = []
	
	data=[]
	
	
	####################### tabela nr 1
	
	estilo_tabela3 = [('BOX',(0,0),(-1,-1),2,colors.black),
							("ALIGN", (0,0), (-1, -1), "CENTER"),
							("VALIGN", (0, 0	), (-1,-1), "MIDDLE"),
							('GRID',(-1,-1),(-1,-1),1,colors.black)
							]
							

							
	tabela1 = []
	parcial_trabalhos = Paragraph("AUDITORIA DE SEGURANÇA EM OBRA", styleN)
	tabela1.append([parcial_trabalhos])
	tabela1.append([texto_branco])
	tabela1.append([texto_branco])
	#tabela1.append([data_obra])
	t3 = Table(tabela1,colWidths=[7*inch],rowHeights=(25))
	#t3.setStyle(estilo_tabela3)
	
	###################################    tabela nr 2
	
	
	estilo_cliente = [	("ALIGN", (0, 0), (0, 0), "LEFT"),
						("VALIGN", (0, 1), (0,0), "MIDDLE"),
						#("ALIGN", (0, 1), (-1, -1), "CENTER"),
						#("VALIGN", (0, 1), (-1, -1), "MIDDLE"),
						#("ALIGN", (0, 1), (-1, -1), "CENTER"),
						#("TOPPADDING", (0, 1), (-1, -1), 20),
						#('GRID',(0,1),(-1,-1),1,colors.black),
						#("BOTTOMPADDING", (0, 1), (-1, -1), 20),
						#('BACKGROUND', (0, 1), (1,4), colors.gray)
					]
	tabela2 = []
	tabela2.append([texto_branco])
	obra_texto = Paragraph("Obra: ", styleB12)
	nome_obra_texto = Paragraph(str(nome_obra), styleA)
	tabela2.append([obra_texto,nome_obra_texto])
	cliente_texto = Paragraph("Cliente: ", styleB12)
	nome_cliente = Paragraph(str(cliente), styleA)
	tabela2.append([cliente_texto,nome_cliente])
	cliente_texto = Paragraph("Empreiteiro: ", styleB12)
	nome_empreiteiro_texto = Paragraph(str(empreiteiro), styleA)
	tabela2.append([cliente_texto,nome_empreiteiro_texto])
	t4 = Table(tabela2,colWidths=[80,100],rowHeights=(20),hAlign='LEFT')
	#t4.setStyle(estilo_cliente)

	######################### tabela nr 3 descricao ocorrencias
	estilo_desc = [		
						("ALIGN", (0, 0), (0, 0), "RIGHT"),
						("VALIGN", (0, 0), (0,0), "RIGHT"),
						("ALIGN", (0, 0), (-1, -1), "CENTER"),
						("VALIGN", (0, 0), (-1,-1), "MIDDLE"),
						("TOPPADDING", (0, 0), (-1, -1), 20),
						("BOTTOMPADDING", (0, 0), (-1, -1), 20),
						('GRID',(0,3),(2,5),1,colors.black),
						#('BACKGROUND', (1, 1), (1, 1), colors.gray),
						('BACKGROUND', (0, 3), (2, 3), colors.gray)
					]
	tabela3 = []
	tabela3.append([texto_branco])
	tabela3.append([texto_branco])
	tabela3.append([texto_branco])
	descricao_ocorrencias = Paragraph("Descrição das ocorrências" , styleN)
	#tabela3.append([descricao_ocorrencias])
	trabalhadores_texto = Paragraph("N.º de trabalhadores em obra à data da auditoria: ", styleB12)
	nome_trabalhadores_texto = Paragraph(str(trabalhadores), styleA)
	tabela3.append([trabalhadores_texto])
	tabela3.append([nome_trabalhadores_texto])
	#tabela3.append([trabalhadores,acidentes])
	trabalhos_adecorrer_texto = Paragraph("Trabalhos a decorrer: ", styleB12)
	nome_trabalhos_adecorrer_texto = Paragraph(str(trabalhos), styleA)
	tabela3.append([texto_branco])
	tabela3.append([trabalhos_adecorrer_texto])
	tabela3.append([nome_trabalhos_adecorrer_texto])
	tdesc = Table(tabela3,colWidths=[300],rowHeights=(20),hAlign='LEFT')
	#tdesc.setStyle(estilo_desc)
	
	####################### tabela nr 4
	estilo_tabela4_texto = [
							('GRID',(0,1),(-1,-1),1,colors.black)
					]
	tabela4 = []
	texto_tabela4 = Paragraph("Este relatório tem por base as diversas auditorias realizadas á obra, estando nestas auditorias o responsável em obra e/ou o encarregado.<br /> É também efetuada uma avliação qualitativa parcial relativamente ao mês a que se refere este relatório. Salientamos no entanto que: <br />",styleN)
	solicitado_cumprido = Paragraph("Foi solicidato e cumprido:",styleN)
	solicitado_nao_cumprido = Paragraph("Foi solicidato e não cumprido:",styleN)
	tabela4.append([texto_branco])
	tabela4.append([texto_tabela4])
	tabela4_tab = Table(tabela4,colWidths=[8*inch])
	tabela4_tab.setStyle(estilo_tabela4_texto)
	
	estilo_tabela5_texto = [
							("BOTTOMPADDING", (0, 0), (-1, -1), 20),
							('GRID',(0,1),(-1,-1),1,colors.black)
					]
	tabela5 = []
	tabela5.append([texto_branco])
	

	import re
	"""solicitado_cump_limpo = solicitado_cump.replace('\n', ' ').replace('\r', '')
	solicitado_cump2 =  re.sub("([0-9])", "<br/> \\1", solicitado_cump_limpo)
	solicitado_cump_final = Paragraph('<u>Foi solicidato e cumprido:</u>' + ' <br />' + solicitado_cump2,styleA)
	tabela5.append([solicitado_cump_final])
	
	solicitado_nao_cump_limpo = solicitado_nao_cump.replace('\n', ' ').replace('\r', '')
	solicitado_nao_cump2 =  re.sub("([0-9])", "<br/> \\1", solicitado_nao_cump_limpo)
	solicitado_nao_cump_final = Paragraph('<u>Foi solicidato e não cumprido:</u>' + ' <br />' + solicitado_nao_cump2,styleA)
	tabela5.append([solicitado_nao_cump_final])
	
	
	tabela5_tab = Table(tabela5,colWidths=[577])
	tabela5_tab.setStyle(estilo_tabela5_texto)
	"""
	#########################
	recomenda_obra = Paragraph("MEDIDAS CORRETIVAS A IMPLEMENTAR", styleB12c)
	registo_foto = Paragraph("REGISTO FOTOGRÁFICO", styleB12c)
	data.append([registo_foto, recomenda_obra])

	for i in foto:
		I = Image(i.imagem)
		I.drawHeight = 2.9*inch
		I.drawWidth = 3.5*inch
		conforme = Image(i.conformidade)
		conforme.drawHeight = 0.2*inch 
		conforme.drawWidth = 0.2*inch
		medidas_obra = i.descricao
		#if "errado" in str(i.conformidade):
		#	data.append([[I],medidas_obra])
		data.append([[I],medidas_obra])
		conformidade_texto = i.conformidade_texto
		
		data.append(([conforme,str("sss") + str(conformidade_texto)]))

		
		estilo_tabela = [#('BOX',(0,0),(-1,-1),2,colors.black),
							("ALIGN", (0, 0), (0, 0), "CENTER"),
							("VALIGN", (0, 0), (0,0), "MIDDLE"),
							("ALIGN", (0, 0), (-1, -1), "CENTER"),
							("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
							("ALIGN", (0, 0), (-1, -1), "CENTER"),
							]
					
		style = ParagraphStyle(
			name='Normal',
			fontSize=20,
		)
		
		#elements.append(img_empresa)
		#data e nº obra
		#elements.append(Paragraph(str(auditoria_obra)+ "<br />"+ "<br />"+ "<br />", style=style))
		
		#p = canvas.Canvas("hello.pdf")
		#t = Table(data) 
 
		#t=Table(data)
		Title = Paragraph("<br/>" +"<br/>" +"<br/>" +"<br/>" +"<br/>"  , styleA)
		

		data.append([texto_branco])
		for i in range(len(data)):
			if i%3 != 0:
				estilo_tabela.append(('GRID',(0,0),(1,0),1,colors.black))
				estilo_tabela.append(('GRID',(0,i),(1,i),1,colors.black))
				
			#if i%3 == 0:
				#estilo_tabela.append(('LINEBELOW',(0,i),(1,i),1,colors.black))
		
		t = Table(data)
		t.setStyle(estilo_tabela)
		t._argW[1]=2*inch	
		elements.append(Title)
		
		##########   append das tabelas ao doc principal
		elements.append(t3)
		elements.append(t4)
		elements.append(tdesc)
		#elements.append(tabela4_tab)
		#elements.append(tabela5_tab)
		elements.append(PageBreak())
		#############
		elements.append(Paragraph("<br/>" +"<br/>" +"<br/>" +"<br/>"  , styleA))
		elements.append(t)
		rec = recomendacoes.replace(';', ';<br />')
		recomenda_obra = Paragraph("Recomendações" + "<br />" + rec, styleN)
		data2=[]
		data2.append([texto_branco])
		data2.append([texto_branco])
		data2.append([texto_branco])
		data2.append([texto_branco])
		data2.append([texto_branco])
		data2.append([texto_branco])
		data2.append([texto_branco])

		data2.append(["Recomendações: "])
		data2.append(rec)
		#trabalhos_adecorrer = Paragraph("Trabalhos a decorrer: ", styleN)
		#tabela3.append(["Trabalhos a decorrer: "])
		#tabela3.append([trabalhos])
	
	
		#trabalho_obra = Paragraph("Trabalhos a decorrer" + "<br />" + trabalhos, styleN)
		#data2.append([trabalho_obra])
		t2=Table(data2,hAlign='LEFT')
		
		#elements.append(Title)
		elements.append(PageBreak())
		elements.append(t2)
		
		doc.build(elements,canvasmaker=PageNumCanvas)
	email_utilizador = request.user.email
	email = EmailMessage(
	('Relatorio '+idi +' da obra '+str(nome_obra)), 'Relatório gerado automaticamente através da plataforma web', "patrickarsenio@gmail.com", [email_utilizador])
	email.attach_file(outfilepath)
	email.send()
	return render(request,"relatorio_gerado.html",{"ficheiro_pdf":(outfilepath)})

def ver_pdf(request):
	with open(outfilepath, 'rb') as fh:
		print(outfilepath)
		response = HttpResponse(fh.read(), content_type="application/")
		response['Content-Disposition'] = 'inline; filename=' + os.path.basename(outfilepath)
		return response


def guardar_auditoria_edit(request,num):
	if request.method == 'POST':
		form = AuditoriaForm(request.POST)
		auditor_obra = request.user
		num_auditoria = request.POST.get('num', '')
		data_obra = request.POST.get('data', '')
		utilizador = request.user
		o_obra = request.POST.get('obra', '')
		o_obra2 = obras.objects.get(id=o_obra)
		recomendacoes_obra = request.POST.get('recomendacoes', '')
		trabalhos_obra = request.POST.get('trabalhos','')
		
		
		auditoria_edit= auditorias.objects.get(num=num)
		auditoria_edit.data = data_obra
		auditoria_edit.obra = o_obra2
		auditoria_edit.recomendacoes = recomendacoes_obra
		auditoria_edit.trabalhos = trabalhos_obra
		auditoria_edit.save()
		
		#add_auditoria = auditorias(auditor=auditor_obra,data=data_obra,obra=o_obra2,recomendacoes=recomendacoes_obra,
		#trabalhos=trabalhos_obra)
		#add_auditoria.save()
		#num_auditoria2 = auditorias.objects.get(num=add_auditoria.num)
		
		
		#print(num_auditoria,data_obra,utilizador,o_obra,recomendacoes_obra,trabalhos_obra)
		#prod_perms = produtos_permissoes.objects.get(Produto_id=prod_id,loja=lojas,distribuidor=distribuidores,permissao_ativa=False)

		if "form-1-imagem-clear" in request.POST:
			print ("checkbox")
			#prod_perms.delete()
		#print("merdas " ,request.FILES.getlist('form-0-imagem'))
		for f,x in zip(request.FILES.getlist('form-0-imagem'),request.POST.getlist('form-0-descricao', '')):
			print(f)
			foto_add = fotos(auditoria=auditoria_edit,imagem=f,descricao=x)
			foto_add.save()
		return HttpResponseRedirect('/ver_auditoriaEquipamentosForm')
	else:
		form = AuditoriaForm()
	return HttpResponse("auditoria criada.")


class FotosInline(InlineFormSet):
	model = fotos
	#fields='__all__'
	form_class = FotosForm
	extra = 1
	def __init__(self, *args, **kwargs):
		super(FotosInline, self).__init__(*args, **kwargs)
		self.can_delete = False


#@method_decorator(login_required, name='dispatch')
class Auditoria_add(CreatePopupMixin,CreateWithInlinesView):
	model = auditorias
	fields='__all__'
	inlines = [FotosInline]
	template_name='templates/auditoria_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(Auditoria_add,self).get_form(AuditoriaForm)
		form.fields['tecnico'].queryset = User.objects.filter(username=self.request.user)
		form.fields['obra'].queryset = obras.objects.filter(tecnico=self.request.user)
		return form
	def get_context_data(self, **kwargs):
		context = super(Auditoria_add, self).get_context_data(**kwargs)
		o = obras.objects.filter(tecnico=self.request.user)
		context.update({'obras': o})
		return context
			


class Auditoria_Update(UpdateWithInlinesView):
	model = auditorias
	fields='__all__'
	inlines = [FotosInline]
	template_name='templates/auditoria_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(Auditoria_Update,self).get_form(AuditoriaForm)
		form.fields['tecnico'].queryset = User.objects.filter(username=self.request.user)
		form.fields['obra'].queryset = obras.objects.filter(tecnico=self.request.user)
		return form
	def get_context_data(self, **kwargs):
		context = super(Auditoria_Update, self).get_context_data(**kwargs)
		o = obras.objects.filter(tecnico=self.request.user)
		context.update({'obras': o})
		return context
		


class Auditoria_Delete(DeleteView):
    model = auditorias
    success_url = reverse_lazy('ver-auditoria')

###############################

class EquipamentosAdd(CreatePopupMixin,CreateWithInlinesView):
	model = equipamentos
	fields='__all__'
	template_name='equipamentos/equipamentos_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(EquipamentosAdd,self).get_form(EquipamentosForm)
		return form

class Equipamentos(CreatePopupMixin,CreateWithInlinesView):
	model = equipamentos
	fields='__all__'
	template_name='equipamentos/equipamentos.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
		
def ver_equipamentos(request):
	todos_equipamentos = equipamentos.objects.all()
	return render (request ,"equipamentos/equipamentos_ver.html",{'equipamentos':todos_equipamentos})

############################ teste a fazer



class Equipamentos_Update(UpdateWithInlinesView):
	model = equipamentos
	fields='__all__'
	template_name='equipamentos/equipamentos_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(Equipamentos_Update,self).get_form(EquipamentosForm)
		return form



class Equipamentos_Delete(DeleteView):
    model = equipamentos
    success_url = reverse_lazy('equipamentos_ver')
		
#######################
class Carros(CreatePopupMixin,CreateWithInlinesView):
	model = carros
	fields='__all__'
	template_name='equipamentos/carros.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()


class CarrosAdd(CreatePopupMixin,CreateWithInlinesView):
	model = carros
	fields='__all__'
	template_name='equipamentos/carros_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(CarrosAdd,self).get_form(CarrosForm)
		return form

def ver_carros(request):
	todos_carros = carros.objects.all()
	return render (request ,"equipamentos/carros_ver.html",{'carros':todos_carros})



class Carros_Update(UpdateWithInlinesView):
	model = carros
	fields='__all__'
	template_name='equipamentos/carros_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(Carros_Update,self).get_form(CarrosForm)
		return form



class Carros_Delete(DeleteView):
    model = carros
    success_url = reverse_lazy('carros_ver')
    
#################################################

class CartaoComb(CreatePopupMixin,CreateWithInlinesView):
	model = cartao_comb
	fields='__all__'
	template_name='equipamentos/cartao_comb.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()

		
class CartaoComb_Add(CreatePopupMixin,CreateWithInlinesView):
	model = cartao_comb
	fields='__all__'
	template_name='equipamentos/cartao_comb_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(CartaoComb_Add,self).get_form(CataoCombForm)
		return form

def ver_cartao_comb(request):
	todos_cartaocomb = cartao_comb.objects.all()
	return render (request ,"equipamentos/cartao_comb_ver.html",{'cartao_comb':todos_cartaocomb})



class CartaoComb_Update(UpdateWithInlinesView):
	model = cartao_comb
	fields='__all__'
	template_name='equipamentos/cartao_comb_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(CartaoComb_Update,self).get_form(CataoCombForm)
		return form



class CartaoComb_Delete(DeleteView):
    model = cartao_comb
    success_url = reverse_lazy('cartao_comb_ver')
    
    
    
##################

class Portatil(CreatePopupMixin,CreateWithInlinesView):
	model = portatil
	fields='__all__'
	template_name='equipamentos/portatil.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()

		
class PortatilAdd(CreatePopupMixin,CreateWithInlinesView):
	model = portatil
	fields='__all__'
	template_name='equipamentos/portatil_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(PortatilAdd,self).get_form(PortatilForm)
		return form

def ver_portatil(request):
	todos_portatil = portatil.objects.all()
	return render (request ,"equipamentos/portatil_ver.html",{'portatil':todos_portatil})



class Portatil_Update(UpdateWithInlinesView):
	model = portatil
	fields='__all__'
	template_name='equipamentos/portatil_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(Portatil_Update,self).get_form(PortatilForm)
		return form



class Portatil_Delete(DeleteView):
    model = portatil
    success_url = reverse_lazy('portatil_ver')
    
    
###############
class Telemovel(CreatePopupMixin,CreateWithInlinesView):
	model = telemovel
	fields='__all__'
	template_name='equipamentos/telemovel.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()


class TelemovelAdd(CreatePopupMixin,CreateWithInlinesView):
	model = telemovel
	fields='__all__'
	template_name='equipamentos/telemovel_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(TelemovelAdd,self).get_form(TelemovelForm)
		return form


def ver_telemovel(request):
	todos_telemovel = telemovel.objects.all()
	return render (request ,"equipamentos/telemovel_ver.html",{'telemovel':todos_telemovel})



class Telemovel_Update(UpdateWithInlinesView):
	model = telemovel
	fields='__all__'
	template_name='equipamentos/telemovel_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(Telemovel_Update,self).get_form(TelemovelForm)
		return form



class TelemovelAdd_Delete(DeleteView):
    model = telemovel
    success_url = reverse_lazy('telemovel_ver')

###################################


class Lista_conformidades(LoginRequiredMixin,CreatePopupMixin,CreateWithInlinesView):
	model = lista_conformidades
	fields='__all__'
	template_name='administracao/lista_conformidades.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()

class Lista_conformidadesAdd(GroupRequiredMixin,CreatePopupMixin,CreateWithInlinesView):
	group_required = u"Administracao"
	login_url = '/login/'
	raise_exception = True
	redirect_unauthenticated_users = True
	model = lista_conformidades
	fields='__all__'
	template_name='administracao/lista_conformidades_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(Lista_conformidadesAdd,self).get_form(Lista_conformidadesForm)
		return form

def ver_lista_conformidades(request):
	listaconformidades = lista_conformidades.objects.all()
	return render (request ,"administracao/lista_conformidades_ver.html",{'listaconformidades':listaconformidades})

class Lista_conformidades_Update(UpdateWithInlinesView):
	model = lista_conformidades
	fields='__all__'
	template_name='administracao/lista_conformidades_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(Lista_conformidades_Update,self).get_form(Lista_conformidadesForm)
		return form

class Lista_conformidades_Delete(DeleteView):
    model = lista_conformidades
    success_url = reverse_lazy('lista_conformidades_ver')


def exportar_lista_conformidades(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="lista_conformidades.csv"'
	writer = csv.writer(response)
	writer.writerow(['Número', 'Descrição'])
	listaconformidades = lista_conformidades.objects.all().values_list('id', 'descricao')
	for x in listaconformidades:
		writer.writerow(x)
	return response
###################################


class Descricao_Conformidades(LoginRequiredMixin,CreatePopupMixin,CreateWithInlinesView):
	model = descricao_conformidades
	fields='__all__'
	template_name='administracao/descricao_conformidades.html'
	def get_success_url(self):
		return self.object.get_absolute_url()

class Descricao_conformidadesAdd(GroupRequiredMixin,CreatePopupMixin,CreateWithInlinesView):
	group_required = u"Administracao"
	login_url = '/login/'
	raise_exception = True
	redirect_unauthenticated_users = True
	model = descricao_conformidades
	fields='__all__'
	template_name='administracao/descricao_conformidades_add_form.html'
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(Descricao_conformidadesAdd,self).get_form(Descricao_conformidadesForm)
		return form

def ver_Descricao_conformidades(request):
	descricaoconformidades = descricao_conformidades.objects.all()
	return render (request ,"administracao/descricao_conformidades_ver.html",{'descricaoconformidades':descricaoconformidades})

class Descricao_conformidades_Update(UpdateWithInlinesView):
	model = descricao_conformidades
	fields='__all__'
	template_name='administracao/descricao_conformidades_add_form.html'
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(Descricao_conformidades_Update,self).get_form(Descricao_conformidadesForm)
		return form

class Descricao_conformidades_Delete(DeleteView):
    model = descricao_conformidades
    success_url = reverse_lazy('descricao_conformidades_ver')



#####################################
def exportar_equips(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="lista_equipamentos.csv"'
	writer = csv.writer(response)
	writer.writerow(['Nome', 'Carro', 'Telemovel', 'Portatil','Cartao de Combustivel','Outros' ])
	equips = equipamentos.objects.all().values_list('utilizador', 'carro', 'telemovel', 'portatil','cartao_combustivel','outros')
	for x in equips:
		utilizador = User.objects.get(id=x[0])
		carro = carros.objects.get(id=x[1])
		tele = telemovel.objects.get(id=x[2])
		pc = portatil.objects.get(id=x[3])
		cartao = cartao_comb.objects.get(id=x[4])
		outros = x[5]
		writer.writerow([utilizador, carro, tele, pc, cartao,outros ])
	return response


def exportar_carros(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="lista_carros.csv"'
	writer = csv.writer(response)
	writer.writerow(['Modelo', 'Matricula','Data matricula'])
	carro = carros.objects.all().values_list('modelo', 'matricula','data_matricula')
	for x in carro:
		writer.writerow(x)
	return response



def exportar_cartao_comb(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="lista_cartões.csv"'
	writer = csv.writer(response)
	writer.writerow(['Numero'])
	cartao = cartao_comb.objects.all().values_list('numero')
	for x in cartao:
		writer.writerow(x)
	return response

def exportar_portatil(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="lista_pc.csv"'
	writer = csv.writer(response)
	writer.writerow(['Modelo','Serial number'])
	pc = portatil.objects.all().values_list('modelo','serial_number')
	for x in pc:
		writer.writerow(x)
	return response

def exportar_telemovel(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="lista_pc.csv"'
	writer = csv.writer(response)
	writer.writerow(['Modelo','Serial number','Tarifário'])
	tele = telemovel.objects.all().values_list('modelo','serial_number','tarifario')
	for x in tele:
		writer.writerow(x)
	return response







def teste2(request):
	#request.session.set_expiry(300)
	#titulo = _("Gestao produtos")
	user = request.user
	conformidade = json.loads(request.body.decode('utf-8'))
	conformidade_final = lista_conformidades.objects.get(descricao=conformidade)
	desc_conformidade = descricao_conformidades.objects.get(lista=conformidade_final)
	id_desc_conformidade = desc_conformidade.id
	#lista = list(produtos.objects.filter(loja=lojas,distribuidor=user,produtos_permissoes__pode_distribuir=False,produtos_permissoes__permissao_ativa=True).values())
	return JsonResponse({'desc_conformidade': str(desc_conformidade),'id_desc_conformidade': (id_desc_conformidade)})


def copiar_auditoria(request,idi):
	audit = auditorias.objects.get(num=idi)
	audit.num = None
	audit.save()
	fot = fotos.objects.filter(auditoria=idi)
	obj = auditorias.objects.latest('num')
	for x in fot.all():		
		x.id=None
		x.auditoria=obj
		x.save()
	return redirect('/ver_auditoria/')

def relatorio_mensal(request):
	user = request.user
	obras_user = obras.objects.filter(auditor=user)
	return render(request, "auditorias/relatorio_mensal.html",{"obras_user":obras_user})

def relatorio_mensal_apanhar_mes(request):
	obra_nome = json.loads(request.body.decode('utf-8'))
	obra_final = obras.objects.get(designacao=obra_nome)
	auditorias_obra = auditorias.objects.filter(obra=obra_final)
	meses = []
	for x in auditorias_obra:
		meses.append(x.data.month)
	return JsonResponse({'meses': list(set(meses))})

from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin
############################################################
class TableBarChart(_DrawingEditorMixin,Drawing):
	def __init__(self,width=1000,height=200,*args,**kw):
		Drawing.__init__(self,width,height,*args,**kw)
		self.width = 400
		self.height = 140
		self._add(self,VerticalBarChart(),name='chart',validate=None,desc=None)
		self.chart.y = 20
		self.chart.width = self.width - 21
		self.chart.height = self.height - 24
		for x in lista_aval:
			if x["meses"] == "1":
				self.chart.categoryAxis.categoryNames = ['Janeiro']
				jan = "Janeiro"
				jan_aval = x["avaliacao"]
			elif x["meses"] == "2":
				fev = "Fevereiro"
				fev_aval = x["avaliacao"]
				self.chart.categoryAxis.categoryNames = ['fev']
			elif x["meses"] == "3":
				self.chart.categoryAxis.categoryNames = ['mar']
				mar = "Março"
				mar_aval = x["avaliacao"]
			elif x["meses"] == "4":
				abr = "Abril"
			elif x["meses"] == "5":
				mai = "Maio"
			elif x["meses"] == "6":
				jun = "Junho"
			elif x["meses"] == "7":
				jul = "Julho"
			elif x["meses"] == "8":
				ago = "Agosto"
			elif x["meses"] == "9":
				set = "Setembro"
			elif x["meses"] == "10":
				out = "Outubro"
			elif x["meses"] == "11":
				nov = "Novembro"
			elif x["meses"] == "12":
				dez = "Dezembro"
			#print("mes",x["meses"])
			#print("avaliacao",x["avaliacao"])
			#self.chart.categoryAxis.categoryNames = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
			#										 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
		self.chart.data = [(int(mar_aval),)]

		#print(lista_aval)

		self.chart.categoryAxis.labels.fontSize = 7
#######################################################

def mes_auditoria(request):
	global outfilepath_relatorio_mensal,auditor,nome_obra,lista_aval

	auditor = request.user
	#mes = json.loads(request.body.decode('utf-8'))
	#mes_final = (mes["mes"])
	#obra_mes = (mes["obras"])
	mes = request.POST.get('mes', '')
	obra_mes = request.POST.get('obra', '')
	conforme_texto = request.POST.get('conforme', '')
	nao_conforme_texto = request.POST.get('nao_conforme', '')
	avaliacao = request.POST.get('avaliacao', '')
	avaliacao_texto = request.POST.get('avaliao_parcial', '')
	nome_obra = obras.objects.get(designacao=obra_mes)

	#try:
	try:
		obj = relatorios_mensais.objects.get(obras=nome_obra, meses=mes)
		#if obj:
		#	return HttpResponse("mes ja foi avaliado.")
		#else:
		#	obj = relatorios_mensais(obras=nome_obra, meses=mes, avaliacao=avaliacao)
		#	obj.save()
	except relatorios_mensais.DoesNotExist:
		obj = relatorios_mensais(obras=nome_obra, meses=mes, avaliacao=avaliacao)
		obj.save()

	#p = relatorios_mensais(obras=nome_obra, meses=mes, avaliacao=avaliacao)
	#p.save()

	avaliacao_relatorio = relatorios_mensais.objects.filter(obras=nome_obra).values("meses","avaliacao")
	lista_aval = []
	for aval in avaliacao_relatorio:
		lista_aval.append(aval)
		#print(aval)
	#print(lista_aval)
	auditorias_mes = auditorias.objects.filter(data__month=mes,obra=nome_obra)
	for data in auditorias_mes:
		data_mensal = data.data
	styleSheet = getSampleStyleSheet()
	styleSheet.add(ParagraphStyle(name='TestStyle',
							   fontName='Calibri_Italic',
							   fontSize=12,
							   textColor= black,
							   leading=12))

	styleSheet2 = getSampleStyleSheet()
	styleSheet2.add(ParagraphStyle(name='TestStyle2',
							   fontName='Calibri_Bold',
							   fontSize=14,
							   textColor= blue,
							   leading=12))
	styleSheet2.add(ParagraphStyle(name='TestStyle3',
							   fontName='Calibri_Italic',
							   fontSize=12,
							   textColor= black,
							   leading=12))
	styleSheet2.add(ParagraphStyle(name='TestStyle4',
							   fontName='Calibri_Bold',
							   fontSize=12,
							   textColor= black,
							   leading=12))
	styleSheet2.add(ParagraphStyle(name='TestStyle5',
								   fontName='Calibri_Bold',
								   fontSize=12,
								   textColor=black,
								   leading=12))
	styleSheet2.add(ParagraphStyle(name='TestStyle6',
								   fontName='Calibri_Bold_Italic',
								   fontSize=12,
								   textColor=black,
								   leading=12))
	styleSheet.add(ParagraphStyle(name='TestStyle7',
								  fontName='Calibri_Italic',
								  fontSize=12,
								  textColor=colors.red,
								  leading=12))
	styleSheet.add(ParagraphStyle(name='TestStyle8',
								  fontName='Calibri_Italic',
								  fontSize=12,
								  textColor=colors.green,
								  leading=12))
	styleSheet.add(ParagraphStyle(name='TestStyle9',
								  fontName='Calibri_Italic',
								  fontSize=12,
								  textColor=colors.blue,
								  leading=12))
	styleN = styleSheet2["TestStyle2"]
	#styleN.alignment = TA_CENTER

	styleB12 = styleSheet2["TestStyle3"]
	styleB12.alignment = TA_CENTER

	styleB12_left = styleSheet2["TestStyle3"]
	styleB12_left.alignment = TA_LEFT

	styleB12_left_bold = styleSheet2["TestStyle5"]
	styleB12_left_bold.alignment = TA_LEFT

	styleB12_left_bold_italic = styleSheet2["TestStyle6"]
	styleB12_left_bold_italic.alignment = TA_LEFT

	styleB12_center_bold_italic = styleSheet2["TestStyle6"]
	styleB12_center_bold_italic.alignment = TA_CENTER

	styleB12c = styleSheet2["TestStyle4"]
	styleB12c.alignment = TA_CENTER

	styleA = styleSheet["TestStyle"]
	styleA.alignment = TA_CENTER

	styleA_red = styleSheet["TestStyle7"]
	styleA_red.alignment = TA_CENTER

	styleA_green = styleSheet["TestStyle8"]
	styleA_green.alignment = TA_CENTER

	styleA_blue = styleSheet["TestStyle9"]
	styleA_blue.alignment = TA_CENTER

	texto_branco = Paragraph("<br />",styleN)
	pasta_pessoal = str(request.user)
	if not os.path.exists("relatorios_mensal/"+pasta_pessoal):
		os.makedirs("relatorios_mensal/" + pasta_pessoal)
	ficheiro_pdf = "relatorio_mensal"+  time.strftime("'%d-%m-%Y")+ ".pdf"
	outfiledir = str("relatorios_mensal/"+pasta_pessoal)
	outfilepath_relatorio_mensal = os.path.join( outfiledir, ficheiro_pdf)
	doc = BaseDocTemplate(outfilepath_relatorio_mensal, pagesize=letter)



	def header(canvas, doc, content, img2):
		canvas.saveState()
		w, h = content.wrap(doc.width, doc.topMargin)
		w2, h2 = img2.wrap(doc.width, doc.topMargin)
		content.drawOn(canvas, 20, doc.height + doc.topMargin - 30)
		user = request.user
		img2.drawOn(canvas, 200, doc.height + doc.topMargin - 400)
		canvas.restoreState()


	frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
	logo_empresa = nome_obra.empresa
	img_empresa = Image("media/" + logo_empresa)
	img_empresa.drawHeight = 30 * mm
	img_empresa.drawWidth = 80 * mm
	header_content = img_empresa
	###### conseguir imagem transparente para fazer marca de agua
	template = PageTemplate(id='test', frames=frame,onPage=partial(header, content=header_content, img2=header_content))
	doc.addPageTemplates([template])

	texto_branco = Paragraph("<br />",styleN)

	documento = []
	tabela1 = []
	tabela1.append([texto_branco])
	tabela1.append([texto_branco])
	tabela1.append([texto_branco])
	tabela1.append([texto_branco])
	parcial_trabalhos = ("RELATÓRIO PARCIAL DOS TRABALHOS")
	mes_relatorio = ("Mês: " + (data_mensal).strftime("%B %Y"))
	tabela1.append([parcial_trabalhos])
	tabela1.append([mes_relatorio])

	estilo_tabela1 = [
					  ('GRID', (0, 4), (-1, -1), 1, colors.black),
					  ("ALIGN", (0,4), (-1, -1), "CENTER"),
					  ("VALIGN", (0,4), (-1,-1), "MIDDLE"),
					  ("FONTSIZE", (0,4), (-1,-1), 14),
					  ("FONTSIZE", (0,5), (-1,-1), 12),
					  ('TEXTCOLOR', (0, 4), (0, 4), colors.blue),
					  ('FONTNAME', (0, 4), (0, 5), "Calibri_Bold"),
					  ('BACKGROUND', (0, 4), (0, -1), colors.lightgrey),
					  ]
	t1 = Table(tabela1,colWidths=[350])
	t1.setStyle(estilo_tabela1)

	estilo_tabela2 = [
		('GRID', (0,1), (-1, -1), 1, colors.black),
		("ALIGN", (1, 1), (-1, -1), "CENTER"),
		("VALIGN", (0, 1), (-1, -1), "MIDDLE"),
		('BACKGROUND', (0, 1), (-1, -1), colors.grey),
		('TEXTCOLOR', (0, 1), (0, 3), colors.blue),
		('FONTNAME', (0, 1), (0, 3), "Calibri_Bold"),
		('FONTNAME', (1, 1), (1, 3), "Calibri"),
	]

	tabela2 = []
	tabela2.append([texto_branco])
	tabela2.append(["Dono de obra: ",nome_obra.dono_de_obra])
	tabela2.append(["Obra: ",nome_obra.designacao])
	tabela2.append(["Empreiteiro: ",nome_obra.empreiteiro])
	t2 = Table(tabela2,colWidths=[80,350],hAlign='LEFT')
	t2.setStyle(estilo_tabela2)

	estilo_tabela3 = [
		('GRID', (0, 2), (-1, -1), 1, colors.black),
		("ALIGN", (0, 1), (1, 3), "CENTER"),
		("VALIGN", (0, 1), (1, -1), "MIDDLE"),
		('SPAN', (0, 1), (1, 1)),
		('FONTNAME', (0, 1), (0, 1), "Calibri_Bold"),
		("FONTSIZE", (0, 1), (-1, -1), 12),
		('FONTNAME', (0, 2), (1, 3), "Calibri_Bold"),
		('BACKGROUND', (0, 2), (1, 2), colors.lightgrey),
	]
	tabela3 = []
	tabela3.append([texto_branco])
	tabela3.append(["Descrição das Ocorrências"])
	num_trabalhadores_obra = ("N.º de Trabalhadores estimados em obra")
	acidentes = ("Acidentes/Incidentes")
	tabela3.append([num_trabalhadores_obra,acidentes])
	media_trabalhadores = 0
	for idx, x in enumerate(auditorias_mes):
		idx = idx+1
		if idx < len(auditorias_mes):
			media_trabalhadores += int(x.num_trabalhadores)/idx
	tabela3.append([int(media_trabalhadores),""])
	t3 = Table(tabela3,colWidths=[210,210])
	t3.setStyle(estilo_tabela3)

	estilo_tabela4 = [
		('BOX', (0, 1), (-1, -1), 1, colors.black),
		("ALIGN", (0, 1), (0, 1), "LEFT"),
		("VALIGN", (0, 1), (0, 1), "MIDDLE"),
		('FONTNAME', (0, 1), (0, 1), "Calibri_Italic"),
	]

	tabela4 = []
	tabela4.append([texto_branco])
	#tabela4.append([texto_branco])
	texto_relatorio = Paragraph("""Este relatório tem por base as diversas auditorias realizadas à obra, estando presentes nestas
						auditorias o responsável em obra e/ou o encarregado.<br /> É também efectuada uma avaliação qualitativa parcial 
						relativamente ao mês a que se refere este relatório. Salientamos no entanto que:""",styleB12_left)
	tabela4.append([texto_relatorio])
	t4 = Table(tabela4)
	t4.setStyle(estilo_tabela4)

	estilo_tabela5 = [
		('BOX', (0, 1), (-1, -1), 1, colors.black),
		("ALIGN", (0, 1), (-1, -1), "CENTER"),
		("VALIGN", (0, 1), (-1, -1), "MIDDLE"),
	]

	tabela5 = []
	solicidato_cump = Paragraph("<u>Foi solicitado e cumprido:</u>",styleB12_left_bold)
	empreiteiro_texto = Paragraph(conforme_texto,styleB12_left)
	nota_texto = Paragraph("<u>Nota: As não conformidades acima referidas poderão encontrar-se em resolução de momento.</u>",styleB12_left)
	tabela5.append([texto_branco])
	tabela5.append([solicidato_cump])
	tabela5.append([empreiteiro_texto])
	tabela5.append([nota_texto])
	t5 = Table(tabela5)
	t5.setStyle(estilo_tabela5)

	estilo_tabela6 = [
		('BOX', (0, 1), (-1, -1), 1, colors.black),
		("ALIGN", (0, 1), (-1, -1), "CENTER"),
		("VALIGN", (0, 1), (-1, -1), "MIDDLE"),
	]
	tabela6 = []
	solicitado_nao_cump = Paragraph("<u>Foi solicitado e não totalmente cumprido:</u>", styleB12_left_bold)
	nota_texto = Paragraph("<u>Nota: As não conformidades acima referidas poderão encontrar-se em resolução de momento.</u>",
						   styleB12_left)
	tabela6.append([texto_branco])
	tabela6.append([solicitado_nao_cump])
	empreiteiro_texto2 = Paragraph(nao_conforme_texto, styleB12_left)
	tabela6.append([empreiteiro_texto2])
	tabela6.append([nota_texto])
	t6 = Table(tabela6)
	t6.setStyle(estilo_tabela6)
	documento.append(PageBreak())

	estilo_tabela8 = [

		("ALIGN", (0, 6), (0, 6), "CENTER"),
		("VALIGN", (0, 6), (0, 6), "MIDDLE"),
		('FONTNAME', (0, 6), (0, 6), "Calibri_Bold_Italic"),
		('BACKGROUND', (0, 6), (0, 6), colors.lightgrey),
		('FONTNAME', (0, 9), (0, 9), "Calibri_Italic"),
		('GRID', (0, 11), (4, 12), 1, colors.black),
	]

	tabela8 = []
	tabela8.append([texto_branco])
	tabela8.append([texto_branco])
	tabela8.append([texto_branco])
	tabela8.append([texto_branco])
	tabela8.append([texto_branco])
	tabela8.append([texto_branco])
	tabela8.append(["AVALIAÇÃO PARCIAL DA OBRA EM MATÉRIA DE SEGURANÇA E SAÚDE"])
	tabela8.append([texto_branco])
	tabela8.append([texto_branco])
	tabela8.append([avaliacao_texto])
	t8 = Table(tabela8)
	t8.setStyle(estilo_tabela8)

	estilo_tabela8_1 = [
		("ALIGN", (0, 1), (4, -1), "CENTER"),
		("VALIGN", (0, 1), (4, -1), "MIDDLE"),
		('FONTNAME', (0, 2), (0, -1), "Calibri_Italic"),
		('SPAN', (0, 1), (4, 1)),
		('GRID', (0, 1), (4, -1), 1, colors.black),
	]

	tabela8_1 = []
	tabela8_1.append([texto_branco])
	tabela8_1.append(["AVALIAÇÃO PARCIAL DA OBRA EM MATÉRIA DE SEGURANÇA E SAÚDE"])
	mau =Paragraph("Mau<br />(1)",styleA_red)
	ab_med = Paragraph("Abaixo de médio<br />(2)",styleA)
	med = Paragraph("Médio<br />(3)",styleA_blue)
	ac_med = Paragraph("Acima de médio<br />(4)",styleA)
	bom = Paragraph("Bom<br />(5)",styleA_green)
	tabela8_1.append([mau,ab_med,med,ac_med,bom])
	if avaliacao == "1":
		tabela8_1.append(["X"])
	elif avaliacao == "2":
		tabela8_1.append(["","X"])
	elif avaliacao == "3":
		tabela8_1.append(["","","X"])
	elif avaliacao == "4":
		tabela8_1.append(["","","","X"])
	elif avaliacao == "5":
		tabela8_1.append(["","","","","X"])
	#tabela8_1.append(["GRAFICO"])
	t8_1 = Table(tabela8_1,colWidths=[100,100,100,100,100])
	t8_1.setStyle(estilo_tabela8_1)

	#tabela8_2 = []
	#tabela8_2.append([texto_branco])
	#B = TableBarChart()
	#tabela8_2.append([B])
	#t8_2 = Table(tabela8_2)

	estilo_tabela9 = [
		('BOX', (0, 1), (-1, -1), 1, colors.black),
		("ALIGN", (0, 1), (-1, -1), "CENTER"),
		("VALIGN", (0, 1), (-1, -1), "MIDDLE"),
		('FONTNAME', (0, 2), (0, -1), "Calibri_Italic"),
	]
	tabela9 = []
	tabela9.append([texto_branco])
	rec_seg = Paragraph("""<u>RECOMENDAÇÕES DE SEGURANÇA:</u>""",styleB12_left_bold_italic)
	tabela9.append([rec_seg])
	texto_rec_seg = Paragraph("""Todos os trabalhadores deverão utilizar sempre capacete de protecção e botas de biqueira de aço para além de todos os outros E.P.I.’s específicos para cada actividade;
		<br/>Todas as zonas de potencial risco de queda em altura deverão possuir guarda-corpos em toda a
		sua área, capazes de impedir a queda de pessoas e materiais. Todos os guarda-corpos utilizados
		em obra deverão estar munidos de guarda superior, intermédia e rodapé; Salienta-se que os
		guarda-corpos deverão possuir resistência suficiente para suportar o impacto de trabalhadores ou
		material. Devem ser colocados rodapés, 0.15 m de altura fixado aos montantes, com função de
		prevenir a queda de materiais ou ferramentas a partir do plano de trabalho.
		<br/>Todos os desníveis deverão estar protegidos com protecção colectiva.
		<br/>Todas as extensões que estejam em mau estado de conservação deverão ser retiradas de
		funcionamento e serem substituídas por cabos em bom estado de conservação.
		<br/>É rigorosamente proibido retirar ou modificar qualquer peça ou órgão de protecção original das
		máquinas de corte;
		<br/>Todas as escavações devem manter-se sinalizadas;
		<br/>Todas as ferramentas e equipamentos de trabalho deverão estar em bom estado de conservação
		de modo a garantir a segurança dos seus utilizadores;
		<br/>Todos os quadros eléctricos e pimenteiros deverão ter um pictograma indicador de “Perigo de
		Electrocussão”;
		<br/>Todas as máquinas devem ter protecção contra capotamento e sinais sonoros e luminoso.""",styleB12)
	tabela9.append([texto_rec_seg])
	t9 = Table(tabela9)
	t9.setStyle(estilo_tabela9)

	tabela10 = []
	tabela10.append([texto_branco])
	tabela10.append([texto_branco])
	tabela10.append([texto_branco])
	tabela10.append([texto_branco])
	tabela10.append([texto_branco])
	tabela10.append([texto_branco])
	texto_final = Paragraph("""Salienta-se o facto da responsabilidade da implementação de todas as medidas em matéria
				de Segurança e Saúde solicitadas pelo dono da obra, via Coordenação de Segurança, serem
				sempre da incumbência do Empreiteiro Geral.
				<br/><br/><br/>
				O Coordenador em matéria de Segurança e Saúde não se poderá responsabilizar por
				quaisquer acidentes que derivem das não conformidades transcritas neste documento, sendo
				da responsabilidade do empreiteiro cumprir as mesmas.
				<br/><br/><br/>
				A segurança passa por todos os envolvidos em obra e não só pelos intervenientes directos.
				<br/><br/><br/>
				""",styleB12)
	texto_assinatura = Paragraph("""<b>Coordenador em Matéria de Segurança e Saúde</b>
				<br/><br/><br/>""",styleB12_center_bold_italic)
	nome_texto = Paragraph("""_______________________________________<br/>
				(Eng.º João Estêvão)""",styleB12c)
	tabela10.append([texto_final])
	tabela10.append([texto_assinatura])
	tabela10.append([nome_texto])
	t10 = Table(tabela10)


	estilo_tabela7 = [
		('GRID', (0, 1), (-1, -1), 1, colors.black),
		("ALIGN", (0, 0), (0, 0), "CENTER"),
		("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
		('FONTNAME', (0, -1), (0, -1), "Calibri_Bold"),
		('BACKGROUND', (0, 1), (1, 1), colors.lightgrey),
	]

	tabela7 = []
	tabela7.append([texto_branco])
	recomenda_obra = Paragraph("MEDIDAS CORRETIVAS A IMPLEMENTAR", styleB12c)
	registo_foto = Paragraph("REGISTO FOTOGRÁFICO", styleB12c)
	tabela7.append([registo_foto, recomenda_obra])

	for x in auditorias_mes:
		auditoria_obra = auditorias.objects.get(num=x.num)
		cliente = auditoria_obra.obra.cliente
		empreiteiro = auditoria_obra.obra.empreiteiro
		auditor = (auditoria_obra.auditor)
		data_obra = (auditoria_obra.data)
		nome_obra = (auditoria_obra.obra)
		trabalhos = (auditoria_obra.trabalhos)
		recomendacoes = (auditoria_obra.recomendacoes)
		foto = fotos.objects.filter(auditoria=auditoria_obra)
		foto2 = fotos.objects.filter(auditoria=auditoria_obra,conformidade="certo.jpg")
		foto3 = fotos.objects.filter(auditoria=auditoria_obra,conformidade="errado.jpg")
		trabalhadores = auditoria_obra.num_trabalhadores

		pasta_pessoal = str(request.user)


		for i in foto:
			I = Image(i.imagem)
			I.drawHeight = 2.9*inch
			I.drawWidth = 3.5*inch
			conforme = Image(i.conformidade)
			conforme.drawHeight = 0.2*inch
			conforme.drawWidth = 0.2*inch
			medidas_obra = i.descricao
			conformidade_texto = i.conformidade_texto
			conformidade_t = i.conformidade
			tabela7.append([[I],medidas_obra])
			if conformidade_t == "certo.jpg":
				conformidade_t = "Conforme "
			elif conformidade_t == "errado.jpg":
				conformidade_t = "Não conforme "

			tabela7.append([conforme,str(conformidade_t)+str(conformidade_texto)])

			t7 = Table(tabela7)
			t7.setStyle(estilo_tabela7)
			documento.append(t1)
			documento.append(t2)
			documento.append(t3)
			documento.append(t4)
			documento.append(t5)
			documento.append(t6)
			documento.append(PageBreak())
			documento.append(t7)
			documento.append(PageBreak())
			documento.append(t8)
			documento.append(t8_1)
			#documento.append(t8_2)
			documento.append(t9)
			documento.append(PageBreak())
			documento.append(t10)
		doc.build(documento,canvasmaker=PageNumCanvas)
	return render(request, "auditorias/gerar_relato_mensal.html", {"ficheiro_pdf": (outfilepath_relatorio_mensal)})




###################################
class Empreiteiros(LoginRequiredMixin,CreatePopupMixin,CreateWithInlinesView):
	model = empreiteiros
	fields='__all__'
	template_name='empreitadas/empreiteiros.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()

class EmpreiteirosAdd(GroupRequiredMixin,CreatePopupMixin,CreateWithInlinesView):
	group_required = u"Administracao"
	login_url = '/login/'
	raise_exception = True
	redirect_unauthenticated_users = True
	model = empreiteiros
	fields='__all__'
	template_name='empreitadas/empreiteiros_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(EmpreiteirosAdd,self).get_form(EmpreiteirosForm)
		return form

def ver_Empreiteiros(request):
	todos_empreiteiros = empreiteiros.objects.all()
	return render (request ,"empreitadas/empreiteiros_ver.html",{'empreiteiros':todos_empreiteiros})

class Empreiteiros_Update(UpdateWithInlinesView):
	model = empreiteiros
	fields='__all__'
	template_name='empreitadas/empreiteiros_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(Empreiteiros_Update,self).get_form(EmpreiteirosForm)
		return form

class Empreiteiros_Delete(DeleteView):
    model = empreiteiros
    success_url = reverse_lazy('lista_empreiteiros_ver')
    
################################
class Trabalhadores(LoginRequiredMixin,CreatePopupMixin,CreateWithInlinesView):
	model = trabalhadores
	fields='__all__'
	template_name='empreitadas/trabalhadores.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()

class TrabalhadoresAdd(GroupRequiredMixin,CreatePopupMixin,CreateWithInlinesView):
	group_required = u"Administracao"
	login_url = '/login/'
	raise_exception = True
	redirect_unauthenticated_users = True
	model = trabalhadores
	fields='__all__'
	template_name='empreitadas/trabalhadores_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(TrabalhadoresAdd,self).get_form(TrabalhadoresForm)
		return form

def ver_Trabalhadores(request):
	todos_trabalhadores = trabalhadores.objects.all()
	return render (request ,"empreitadas/trabalhadores_ver.html",{'trabalhadores':todos_trabalhadores})

class Trabalhadores_Update(UpdateWithInlinesView):
	model = trabalhadores
	fields='__all__'
	template_name='empreitadas/trabalhadores_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(Trabalhadores_Update,self).get_form(TrabalhadoresForm)
		return form

class Trabalhadores_Delete(DeleteView):
    model = trabalhadores
    success_url = reverse_lazy('trabalhadores_ver')
    
#########################

class Sub_empreiteiros(LoginRequiredMixin,CreatePopupMixin,CreateWithInlinesView):
	model = sub_empreiteiros
	fields='__all__'
	template_name='empreitadas/sub_empreiteiros.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()

class Sub_empreiteirosAdd(GroupRequiredMixin,CreatePopupMixin,CreateWithInlinesView):
	group_required = u"Administracao"
	login_url = '/login/'
	raise_exception = True
	redirect_unauthenticated_users = True
	model = sub_empreiteiros
	fields='__all__'
	template_name='empreitadas/sub_empreiteiros_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(Sub_empreiteirosAdd,self).get_form(Sub_empreiteirosForm)
		return form

def ver_Sub_empreiteiros(request):
	todos_sub_empreiteiros = sub_empreiteiros.objects.all()
	return render (request ,"empreitadas/sub_empreiteiros_ver.html",{'sub_empreiteiros':todos_sub_empreiteiros})

class Sub_empreiteiros_Update(UpdateWithInlinesView):
	model = sub_empreiteiros
	fields='__all__'
	template_name='empreitadas/sub_empreiteiros_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(Sub_empreiteiros_Update,self).get_form(Sub_empreiteirosForm)
		return form

class Sub_empreiteiros_Delete(DeleteView):
    model = sub_empreiteiros
    success_url = reverse_lazy('sub_empreiteiros_ver')
    
###################

class Empreitada(LoginRequiredMixin,CreatePopupMixin,CreateWithInlinesView):
	model = empreitada
	fields='__all__'
	template_name='empreitadas/empreitada.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()

class EmpreitadaAdd(GroupRequiredMixin,CreatePopupMixin,CreateWithInlinesView):
	group_required = u"Administracao"
	login_url = '/login/'
	raise_exception = True
	redirect_unauthenticated_users = True
	model = empreitada
	fields='__all__'
	template_name='empreitadas/empreitada_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(EmpreitadaAdd,self).get_form(EmpreitadaForm)
		return form

def ver_Empreitada(request):
	todos_empreitada = empreitada.objects.all()
	for x in todos_empreitada:
		emp = empreiteiros.objects.get(nome_empresa=x)
	trabalhadores_emp = trabalhadores.objects.filter(empreiteiro=emp)
	print (trabalhadores_emp)
	return render (request ,"empreitadas/empreitada_ver.html",{'empreitada':todos_empreitada,'trabalhadores':trabalhadores_emp})

class Empreitada_Update(UpdateWithInlinesView):
	model = empreitada
	fields='__all__'
	template_name='empreitadas/empreitada_add_form.html' 
	def get_success_url(self):
		return self.object.get_absolute_url()
	def get_form(self, form_class):
		form = super(Empreitada_Update,self).get_form(EmpreitadaForm)
		return form

class Empreitada_Delete(DeleteView):
    model = empreitada
    success_url = reverse_lazy('empreitada_ver')
    
#####################

def escolher_empreitada(request):
	obra = obras.objects.all()
	return render (request ,"empreitadas/escolher_empreitada.html",{"obras":obra})


def escolher_empreitada2(request):
	empreitada = json.loads(request.body.decode('utf-8'))
	obras_filt = obras.objects.get(designacao=empreitada)
	empreiteiro = empreiteiros.objects.filter(obra=obras_filt).values("nome_empresa")
	return JsonResponse({'obra': list(empreiteiro)})


from reportlab.lib.pagesizes import letter, landscape

def gerar_mapa(request):
	global outfilepath_mapa
	nome_obra = request.POST.get('select1', '')
	empresa = request.POST.get('empreiteiros', '')
	nome_obra_final = obras.objects.get(designacao = nome_obra)
	query = empreiteiros.objects.get(obra=nome_obra_final,nome_empresa=empresa)
	trabalhadores_empresa = trabalhadores.objects.filter(empreiteiro=query)
	
	logo_empresa = nome_obra_final.empresa
	img_empresa = Image("media/"+logo_empresa)
	img_empresa.drawHeight = 25*mm
	img_empresa.drawWidth = 45*mm
	
	############### pdf
	
	def make_landscape(canvas,doc):
		canvas.setPageSize(landscape(letter))
    
	pasta_pessoal = str(request.user)
	if not os.path.exists("empreitadas/"+pasta_pessoal):
		pp = os.makedirs("empreitadas/" + pasta_pessoal)
	ficheiro_pdf = "mapa_"+str(empresa)+ time.strftime("'%d-%m-%Y") + ".pdf"
	#ficheiro_pdf = "empreitadas" + ".pdf"
	outfiledir = str("empreitadas/"+pasta_pessoal)
	outfilepath_mapa = os.path.join( outfiledir, ficheiro_pdf )
	doc = SimpleDocTemplate(outfilepath_mapa, topMargin=2 * cm, bottomMargin=0)
	doc.pagesize = landscape(A4)
	styleSheet = getSampleStyleSheet()
	styleSheet.add(ParagraphStyle(name='TestStyle',
							   fontName='Calibri',
							   fontSize=12,
							   textColor= black,
							   leading=12))
							   
	
	styleN = styleSheet["TestStyle"]
	styleN.alignment = TA_CENTER
	
	estilo_tabela1 = [		
						('GRID',(0,0),(1,1),1,colors.black),
						("ALIGN", (0, 0), (1, 1), "CENTER"),
						("VALIGN", (0, 0), (1,1), "MIDDLE"),
					]

	documento = []
	tabela1 = []
	texto_branco = Paragraph("<br />",styleN)
					
	tabela1.append([img_empresa,"Registo de documentos de empresas e trabalhadores em obra"])
	tabela1.append(["Empreitada",query.obra])
	tabela1.append([texto_branco])
	t1 = Table(tabela1,colWidths=(5*cm, None))
	t1.setStyle(estilo_tabela1)
	documento.append(t1)
	
	tabela2 = []
	tabela2.append(["Empresa",query.nome_empresa])
	tabela2.append(["Morada da sede",query.morada])
	tabela2.append(["Atividade",query.atividade])
	tabela2.append(["Alvará/Titulo de registo (INCI)",query.alvara])
	tabela2.append(["Número de identificação fiscal (NIF)",query.nif])
	tabela2.append(["Representante da empresa","Nome " + query.nome_representante])
	tabela2.append([" ","Contacto " + query.contacto_representante])
	tabela2.append(["Seguro responsabilidade civil","Nº Apólice " + query.num_ap_seguro_resp_civil])
	tabela2.append([" ","Data " + str(query.data_seguro_resp_civil)])
	tabela2.append([" ","Validade " + str(query.validade_seguro_resp_civil)])
	tabela2.append(["Declaração de não dividas SS", "Data " + str(query.data_decl_ss)])
	tabela2.append([" ","Validade "+ str(query.validade_decl_ss)])
	tabela2.append(["Certidão de não dividas às finanças", "Data " + str(query.data_cert_financas)])
	tabela2.append([" ","Validade "+ str(query.validade_cert_financas)])
	tabela2.append(["Folha de férias", "Mês " + query.mes_folha_ferias])
	tabela2.append([" ","Recibo " + query.recibo_folha_ferias])
	tabela2.append(["Horário de trabalho",query.horario_trabalho])
	tabela2.append(["Declaração de adesão ao PSS",query.declaracao_pss])
	tabela2.append(["Declaração de trabalhadores imigrantes",query.declaracao_imigrantes])
	tabela2.append(["Contrato de subempreitada",query.contrato_subempreitada])
	
	tabela3 = []
	tabela3.append(["Seguro de acidentes de trabalho","Companhia" + query.companhia_seguro_trabalho])
	tabela3.append([" ","Nº Apólice " + query.apolice_seguro_trabalho])
	tabela3.append([" ","Modalidade " + query.modalidade_seguro_trabalho])
	tabela3.append([" ","Validade " + str(query.valdade_seguro_trabalho)])

	#tres_meses = datetime.timedelta(6 * 365 / 12)
	validade_seguro_resp_civil_f = datetime.datetime.strptime(query.validade_seguro_resp_civil, '%d/%m/%Y')
	validade_decl_ss_f = datetime.datetime.strptime(query.validade_decl_ss, '%d/%m/%Y')
	validade_cert_financas_f = datetime.datetime.strptime(query.validade_cert_financas, '%d/%m/%Y')
	valdade_seguro_trabalho_f = datetime.datetime.strptime(query.valdade_seguro_trabalho, '%d/%m/%Y')
	#data_i = datetime.datetime.combine(query.data_seguro_resp_civil + tres_meses , datetime.datetime.min.time())
	hoje = datetime.datetime.today()

	estilo_tabela2 = [
		('FONTSIZE', (0, 0), (-1, -1), 6),
		("ALIGN", (-1, -1), (-1, -1), "CENTER"),
		("VALIGN", (-1, -1), (-1, -1), "MIDDLE"),
	]
	estilo_tabela3 = [
		('FONTSIZE', (0, 0), (-1, -1), 6),
	]

	if hoje >= validade_seguro_resp_civil_f:
		estilo_tabela2.append(('BACKGROUND', (1, 9), (1, 9), colors.red),)
	else:
		estilo_tabela2.append(('BACKGROUND', (1, 9), (1, 9), colors.lightgreen),)
	if hoje >= validade_decl_ss_f:
		estilo_tabela2.append(('BACKGROUND', (1, 11), (1, 11), colors.red),)
	else:
		estilo_tabela2.append(('BACKGROUND', (1, 11), (1, 11), colors.lightgreen),)
	if hoje >= validade_cert_financas_f:
		estilo_tabela2.append(('BACKGROUND', (1, 13), (1, 13), colors.red),)
	else:
		estilo_tabela2.append(('BACKGROUND', (1, 13), (13, 13), colors.lightgreen),)
	if hoje >= valdade_seguro_trabalho_f:
		estilo_tabela3.append(('BACKGROUND', (1, 3), (1, 3), colors.red),)
	else:
		estilo_tabela3.append(('BACKGROUND', (1, 3), (1, 3), colors.lightgreen),)

	t2 = Table(tabela2,hAlign='LEFT',rowHeights=(6*mm))
	t2.setStyle(estilo_tabela2)
	t3 = Table(tabela3,rowHeights=(6*mm))
	t3.setStyle(estilo_tabela3)
	estilo_t = [('VALIGN', (0,0), (-1,-1), 'CENTER')]
	t = [[t2,t3]]
	t_final = Table(t) 
	t_final.setStyle(estilo_t)
	documento.append(t_final)
	estilo_tabela4 = [		
						#('GRID',(0,0),(-1,-1),1,colors.black),
						('GRID',(0,0),(-1,0),1,colors.black),
						('BOX',(0,0),(-1,-1),1,colors.black),
						#('LINEBELOW', (0,0), (-1,0), 2, colors.black),
						('GRID',(1,1),(2,1),1,colors.black),
						('GRID',(6,1),(8,1),1,colors.black),
						('GRID',(0,2),(-1,-1),1,colors.black),
						('FONTSIZE', (0, 0), (-1, -1), 6),
						('SPAN',(1,0),(2,0)),
						('SPAN',(6,0),(8,0)),
						#('SPAN',(1,0),(5,0)),
						("ALIGN", (0, 0), (1, 1), "CENTER"),
						("VALIGN", (0, 0), (1,1), "MIDDLE"),
					
					]
	tabela4 = []
	tabela4.append(["Nome","DI","DN","DN","NIF","NISS","Inspeção médica","Inspeção médica",
	"Registo EPIS","Registo EPIS","Registo Formação","CP","Contrato ACT","Seguro de AT","Declaração de manobrador","Carta de riscos (TT)",
	"Idade","Entrada Obra","Saída obra"])
	tabela4.append([" ","Nº","Validade DI"," "," "," ","Resultado","Data","Validade",
		" "," "," "," "," "," "," ",
		" "," "," "])
	
	for x in trabalhadores_empresa:
		tabela4.append([x.nome,x.num_di,x.validade_di,x.dn,x.nif,x.niss,x.resultado_insp_med,x.data_insp_med
		,x.validade_insp_med,x.registo_epis,x.registo_formacao,x.cp,x.contrato_act,x.seguro_at,x.declaracao_manobrador,
		x.carta_riscos,x.idade,x.data_entrada_obra,x.data_saida_obra])
	t4 = Table(tabela4)
	t4.setStyle(estilo_tabela4)
	documento.append(t4)
	doc.build(documento)



	#####################
	return render (request ,"empreitadas/gerar_mapa.html",{'empreiteiros':query,'trabalhadores':trabalhadores_empresa})

def ver_pdf_mapa(request):
	with open(outfilepath_mapa, 'rb') as fh:
		response = HttpResponse(fh.read(), content_type="application/")
		response['Content-Disposition'] = 'inline; filename=' + os.path.basename(outfilepath_mapa)
		return response

def ver_pdf_mensal(request):
	with open(outfilepath_relatorio_mensal, 'rb') as fh:
		response = HttpResponse(fh.read(), content_type="application/")
		response['Content-Disposition'] = 'inline; filename=' + os.path.basename(outfilepath_relatorio_mensal)
		return response
def index_empreitada(request):
	return render (request ,"empreitadas/mapas.html")
	
def comunicacao_previa(request):
	obra = obras.objects.all()
	return render (request ,"empreitadas/comunicacao_previa.html",{"obras":obra})

def gerar_comunicacao_previa(request):
	empreitada = json.loads(request.body.decode('utf-8'))
	obras_filt = obras.objects.get(designacao=empreitada)
	emp = empreiteiros.objects.filter(obra=obras_filt).values()
	return JsonResponse({'obra': list(emp)})

def ver_subempreiteiros(request):
	empreiteiro = json.loads(request.body.decode('utf-8'))
	emp_obj = empreiteiros.objects.get(nome_empresa=empreiteiro)
	sub = empreiteiros.objects.filter(nome_empresa=emp_obj).values("subempreiteiro")
	lista_sub_emp = []
	for x in sub:
		lista_sub_emp.append(list(empreiteiros.objects.filter(id=x.get('subempreiteiro')).values("nome_empresa")))
	print ((lista_sub_emp))
	return JsonResponse({'obra': (lista_sub_emp)})


class PageNumCanvas2(canvas.Canvas):
	def __init__(self, *args, **kwargs):
		canvas.Canvas.__init__(self, *args, **kwargs)
		self.pages = []
 
	def showPage(self):
		self.pages.append(dict(self.__dict__))
		self._startPage()
 
	def save(self):
		page_count = len(self.pages)
 
		for page in self.pages:
			self.__dict__.update(page)
			self.draw_page_number(page_count)
			canvas.Canvas.showPage(self)
		canvas.Canvas.save(self)
 
	def draw_page_number(self, page_count):
		page = "%s / %s" % (self._pageNumber, page_count)
		self.setFont("Calibri", 9)
		self.drawRightString(148.5*mm, 10*mm, page)

def criar_comunicacao_previa(request):
	global outfilepath
	nome_obra = request.POST.get('select1', '')
	empresa = request.POST.get('empreiteiros', '')
	subempresa = request.POST.getlist('subempreiteiros','')
	
	nome_obra_final = obras.objects.get(designacao = nome_obra)
	empresa_query = empreiteiros.objects.get(obra=nome_obra_final,nome_empresa=empresa)
	
	logo_empresa = nome_obra_final.empresa
	img_empresa = Image("media/"+logo_empresa)
	img_empresa.drawHeight = 25*mm
	img_empresa.drawWidth = 45*mm
	
	
	############### pdf
	
	def make_landscape(canvas,doc):
		canvas.setPageSize(landscape(letter))
    
	pasta_pessoal = str(request.user)
	if not os.path.exists("empreitadas/"+pasta_pessoal):
		pp = os.makedirs("empreitadas/" + pasta_pessoal)

	date_string = time.strftime("%Y-%m-%d-%H:%M:%S")
	ficheiro_pdf = "comunicacao_previa"+ datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".pdf"
	#ficheiro_pdf = "comunicacao_previa" + ".pdf"
	outfiledir = str("empreitadas/"+pasta_pessoal)
	outfilepath = os.path.join( outfiledir, ficheiro_pdf )
	doc = SimpleDocTemplate(outfilepath, topMargin=2 * cm, bottomMargin=0)
	doc.pagesize = landscape(A4)
	styleSheet = getSampleStyleSheet()
	styleSheet.add(ParagraphStyle(name='TestStyle',
							   fontName='Calibri',
							   fontSize=6,
							   textColor= black,
							   leading=12))
							   
	
	styleN = styleSheet["TestStyle"]
	styleN.alignment = TA_CENTER
	
	estilo_tabela1 = [		
						('GRID',(0,0),(2,0),1,colors.black),
						("ALIGN", (0, 0), (2, 0), "CENTER"),
						("VALIGN", (0, 0), (2,0), "MIDDLE"),
						('FONTSIZE', (0, 0), (-1, -1), 10),
					]

	documento = []
	tabela1 = []
	texto_branco = Paragraph("<br />",styleN)
					
	tabela1.append([img_empresa,"ATUALIZAÇÃO DA COMUNICAÇÃO PRÉVIA","007_P3_CS"])
	tabela1.append([texto_branco])
	t1 = Table(tabela1,colWidths=(5*cm, None,None),rowHeights=(20*mm))
	t1.setStyle(estilo_tabela1)
	documento.append(t1)
	
	
	estilo_tabela2 = [		
						("VALIGN", (0, 0), (-1,-1), "MIDDLE"),
						('LINEBELOW', (0,0), (-1,-1), 1, colors.black),
						('LINEABOVE', (0,0), (-1,-1), 1, colors.black),
						('BOX', (0,0), (-1,-1), 1, colors.black),
						('INNERGRID', (1,0), (-1,-1), 1, colors.black),
						('FONTSIZE', (0, 0), (-1, -1), 6),
					]
					
	tabela2 = []
	tabela2.append(["Obra:" , str(nome_obra_final),"NIF"])
	tabela2.append(["Dono da Obra:" , str(nome_obra_final.dono_de_obra),str(nome_obra_final.nif_dono_de_obra)])
	tabela2.append(["Empreiteiro Geral:" , str(empresa_query),str(empresa_query.nif)])
	t2 = Table(tabela2,hAlign='LEFT',colWidths=(10*cm, None,None))
	t2.setStyle(estilo_tabela2)
	
	estilo_tabela3 = [('FONTSIZE', (0, 0), (-1, -1), 6),]
					
	tabela3 = []
	tabela3.append(["Data: " , time.strftime("%d/%m/%Y")])
	tabela3.append([texto_branco])
	tabela3.append(["Obra (P3) Nº: ",str(nome_obra_final.num)])
	t3 = Table(tabela3,hAlign='LEFT')
	for i in range(len(tabela3)):
			if i%2 != 0:
				estilo_tabela3.append(('BOX',(0,0),(1,0),1,colors.black))
				estilo_tabela3.append(('BOX',(0,i+1),(1,i+1),1,colors.black))
	t3.setStyle(estilo_tabela3)
	estilo_t = [('VALIGN', (0,0), (-1,-1), 'CENTER')]
	t = [[t2,t3]]
	t_final = Table(t) 
	t_final.setStyle(estilo_t)
	documento.append(t_final)
	
	estilo_tabela4 = [		
						('GRID',(0,2),(-1,-1),1,colors.black),
						('FONTSIZE', (0, 0), (-1, -1), 6),
					]
	tabela4 = []
	tabela4.append([texto_branco])
	tabela4.append([texto_branco])
	tabela4.append(["N.º","Subempreiteiro","Nome do Responsável","Contacto","Contribuinte","Morada","Código Postal","Localidade","Data Início","Termo","Atividade","N.º Alvará"])
	i=1
	for x in subempresa:
		subempresa_query = empreiteiros.objects.get(nome_empresa=x)
		i = round(i+0.1,1)
		tabela4.append([i,subempresa_query,str(subempresa_query.nome_representante),str(subempresa_query.contacto_representante),
		str(subempresa_query.nif),str(subempresa_query.morada),str(subempresa_query.cp),str(subempresa_query.localidade),str("data inicio"),
		str("Final da obra"),str(subempresa_query.atividade),str(subempresa_query.alvara)])
	t4 = Table(tabela4,hAlign='LEFT')
	t4.setStyle(estilo_tabela4)
	texto = Paragraph("""<br /><br />De acordo com o D.L. n.º 273/2003 - Deve a entidade executante organizar um registo atualizado dos
	 subempreiteiros e trabalhadores independentes por si contratados com atividade no estaleiro, bem como
	 fornecer ao dono da obra as informações necessárias""",styleN)
	
	documento.append(t4)
	documento.append(texto)
	
	estilo_tabela5 = [		
						('GRID',(0,1),(-1,-1),1,colors.black),
						("ALIGN", (0, 0), (-1, -1), "CENTER"),
						("VALIGN", (0, 0), (-1,-1), "MIDDLE"),
						('FONTSIZE', (0, 0), (-1, -1), 6),
					]
					
	tabela5 = []
	tabela5.append([texto_branco])
	tabela5.append(["     ","Data",time.strftime("%d/%m/%Y"),"O responsável","   "])
	t5 = Table(tabela5)
	t5.setStyle(estilo_tabela5)
	documento.append(t5)
	doc.build(documento,canvasmaker=PageNumCanvas2)
	return render(request,"relatorio_gerado.html",{"ficheiro_pdf":(outfilepath)})

