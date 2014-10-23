# -*- encoding: utf-8 -*-
import json
import hashlib

from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers

from .models import Contrato, Proveedor, TipoBien, Ejecutora, FirmaCargaDatos


def filtrosContratosSiga(request):
	thisYear = datetime.today().year
	years = range(thisYear - 15, thisYear + 1)
	year = years.sort(reverse= True)

	tiposBien = TipoBien.objects.all().order_by("nombre")
	

	return render(request, "combustible/filtrosContratosSiga.html", locals())

def listContratosSiga(request):
	# contratos = Contrato.objects.using("remote").all()
	contratos = Contrato.objects.all()

	return render(request, "combustible/listContratosSiga.html", locals())


def registraHuellaDigital(querySet):
	data = serializers.serialize("json", querySet)
	huellaDigital = hashlib.sha1(data).hexdigest()
	firma = FirmaCargaDatos.objects.get(nombreEntidad = querySet.model.__name__)
	firma.huellaDigital = huellaDigital
	firma.save()


def getHuellaDital(querySet):
	data = serializers.serialize("json", querySet)
	huellaDigital = hashlib.sha1(data).hexdigest()
	return huellaDigital

def validaHuellaDital(querySet):
	huellaDigitalActual = getHuellaDital(querySet)
	huellaDigitalUltima = FirmaCargaDatos.objects.get(nombreEntidad = querySet.model.__name__)
	return huellaDigitalActual == huellaDigitalUltima.huellaDigital

def importarEjecutorasSiga():
	ejecutorasSiga = Ejecutora.objects.using("remote").all()

	respuesta = {
		"estado": True,
		"mensaje": "No hay nuevas Unidades Ejecutoras SIGA"
	}
	
	validaHuella = validaHuellaDital(ejecutorasSiga)

	if not validaHuella :
		# print "Carga ejecutoras"
		try:
			for ejecutoraSiga in ejecutorasSiga:
				ejecutoraI = Ejecutora(secEjec = ejecutoraSiga.secEjec)
				ejecutoraI.nombre = ejecutoraSiga.nombre
				ejecutoraI.ruc = ejecutoraSiga.ruc
				ejecutoraI.localidad = ejecutoraSiga.localidad
				ejecutoraI.lugar = ejecutoraSiga.lugar
				ejecutoraI.lugarNum = ejecutoraSiga.lugarNum
				ejecutoraI.save()

			respuesta["mensaje"] = "Unidades Ejecutoras SIGA importadas correctamente"
			# Guardamos la huella digital de las ejecutoras
			registraHuellaDigital(ejecutorasSiga)

		except:
			respuesta["estado"] = False
			respuesta["mensaje"] = "Error en la carga de unidades ejecutoras"

	return respuesta


def importarProveedoresSiga():
	proveedoresSiga = Proveedor.objects.using("remote").all()

	respuesta = {
		"estado": True,
		"mensaje": "No hay nuevos Proveedores SIGA"
	}

	validaHuella = validaHuellaDital(proveedoresSiga)
	if not validaHuella:
		try:
			for proveedorSiga in proveedoresSiga:
				proveedorI = Proveedor(idProveedor = proveedorSiga.idProveedor)
				proveedorI.nroRuc = proveedorSiga.nroRuc
				proveedorI.nombreProv = proveedorSiga.nombreProv
				proveedorI.save()

			respuesta["mensaje"] = "Proveedores SIGA importados correctamente"

			# Guardamos la huella digital de los proveedores
			registraHuellaDigital(proveedoresSiga)
		except:
			respuesta["estado"] = False
			respuesta["mensaje"] = "Error durante la carga de proveedores"
		
	return respuesta


def importarContratosSiga(request):
	contratosSiga = Contrato.objects.using("remote").all()

	resEjec = importarEjecutorasSiga()
	resProv = importarProveedoresSiga()

	respuesta = {
		"estado": True,
		"mensaje": "No hay nuevos Contratos SIGA"
		"asdfasdf": "adfsadfdsaf"
		
	}

	validaHuella = validaHuellaDital(contratosSiga)
	if not validaHuella:
		try:
			for contratoSiga in contratosSiga:
				contratoI = Contrato(secContrato = contratoSiga.secContrato)
				contratoI.anoEje = contratoSiga.anoEje
				contratoI.secEjec = contratoSiga.secEjec
				contratoI.tipoBien = contratoSiga.tipoBien
				contratoI.nroDocumento = contratoSiga.nroDocumento
				contratoI.proveedor = Proveedor.objects.get(pk = contratoSiga.proveedor.pk)
				contratoI.glosa = contratoSiga.glosa
				contratoI.especTecnicas = contratoSiga.especTecnicas
				contratoI.save()

			respuesta["mensaje"] = "Contratos SIGA Importados correctamente !!!"

			registraHuellaDigital(contratosSiga)

		except:
			respuesta["estado"] = False	
			respuesta["mensaje"] = "Error, Error al importar los contratos SIGA"
		
	respuesta["mensaje"] += "<br />" + resEjec["mensaje"] + "<br />" + resProv["mensaje"]

	return HttpResponse(json.dumps(respuesta), "application/json")


import random
def defineProveedoresContratos(request):
	contratos = Contrato.objects.using("remote").all()
	ids = range(1, 2259)

	for contrato in contratos:
		random.shuffle(ids)
		contrato.proveedor = Proveedor.objects.using("remote").get(pk = ids[0])
		contrato.save(using = 'remote')

	return HttpResponse("Proveedores configurados correctamente")







