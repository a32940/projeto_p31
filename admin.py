from django.contrib import admin
from projeto_p3.models import relatorios_mensais,obras,auditorias,fotos,carros,equipamentos,descricao_conformidades,lista_conformidades,empreiteiros,subempreiteiros
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.http import Http404  
from django import forms
from django.forms import ModelForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.admin import widgets
from django.contrib.admin import AdminSite
from django.http import HttpResponse
from django.utils.translation import ugettext as _



class ImageInline(admin.TabularInline):
    model = fotos

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]


from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .resources import obrasResource

@admin.register(obras)
class PersonAdmin(ImportExportModelAdmin):
	exclude = ('id','dono_de_obra',)

	def get_resource_class(self):
		return obrasResource
    
#admin.site.register(obras)
admin.site.register(auditorias,CategoryAdmin)
admin.site.register(fotos)
admin.site.register(carros)
admin.site.register(relatorios_mensais)
admin.site.register(equipamentos)
admin.site.register(descricao_conformidades)
admin.site.register(lista_conformidades)
admin.site.register(empreiteiros)
admin.site.register(subempreiteiros)

