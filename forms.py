from django import forms
from django.forms import ModelForm,Textarea,TextInput
from django.forms.widgets import HiddenInput
from django.core.exceptions import ValidationError
from django.contrib.auth import (authenticate,get_user_model,login,logout)
from django.contrib.auth.forms import UserChangeForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from projeto_p3.models import descricao_conformidades,empreitada,sub_empreiteiros,trabalhadores,obras,estados,auditorias,fotos,equipamentos,cartao_comb,telemovel,portatil,carros,lista_conformidades,empreiteiros
from django.forms.models import inlineformset_factory
from django_addanother.widgets import AddAnotherWidgetWrapper
from django.urls import reverse_lazy
from extra_views import InlineFormSet


class UserLoginForm(forms.Form):

	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self,*args,**kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("Utilizador inexistente.")
			if not user.check_password(password):
				raise froms.ValidationError("Password errada.")
			if not user.is_active:
				raise forms.ValidationError("Utilizador já nao está ativo.")
		return super (UserLoginForm,self).clean(*args,**kwargs)



class DateInput(forms.DateInput):
    input_type = 'date'



class ObraForm(ModelForm):

	class Meta:
		model = obras
		fields = ['num','designacao','dono_de_obra','nif_dono_de_obra','concelho','num_cliente','funcao',
		'empresa','cliente','requerente','empreiteiro','estado','periodicidade','tecnico','auditor',
		'data_inicio','data_fim','observacoes','avaliacao','num_at']
		widgets = {
			'data_inicio': DateInput(attrs={'type': 'date'}),
			'data_fim': DateInput(attrs={'type': 'date'}),
		}
	def __init__(self, *args, **kwargs):
		super(ObraForm, self).__init__(*args, **kwargs)
		self.fields['empresa'].widget.attrs['class'] = 'w3layouts_select'
		self.fields['estado'].widget.attrs['class'] = 'w3layouts_select'
		self.fields['tecnico'].widget.attrs['class'] = 'w3layouts_select'
		self.fields['auditor'].widget.attrs['class'] = 'w3layouts_select'
		self.fields['data_inicio'].widget.attrs['class'] = 'w3layouts_select'
		self.fields['data_fim'].widget.attrs['class'] = 'w3layouts_select'


class AuditoriaForm(ModelForm):

	class Meta:
		model = auditorias
		fields = ['tecnico','auditor','num','data','obra','num_trabalhadores','recomendacoes','trabalhos','empresa']
		widgets = {
			'solicitado_cumprido':Textarea(attrs={'rows':4, 'cols':15}),
			'solicitado_nao_cumprido':Textarea(attrs={'rows':4, 'cols':15}),
			'data': DateInput(attrs={'type': 'date'}),
			'recomendacoes': Textarea(attrs={'cols': 80, 'rows': 20}),
			'trabalhos': Textarea(attrs={'cols': 20, 'rows': 20}),
			'empresa': forms.HiddenInput(),
			'num_trabalhadores' :TextInput(attrs= {'pattern':'\d*'}),
		}
	def __init__(self, *args, **kwargs):
		super(AuditoriaForm, self).__init__(*args, **kwargs)
		self.fields['tecnico'].widget.attrs['class'] = 'w3layouts_select'
		self.fields['auditor'].widget.attrs['class'] = 'w3layouts_select'
		self.fields['obra'].widget.attrs['class'] = 'w3layouts_select'
		self.fields['data'].widget.attrs['class'] = 'w3layouts_select'
	


class FotosForm(ModelForm):
	class Meta:
		model = fotos
		fields = ('imagem','auditoria','conformidade','conformidade_texto','descricao','conformidade_texto2' )
		widgets = {
			#'descricao': Textarea(attrs={'cols': 10, 'rows': 10}),
			'image': forms.HiddenInput()
		}
	def __init__(self, *args, **kwargs):
		super(FotosForm, self).__init__(*args, **kwargs)
		self.fields['conformidade'].widget.attrs['class'] = 'w3layouts_select'
		self.fields['conformidade_texto'].widget.attrs['class'] = 'w3layouts_select , search_select'
		self.fields['conformidade_texto2'].widget.attrs['class'] = 'w3layouts_select'
		self.fields['descricao'].widget.attrs['class'] = 'w3layouts_select'


class EquipamentosForm(ModelForm):
	class Meta:
		model = equipamentos
		fields ='__all__'
	def __init__(self, *args, **kwargs):
			super(EquipamentosForm, self).__init__(*args, **kwargs)
			self.fields['utilizador'].widget.attrs['class'] = 'w3layouts_select'
			self.fields['carro'].widget.attrs['class'] = 'w3layouts_select'
			self.fields['telemovel'].widget.attrs['class'] = 'w3layouts_select'
			self.fields['portatil'].widget.attrs['class'] = 'w3layouts_select'
			self.fields['cartao_combustivel'].widget.attrs['class'] = 'w3layouts_select'
							
class CarrosForm(ModelForm):
	class Meta:
		model = carros
		fields ='__all__'
		widgets = {
			'data_matricula': DateInput(attrs={'type': 'date'}),
			'data_seguro': DateInput(attrs={'type': 'date'}),
		}
	def __init__(self, *args, **kwargs):
		super(CarrosForm, self).__init__(*args, **kwargs)
		self.fields['matricula'].widget.attrs.update({
			'pattern': '[A-Z-0-9]{2}-[A-Z-0-9]{2}-[A-Z-0-9]{2}',
			'placeholder': 'XX-XX-XX',
			'class':'matricula',
			'style':'text-transform:uppercase',
		})
		self.fields['data_matricula'].widget.attrs.update({
			'class': 'w3layouts_select',
		})
		self.fields['data_seguro'].widget.attrs.update({
			'class': 'w3layouts_select',
		})

class PortatilForm(ModelForm):
	class Meta:
		model = portatil
		fields ='__all__'

class TelemovelForm(ModelForm):
	class Meta:
		model = telemovel
		fields ='__all__'
	def __init__(self, *args, **kwargs):
			super(TelemovelForm, self).__init__(*args, **kwargs)
			self.fields['tarifario'].widget.attrs['class'] = 'w3layouts_select'
			self.fields['numero'].widget.attrs.update({
			'class': 'numero',
		})

class CataoCombForm(ModelForm):
	class Meta:
		model = cartao_comb
		fields ='__all__'

class Lista_conformidadesForm(ModelForm):
	class Meta:
		model = lista_conformidades
		fields='__all__'


class Descricao_conformidadesForm(ModelForm):
	class Meta:
		model = descricao_conformidades
		fields='__all__'
	def __init__(self, *args, **kwargs):
		super(Descricao_conformidadesForm, self).__init__(*args, **kwargs)
		self.fields['lista'].widget.attrs.update({
			'class': 'w3layouts_select',
		})
		self.fields['lista'].label = "Não conformidade"

class EmpreiteirosForm(ModelForm):
	class Meta:
		model = empreiteiros
		fields='__all__'
		labels = {
			"subempreiteiro": "Empreiteiro geral"
		}
		widgets = {
			'data_seguro_resp_civil': DateInput(attrs={'type': 'date'}),
			'data_decl_ss': DateInput(attrs={'type': 'date'}),
			'data_cert_financas': DateInput(attrs={'type': 'date'}),
			'valdade_seguro_trabalho': DateInput(attrs={'type': 'date'}),
		}
	def __init__(self, *args, **kwargs):
		super(EmpreiteirosForm, self).__init__(*args, **kwargs)
		self.fields['validade_seguro_resp_civil'].widget.attrs['readonly'] = True
		self.fields['validade_decl_ss'].widget.attrs['readonly'] = True
		self.fields['validade_cert_financas'].widget.attrs['readonly'] = True
		self.fields['data_seguro_resp_civil'].widget.attrs.update({
			'class': 'w3layouts_select',
		})
		self.fields['data_decl_ss'].widget.attrs.update({
			'class': 'w3layouts_select',
		})
		self.fields['subempreiteiro'].widget.attrs.update({
			'class': 'w3layouts_select',
		})
		self.fields['obra'].widget.attrs.update({
			'class': 'w3layouts_select',
		})
		self.fields['data_cert_financas'].widget.attrs.update({
			'class': 'w3layouts_select',
		})
		self.fields['mes_folha_ferias'].widget.attrs.update({
			'class': 'w3layouts_select',
		})
		self.fields['contrato_subempreitada'].widget.attrs.update({
			'class': 'w3layouts_select',
		})
		self.fields['declaracao_imigrantes'].widget.attrs.update({
			'class': 'w3layouts_select',
		})
		self.fields['declaracao_pss'].widget.attrs.update({
			'class': 'w3layouts_select',
		})
		self.fields['horario_trabalho'].widget.attrs.update({
			'class': 'w3layouts_select',
		})
		self.fields['recibo_folha_ferias'].widget.attrs.update({
			'class': 'w3layouts_select',
		})
		self.fields['valdade_seguro_trabalho'].widget.attrs.update({
			'class': 'w3layouts_select',
		})

class TrabalhadoresForm(ModelForm):
	class Meta:
		model = trabalhadores
		fields='__all__'
		widgets = {
			'data_entrada_obra': DateInput(attrs={'type': 'date'}),
			'data_saida_obra': DateInput(attrs={'type': 'date'}),
			'data_insp_med': DateInput(attrs={'type': 'date'}),
			'validade_di': DateInput(attrs={'type': 'date'}),
		}
	def __init__(self, *args, **kwargs):
			super(TrabalhadoresForm, self).__init__(*args, **kwargs)
			self.fields['empreiteiro'].widget.attrs['class'] = 'w3layouts_select'
			self.fields['resultado_insp_med'].widget.attrs['class'] = 'w3layouts_select'
			self.fields['registo_epis'].widget.attrs['class'] = 'w3layouts_select'
			self.fields['registo_formacao'].widget.attrs['class'] = 'w3layouts_select'
			self.fields['contrato_act'].widget.attrs['class'] = 'w3layouts_select'
			self.fields['seguro_at'].widget.attrs['class'] = 'w3layouts_select'
			self.fields['declaracao_manobrador'].widget.attrs['class'] = 'w3layouts_select'
			self.fields['carta_riscos'].widget.attrs['class'] = 'w3layouts_select'
			self.fields['data_entrada_obra'].widget.attrs['class'] = 'w3layouts_select'
			self.fields['data_saida_obra'].widget.attrs['class'] = 'w3layouts_select'
			self.fields['data_insp_med'].widget.attrs['class'] = 'w3layouts_select'
			self.fields['validade_di'].widget.attrs['class'] = 'w3layouts_select'

class Sub_empreiteirosForm(ModelForm):
	class Meta:
		model = sub_empreiteiros
		fields='__all__'
		
class EmpreitadaForm(ModelForm):
	class Meta:
		model = empreitada
		fields='__all__'

		
		
class RequestModelForm(ModelForm):
    """
    Sub-class the ModelForm to provide an instance of 'request'.
    It also saves the object with the appropriate user.
    """
    def __init__(self, request, *args, **kwargs):
        """ Override init to grab the request object. """
        self.request = request
        super(RequestModelForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        m = super(RequestModelForm, self).save(commit=False)
        m.owner = self.request.user
        if commit:
            m.save()
        return m




class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2
        
        
