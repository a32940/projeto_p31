from django.contrib import admin
from django.urls import path
from projeto_p3.views import (login_page,logout_page,relatorios,ver_obras,index,add_obra,guardar_obra,add_auditoria,guardar_auditoria,
ver,ver_auditoria,gerar_relatorio,guardar_auditoria_edit,Auditoria_Update,Auditoria_Delete,Auditoria_add,EquipamentosAdd,Equipamentos,CarrosAdd,Carros,ver_carros,Carros_Update,Carros_Delete,
CartaoComb,CartaoComb_Add,ver_cartao_comb,CartaoComb_Update,CartaoComb_Delete,Portatil,PortatilAdd,ver_portatil,Portatil_Update,Portatil_Delete,Telemovel,TelemovelAdd,ver_telemovel,
Telemovel_Update,TelemovelAdd_Delete,EquipamentosAdd,Equipamentos,ver_equipamentos,Equipamentos_Update,Equipamentos_Delete,exportar_equips,exportar_carros,exportar_cartao_comb,exportar_portatil,
exportar_telemovel,exportar_obra,Obra_Update,Obra_Delete,Obra_add,Lista_conformidades,Lista_conformidadesAdd,Lista_conformidades_Delete,Lista_conformidades_Update,ver_lista_conformidades,
exportar_lista_conformidades,teste2,copiar_auditoria,ver_pdf,relatorio_mensal,mes_auditoria,EmpreiteirosAdd,ver_Empreiteiros,Empreiteiros_Update,Empreiteiros_Delete,Empreiteiros,
Trabalhadores,TrabalhadoresAdd,ver_Trabalhadores,Trabalhadores_Update,Trabalhadores_Delete,Sub_empreiteiros,Sub_empreiteirosAdd,ver_Sub_empreiteiros,Sub_empreiteiros_Update,Sub_empreiteiros_Delete,
Empreitada,EmpreitadaAdd,ver_Empreitada,Empreitada_Update,Empreitada_Delete,escolher_empreitada,escolher_empreitada2,gerar_mapa,index_empreitada,comunicacao_previa,gerar_comunicacao_previa,
ver_subempreiteiros,criar_comunicacao_previa,ver_pdf_mapa,ver_pdf_mensal,relatorio_mensal_apanhar_mes,Descricao_Conformidades,Descricao_conformidadesAdd,ver_Descricao_conformidades,Descricao_conformidades_Update,Descricao_conformidades_Delete
)
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from projeto_p3.models import descricao_conformidades,empreitada,sub_empreiteiros,trabalhadores,auditorias,carros,cartao_comb,portatil,telemovel,equipamentos,obras,lista_conformidades,empreiteiros
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^chaining/', include('smart_selects.urls')),
    url((r'^$'),index,name="index"),
    url(r'^login/$', login_page),
	url(r'^logout/$', logout_page),
    url(r'gerar_relatorio',relatorios),

    url(r'ver_obras',ver_obras,name='obras_ver'),
    url(r'add_obra',Obra_add.as_view(),name='obras_add'),
	url(r'guardar_obra',guardar_obra),
	path('obra/<int:pk>/', Obra_Update.as_view(model=obras,template_name='obra/obra_add_form.html'), name='obras_update'),
	path('obra/<int:pk>/apagar/', Obra_Delete.as_view(model=obras,template_name='obra/obra_form_delete.html'), name='obras_delete'),

	url(r'^relatorio_mensal/mes_auditoria/mes/ver_pdf_mensal/$', ver_pdf_mensal, name='ver_pdf_mensal'),

	url(r'add_auditoria',add_auditoria),
	url(r'guardar_auditoria',guardar_auditoria),
	url(r'ver_auditoria',ver_auditoria,name='ver-auditoria'),
	url(r'^criar_relatorio_auditoria/ver_pdf_mapa/$',ver_pdf_mapa,name='ver_pdf_mapa'),


	url(r'ver_pdf',ver_pdf,name='ver_pdf'),
	
	url(r'^edit_obras/(?P<idi>\w+)/$',ver),
	
	url(r'^criar_relatorio_auditoria/(?P<idi>\w+)/$',gerar_relatorio),
	url(r'^copiar_auditoria/(?P<idi>\w+)/$',copiar_auditoria),
    url(r'auditoria/add/$', Auditoria_add.as_view(), name='auditor-add'),
	path('auditoria/<int:pk>/', Auditoria_Update.as_view(model=auditorias,template_name='templates/auditoria_form.html'), name='auditor-update'),
	path('auditoria/<int:pk>/delete/', Auditoria_Delete.as_view(model=auditorias,template_name='templates/auditoria_form_delete.html'), name='auditor-delete'),
	
	url(r'^utilizador/password/reset/$', auth_views.password_reset, {'post_reset_redirect' : '/utilizador/password/reset/done/','template_name' : 'password_reset.html'},name="password_reset"),
	url(r'^utilizador/password/reset/done/$',auth_views.password_reset_done,{'template_name' : 'repor_password.html'}),
	url(r'^utilizador/password/reset/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, {'post_reset_redirect' : '/utilizador/password/feito/','template_name' : 'form_reset.html'}, name='password_reset_confirm'),
	url(r'^utilizador/password/feito/$',auth_views.password_reset_complete,{'template_name' : 'reset_completo.html'}),
	
	url(r'equipamentos/$', Equipamentos.as_view(), name='equipamentos'),
	url(r'equipamentos/add/$', EquipamentosAdd.as_view(), name='equipamentos_add'),
	url(r'equipamentos/ver/$', ver_equipamentos, name='equipamentos_ver'),
	path('equipamentos/<int:pk>/', Equipamentos_Update.as_view(model=equipamentos,template_name='equipamentos/equipamentos_add_form.html'), name='equipamentos_update'),
	path('equipamentos/<int:pk>/apagar/', Equipamentos_Delete.as_view(model=equipamentos,template_name='equipamentos/equipamentos_form_delete.html'), name='equipamentos_delete'),
	
	
	url(r'carros/$', Carros.as_view(), name='carros'),
	url(r'carros/add/$', CarrosAdd.as_view(), name='carros_add'),
	url(r'carros/ver/$', ver_carros, name='carros_ver'),
	path('carros/<int:pk>/', Carros_Update.as_view(model=carros,template_name='equipamentos/carros_add_form.html'), name='carro-update'),
	path('carros/<int:pk>/apagar/', Carros_Delete.as_view(model=carros,template_name='equipamentos/carro_form_delete.html'), name='carro-delete'),
	
	url(r'cartao_comb/$', CartaoComb.as_view(), name='cartao_comb'),
	url(r'cartao_comb/add/$', CartaoComb_Add.as_view(), name='cartao_comb_add'),
	url(r'cartao_comb/ver/$', ver_cartao_comb, name='cartao_comb_ver'),
	path('cartao_comb/<int:pk>/', CartaoComb_Update.as_view(model=cartao_comb,template_name='equipamentos/cartao_comb_add_form.html'), name='cartao_comb_update'),
	path('cartao_comb/<int:pk>/apagar/', CartaoComb_Delete.as_view(model=cartao_comb,template_name='equipamentos/cartao_comb_form_delete.html'), name='cartao_comb_delete'),
	
	url(r'portatil/$', Portatil.as_view(), name='portatil'),
	url(r'portatil/add/$', PortatilAdd.as_view(), name='portatil_add'),
	url(r'portatil/ver/$', ver_portatil, name='portatil_ver'),
	path('portatil/<int:pk>/', Portatil_Update.as_view(model=portatil,template_name='equipamentos/portatil_add_form.html'), name='portatil_update'),
	path('portatil/<int:pk>/apagar/', Portatil_Delete.as_view(model=portatil,template_name='equipamentos/portatil_form_delete.html'), name='portatil_delete'),
	
	url(r'telemovel/$', Telemovel.as_view(), name='telemovel'),
	url(r'telemovel/add/$', TelemovelAdd.as_view(), name='telemovel_add'),
	url(r'telemovel/ver/$', ver_telemovel, name='telemovel_ver'),
	path('telemovel/<int:pk>/', Telemovel_Update.as_view(model=telemovel,template_name='equipamentos/telemovel_add_form.html'), name='telemovel_update'),
	path('telemovel/<int:pk>/apagar/', TelemovelAdd_Delete.as_view(model=telemovel,template_name='equipamentos/telemovel_form_delete.html'), name='telemovel_delete'),
	
	url(r'lista_conformidades/$', Lista_conformidades.as_view(), name='lista_conformidades'),
	url(r'lista_conformidades/add/$', Lista_conformidadesAdd.as_view(), name='lista_conformidades_add'),
	url(r'lista_conformidades/ver/$', ver_lista_conformidades, name='lista_conformidades_ver'),
	path('lista_conformidades/<int:pk>/', Lista_conformidades_Update.as_view(model=lista_conformidades,template_name='administracao/lista_conformidades_add_form.html'), name='lista_conformidades_update'),
	path('lista_conformidades/<int:pk>/apagar/', Lista_conformidades_Delete.as_view(model=lista_conformidades,template_name='administracao/lista_conformidades_form_delete.html'), name='lista_conformidades_delete'),

	url(r'descricao_conformidades/$', Descricao_Conformidades.as_view(), name='descricao_conformidades'),
	url(r'descricao_conformidades/add/$', Descricao_conformidadesAdd.as_view(), name='descricao_conformidades_add'),
	url(r'descricao_conformidades/ver/$', ver_Descricao_conformidades, name='descricao_conformidades_ver'),
	path('descricao_conformidades/<int:pk>/', Descricao_conformidades_Update.as_view(model=descricao_conformidades,template_name='administracao/descricao_conformidades_add_form.html'), name='descricao_conformidades_update'),
	path('descricao_conformidades/<int:pk>/apagar/', Descricao_conformidades_Delete.as_view(model=descricao_conformidades,template_name='administracao/descricao_conformidades_form_delete.html'), name='descricao_conformidades_delete'),

	url(r'^exportar/csv/equips/$', exportar_equips),
	url(r'^exportar/csv/carros/c/$', exportar_carros),
	url(r'^exportar/csv/cartao_comb/cc/$', exportar_cartao_comb),
	url(r'^exportar/csv/portatil/p/$', exportar_portatil),
	url(r'^exportar/csv/telemovel/t/$', exportar_telemovel),
	url(r'^exportar/csv/obra/o/$', exportar_obra),
	url(r'^exportar/csv/lista_conformidades/l/$', exportar_lista_conformidades),
	
	url(r'^relatorio_mensal/$', relatorio_mensal),
	url(r'^relatorio_mensal/apanhar_mes/$', relatorio_mensal_apanhar_mes),
	url(r'^relatorio_mensal/mes_auditoria/mes/$', mes_auditoria),

	
	url(r'empreiteiros/$', Empreiteiros.as_view(), name='empreiteiros'),
	url(r'empreiteiros/add/$', EmpreiteirosAdd.as_view(), name='empreiteiros_add'),
	url(r'empreiteiros/ver/$', ver_Empreiteiros, name='empreiteiros_ver'),
	path('empreiteiros/<int:pk>/', Empreiteiros_Update.as_view(model=empreiteiros,template_name='empreitadas/empreiteiros_add_form.html'), name='empreiteiros_update'),
	path('empreiteiros/<int:pk>/apagar/', Empreiteiros_Delete.as_view(model=empreiteiros,template_name='empreitadas/empreiteiros_form_delete.html'), name='empreiteiros_delete'),
	
	url(r'trabalhadores/$', Trabalhadores.as_view(), name='trabalhadores'),
	url(r'trabalhadores/add/$', TrabalhadoresAdd.as_view(), name='trabalhadores_add'),
	url(r'trabalhadores/ver/$', ver_Trabalhadores, name='trabalhadores_ver'),
	path('trabalhadores/<int:pk>/', Trabalhadores_Update.as_view(model=trabalhadores,template_name='empreitadas/trabalhadores_add_form.html'), name='trabalhadores_update'),
	path('trabalhadores/<int:pk>/apagar/', Trabalhadores_Delete.as_view(model=trabalhadores,template_name='empreitadas/trabalhadores_form_delete.html'), name='trabalhadores_delete'),
	
	url(r'sub_empresa/$', Sub_empreiteiros.as_view(), name='sub_empreiteiros'),
	url(r'sub_empresa/add/$', Sub_empreiteirosAdd.as_view(), name='sub_empreiteiros_add'),
	url(r'sub_empresa/ver/$', ver_Sub_empreiteiros, name='sub_empreiteiros_ver'),
	path('sub_empresa/<int:pk>/', Sub_empreiteiros_Update.as_view(model=sub_empreiteiros,template_name='empreitadas/sub_empreiteiros_add_form.html'), name='sub_empreiteiros_update'),
	path('sub_empresa/<int:pk>/apagar/', Sub_empreiteiros_Delete.as_view(model=sub_empreiteiros,template_name='empreitadas/sub_empreiteiros_form_delete.html'), name='sub_empreiteiros_delete'),
	
	
	url(r'index_empreitada/$', index_empreitada, name='index_empreitada'),
	url(r'empreitada/$', Empreitada.as_view(), name='empreitada'),
	url(r'empreitada/add/$', EmpreitadaAdd.as_view(), name='empreitada_add'),
	url(r'empreitada/ver/$', ver_Empreitada, name='empreitada_ver'),
	path('empreitada/<int:pk>/', Empreitada_Update.as_view(model=empreitada,template_name='empreitadas/empreitada_add_form.html'), name='empreitada_update'),
	path('empreitada/<int:pk>/apagar/', Empreitada_Delete.as_view(model=empreitada,template_name='empreitadas/empreitada_form_delete.html'), name='empreitada_delete'),
	url(r'escolher_empreitada/esc/$', escolher_empreitada, name='escolher_empreitada'),

	url(r'^teste2/$', teste2),
	url(r'^escolher_empreitada/empresa/$', escolher_empreitada2),
	url(r'^empreitada/gerar_mapa/$', gerar_mapa),
	url(r'^empreitada/comunicacao_previa/$', comunicacao_previa),
	url(r'^empreitada/gerar_comunicacao/$', gerar_comunicacao_previa),
	url(r'^empreitada/ver_subempreiteiro/$', ver_subempreiteiros),
	url(r'^empreitada/gerar_comunicacao/pdf/$', criar_comunicacao_previa),
	

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
