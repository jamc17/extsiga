# -*- encoding: utf-8 -*-
import json
import hashlib

from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.db import connections

from .models import Contrato, Proveedor, TipoBien, Ejecutora, FirmaCargaDatos


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
				contratoI.especTecnicas = contratoSiga.especTecnicas
				contratoI.fechaContrato = contratoSiga.fechaContrato
				contratoI.fechaInicial = contratoSiga.fechaInicial
				contratoI.fechaFinal = contratoSiga.fechaFinal
				contratoI.idProceso = contratoSiga.idProceso
				contratoI.idContrato = contratoSiga.idContrato
				contratoI.moneda = contratoSiga.moneda
				contratoI.valorMoneda = contratoSiga.valorMoneda
				contratoI.nroConsolidado = contratoSiga.nroConsolidado
				contratoI.anoProceso = contratoSiga.anoProceso
				contratoI.nroProceso = contratoSiga.nroProceso

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


def getEjecutoras(request):
	ejecutoras = list(Ejecutora.objects.all().order_by("secEjec").values())
	
	ejecutorasJson = {
		"data": ejecutoras,
		"success": True
	}
	
	return HttpResponse(json.dumps(ejecutorasJson), "application/json");

def getDetalleEjecutora(request):
	secEjec = request.GET.get("secEjec")
	if secEjec:
		ejecutora = Ejecutora.objects.get(pk = secEjec)
	return render(request, "combustible/detalleEjecutora.html", locals())

def filtrosContratosSiga(request):
	thisYear = datetime.today().year
	years = range(thisYear - 10, thisYear + 1)
	years.sort(reverse= True)
	tiposBien = TipoBien.objects.all().order_by("nombre")

	return render(request, "combustible/filtrosContratosSiga.html", locals())


def getContratosSiga(request):
	year = request.GET.get("anoEje")
	tipoBien = request.GET.get("tipoBien")
	
	if not year:
		year = datetime.today().year

	if not tipoBien:
		tipoBien = TipoBien.objects.all().order_by("nombre")[0].sigla

	contratos = Contrato.objects.filter(estado = 0, anoEje = year, tipoBien = tipoBien).order_by("secContrato")

	return render(request, "combustible/listContratosSiga.html", locals());



def getDetalleContratoSiga(request):
	secContrato = request.GET.get("secContrato")
	if secContrato:
		contrato = Contrato.objects.get(pk = secContrato)

	return render(request, "combustible/detalleContrato.html", locals())


@csrf_exempt
def guardarContratosCombustible(request):
	data = json.loads(request.body)

	respuesta = {
		"estado": True,
		"mensaje": "Contratos de combustible importados correctamente"
	}

	cursorRemote = connections['remote'].cursor()

	try:
		for contrato in data["contratos"]:
			contratoU = Contrato.objects.get(pk = contrato)
			
			# Cargamos el detalle (presupuestal, bienes, CC) del contrato
			cursorRemote.execute("SELECT * FROM SIG_CONTRATOS WHERE SEC_CONTRATO = %s", [contrato])
			print cursorRemote.fetchone()
			
			# contratoU.estado = 1
			contratoU.save()
		cursorRemote.close()

	except:
		respuesta["estado"] = False
		respuesta["mensaje"] = "Error, No se pudo guardar los contratos seleccionados"


	return HttpResponse(json.dumps(respuesta), "application/json")












