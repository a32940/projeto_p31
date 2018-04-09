from table import Table
from django.contrib.auth.models import User
from table.columns import Column
from projeto_p3.models import equipamentos



class TabelaEquipamentos(Table):
	utilizador = Column(field='utilizador', header='utilizador')
	carro = Column(field='carro', header='carro')
	telemovel = Column(field='telemovel', header='telemovel')
	portatil = Column(field='portatil', header='portatil')
	cartao_combustivel = Column(field='cartao_combustivel', header='cartao_combustivel')
	outros = Column(field='outros', header='outros')
	class Meta:
		model = equipamentos


class ButtonsExtensionTable(Table):
	id = Column(field='id', header='Editar/apagar')
	utilizador = Column(field='utilizador', header='utilizador')
	carro = Column(field='carro', header='carro')
	telemovel = Column(field='telemovel', header='telemovel')
	portatil = Column(field='portatil', header='portatil')
	cartao_combustivel = Column(field='cartao_combustivel', header='cartao_combustivel')
	outros = Column(field='outros', header='outros')
	class Meta:
		model = equipamentos
		template_name = 'buttons_table.html'




############ fazer hiperligaçao para editar/apagar
