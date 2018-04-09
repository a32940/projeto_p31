# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
import os

def validate_file_extension(value):
	"""
	Esta função indica que tipo de ficheiros podem ser enviados para a base de dados. Foi imposta uma restrição permitindo apenas o 
	upload de ficheiros com as extensões *'.jpg'*, *'.png'* e *'.gif'*. Caso o tipo de ficheiro não seja suportado é enviado um alerta.
	
	.. code:: python
	
		ext = os.path.splitext(value.name)[1]
		valid_extensions = ['.jpg', '.png', '.gif']
		if not ext.lower() in valid_extensions:
		raise ValidationError(u'Tipo de ficheiro não suportado.')
		
	"""
	ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
	valid_extensions = ['.jpg', '.png', '.gif']
	if not ext.lower() in valid_extensions:
		raise ValidationError(u'Tipo de ficheiro não suportado.')


def validate_image(fieldfile_obj):
	"""
	Esta função impõe um tamanho limite nos ficheiros enviados para a base de dados. 
	Caso o tamanho do ficheiro seja excedido é enviado um alerta.
	
	.. code:: python
	
		filesize = fieldfile_obj.file.size
		megabyte_limit = 1.0
		if filesize > megabyte_limit*1024*1024:
		raise ValidationError("Tamanho máximo permitido é %sMB" % str(megabyte_limit))
		
	"""
	filesize = fieldfile_obj.file.size
	megabyte_limit = 1.0
	if filesize > megabyte_limit*1024*1024:
		raise ValidationError("Tamanho máximo permitido é %sMB" % str(megabyte_limit))
