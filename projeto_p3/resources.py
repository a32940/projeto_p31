from import_export import widgets, fields, resources
from import_export.widgets import ForeignKeyWidget,DateWidget
from .models import obras
from django.conf import settings

class obrasResource(resources.ModelResource):


	class Meta:
		model = obras
		exclude = ('dono_de_obra',)

