# -*- coding: utf-8 -*-

import json
from django.shortcuts import render
from django.http import HttpResponse
from combustible.models import Ejecutora

# Create your views here.
def home(request):
	return render(request, "base/home.html", locals())

def header(request):
	ejecutora = Ejecutora.objects.using("remote").get(pk = 775)
	return render(request, "base/header.html", locals())

def center(request):
	
	return render(request, "base/center.html", locals())

def footer(request):
	
	return render(request, "base/footer.html", locals())

def mainMenu(request):
	items = [{
				'title': "Combustible",
				'store': {'root': {
				        'expanded': True,
				        "children": [
				            {"qtitle": "ContratosSiga", "text": "Contratos Siga", "leaf": True },
				            {"qtitle": "ConsumoMensual", "text": "Consumo Mensual", "leaf": True },
				            {"qtitle": "GeneraCronograma", "text": "Generar Cronograma", "leaf": True },
				            {"qtitle": "Estadisticas", "text": "Estadística de Consumo", "leaf": True },
				        ]
				    }
			    }
		}, {
			'title': "Utilitarios",
			'store': {'root': {
				        'expanded': True,
				        "children": [
				            {"qtitle": "ConsultaDocumentos", "text": "Consultas", "leaf": True },
				            {"qtitle": "Reportes", "text": "Reportes", "leaf": True },
				        ]
				    }
			    }
		}, {
			'title': "Administración",
			'store': {'root': {
				        'expanded': True,
				        "children": [
				            {"text": "Administración", "href": "/admin/" ,"leaf": True},
				            {"text": "Backups", "href": "/phpMyAdmin/" ,"leaf": True},
				        ]
				    }
			    }
		}
	]

	return HttpResponse(json.dumps(items), "application/json")


