# -*- encoding: utf-8 -*-
import json
import hashlib

from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.db import connections

from .models import Contrato, Proveedor, TipoBien, Ejecutora, FirmaCargaDatos, ContratoDet, ContratoSecuencia, ContratoDetPptal, ContratoItem, CatalogoBienServ


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
				contratoI.tipoContrato = contratoSiga.tipoContrato
				contratoI.nroContrato = contratoSiga.nroContrato
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
	estado = request.GET.get("estado")
	
	if not year:
		year = datetime.today().year

	if not tipoBien:
		tipoBien = TipoBien.objects.all().order_by("nombre")[0].sigla
	if not estado:
		estado = 0

	contratos = Contrato.objects.filter(estado = estado, anoEje = year, tipoBien = tipoBien).order_by("secContrato")

	return render(request, "combustible/listContratosSiga.html", locals());



def getDetalleContratoSiga(request):
	secContrato = request.GET.get("secContrato")
	if secContrato:
		contrato = Contrato.objects.get(pk = secContrato)

	return render(request, "combustible/detalleContrato.html", locals())


def getItemsContrato(request):
	secContrato = request.GET.get("secContrato")
	contrato = Contrato.objects.get(pk = secContrato)
	return render(request, "combustible/itemsContrato.html", locals())


# from psycopg2.extras import DictCursor
@csrf_exempt
def guardarContratosCombustible(request):
	data = json.loads(request.body)

	respuesta = {
		"estado": True,
		"mensaje": "Contratos importados correctamente"
	}

	cursorRemote = connections['remote'].cursor()

	# try:
	for contrato in data["contratos"]:
		contratoU = Contrato.objects.get(pk = contrato)
		
		# Cargamos el detalle (presupuestal, bienes, CC) del contrato
		params = {
			"contrato": contratoU,
			"anoEje": contratoU.anoEje,
			"secEjec": contratoU.secEjec,
			"tipoContrato": contratoU.tipoContrato,
			"nroContrato": contratoU.nroContrato
		}

		# Verificamos que los contratos a importar estén comprometidos
		if verificaCompromisoContrato(cursorRemote, params):
			guardaDetalleContrato(cursorRemote, params)

			guardaSecuenciaContrato(cursorRemote, params)

			guardaDetPptalContrato(cursorRemote, params)

			guardaItemsContrato(cursorRemote, params)
			
			contratoU.estado = 1
			contratoU.save()
	cursorRemote.close()

	# except:
	# 	respuesta["estado"] = False
	# 	respuesta["mensaje"] = "Error, No se pudo guardar los contratos seleccionados"


	return HttpResponse(json.dumps(respuesta), "application/json")


def verificaCompromisoContrato(cursor, params):
	cursor.execute("SELECT * FROM SIG_CONTRATO_SECUENCIA WHERE SEC_EJEC = %s AND ANO_EJE = %s AND TIPO_CONTRATO = %s AND NRO_CONTRATO = %s AND FLAG_COMPROMETIDO = %s", [params["secEjec"], params["anoEje"], params["tipoContrato"], params["nroContrato"], 'S'])

	if cursor.rowcount:
		return True

	return False


def guardaDetalleContrato(cursor, params):
	cursor.execute("SELECT * FROM SIG_CONTRATO_DET WHERE SEC_EJEC = %s AND ANO_EJE = %s AND TIPO_CONTRATO = %s AND NRO_CONTRATO = %s", [params["secEjec"], params["anoEje"], params["tipoContrato"], params["nroContrato"]])
		
	if cursor.rowcount:
		contratosDetRemote = dictfetchall(cursor)
		for contratoDetRemote in contratosDetRemote:
			contratoDet = ContratoDet()
			contratoDet.contrato = params["contrato"]
			contratoDet.anoProceso = contratoDetRemote["ANO_PROCESO"]
			contratoDet.valorMoneda = contratoDetRemote["VALOR_MONEDA"]
			contratoDet.save()


def guardaSecuenciaContrato(cursor, params):
	cursor.execute("SELECT * FROM SIG_CONTRATO_SECUENCIA WHERE SEC_EJEC = %s AND ANO_EJE = %s AND TIPO_CONTRATO = %s AND NRO_CONTRATO = %s", [params["secEjec"], params["anoEje"], params["tipoContrato"], params["nroContrato"]])

	if cursor.rowcount:
		contratosSecRemote = dictfetchall(cursor)
		for contratoSecRemote in contratosSecRemote:
			contratoDet = params["contrato"].contratodet_set.filter(anoProceso = contratoSecRemote["ANO_PROCESO"])[0]

			contratoSec = ContratoSecuencia()
			contratoSec.contratoDet = contratoDet
			contratoSec.secFase = contratoSecRemote["SEC_FASE"]
			contratoSec.faseContrato = contratoSecRemote["FASE_CONTRATO"]
			contratoSec.estadoFase = contratoSecRemote["ESTADO_FASE"]
			contratoSec.flagComprometido = contratoSecRemote["FLAG_COMPROMETIDO"]
			contratoSec.save()


def guardaDetPptalContrato(cursor, params):
	cursor.execute("SELECT * FROM SIG_CONTRATO_DET_PPTAL WHERE SEC_EJEC = %s AND ANO_EJE = %s AND NRO_CONTRATO = %s", [params["secEjec"], params["anoEje"], params["nroContrato"]])

	if cursor.rowcount:
		contratosDetPptalRemote = dictfetchall(cursor)
		for contratoDetPptalRemote in contratosDetPptalRemote:
			contratoSecuencia = params["contrato"].contratodet_set.filter(anoProceso = contratoDetPptalRemote["ANO_PROCESO"])[0].contratosecuencia_set.filter(secFase = contratoDetPptalRemote["SEC_FASE"])[0]

			contratoDetPptal = ContratoDetPptal()
			contratoDetPptal.contratoSecuencia = contratoSecuencia
			contratoDetPptal.secDetPptal = contratoDetPptalRemote["SEC_DET_PPTAL"]
			contratoDetPptal.fuenteFinanc = contratoDetPptalRemote["FUENTE_FINANC"]
			contratoDetPptal.secFunc = contratoDetPptalRemote["SEC_FUNC"]
			contratoDetPptal.clasificador = contratoDetPptalRemote["CLASIFICADOR"]
			contratoDetPptal.valorMoneda = contratoDetPptalRemote["VALOR_MONEDA"]
			contratoDetPptal.idClasificador = contratoDetPptalRemote["ID_CLASIFICADOR"]
			contratoDetPptal.save()


def guardaItemsContrato(cursor, params):
	cursor.execute("SELECT * FROM SIG_CONTRATO_ITEM WHERE SEC_EJEC = %s AND ANO_EJE = %s AND TIPO_CONTRATO = %s AND NRO_CONTRATO = %s", [params["secEjec"], params["anoEje"], params["tipoContrato"], params["nroContrato"]])

	if cursor.rowcount:
		contratoItemsRemote = dictfetchall(cursor)
		for contratoItemRemote in contratoItemsRemote:
			# Insertamos primero los items del contrato
			paramsItem = {
				"secEjec": params["secEjec"],
				"tipoBien": contratoItemRemote["TIPO_BIEN"],
				"grupoBien": contratoItemRemote["GRUPO_BIEN"],
				"claseBien": contratoItemRemote["CLASE_BIEN"],
				"familiaBien": contratoItemRemote["FAMILIA_BIEN"],
				"itemBien": contratoItemRemote["ITEM_BIEN"],
			}
			item = guardarCatalogoBienServ(cursor, paramsItem)

			contratoItem = ContratoItem()
			contratoItem.contrato = params["contrato"]
			contratoItem.nroItem = contratoItemRemote["NRO_ITEM"]
			contratoItem.item = item
			contratoItem.unidadMedida = contratoItemRemote["UNIDAD_MEDIDA"]
			contratoItem.cantidad = contratoItemRemote["CANTIDAD"]
			contratoItem.cantidadAdjudica = contratoItemRemote["CANTIDAD_ADJUDICA"]
			contratoItem.moneda = contratoItemRemote["MONEDA"]
			contratoItem.precioMoneda = contratoItemRemote["PRECIO_MONEDA"]
			contratoItem.valorMoneda = contratoItemRemote["VALOR_MONEDA"]
			contratoItem.valorSoles = contratoItemRemote["VALOR_SOLES"]
			contratoItem.cantidadAjustada = contratoItemRemote["CANTIDAD_AJUSTADA"]
			contratoItem.valorMonedaAjustado = contratoItemRemote["VALOR_MONEDA_AJUSTADO"]
			contratoItem.save()


def guardarCatalogoBienServ(cursor, params):
	items = CatalogoBienServ.objects.filter(secEjec = params["secEjec"], tipoBien = params["tipoBien"], grupoBien = params["grupoBien"], claseBien = params["claseBien"], familiaBien = params["familiaBien"], itemBien = params["itemBien"])

	if not items:
		cursor.execute("SELECT SEC_EJEC, TIPO_BIEN, GRUPO_BIEN, CLASE_BIEN, FAMILIA_BIEN, ITEM_BIEN, NOMBRE_ITEM, CODIGO_ITEM FROM CATALOGO_BIEN_SERV WHERE SEC_EJEC = %s AND TIPO_BIEN = %s AND GRUPO_BIEN = %s AND CLASE_BIEN = %s AND FAMILIA_BIEN = %s and ITEM_BIEN = %s", [params["secEjec"], params["tipoBien"], params["grupoBien"], params["claseBien"], params["familiaBien"], params["itemBien"]])

		itemRemote = dictfetchall(cursor)[0]
		item = CatalogoBienServ()
		item.secEjec = itemRemote["SEC_EJEC"]
		item.tipoBien = itemRemote["TIPO_BIEN"]
		item.grupoBien = itemRemote["GRUPO_BIEN"]
		item.claseBien = itemRemote["CLASE_BIEN"]
		item.familiaBien = itemRemote["FAMILIA_BIEN"]
		item.itemBien = itemRemote["ITEM_BIEN"]
		item.nombreItem = itemRemote["NOMBRE_ITEM"]
		item.codigoItem = itemRemote["CODIGO_ITEM"]
		item.save()
	else:
		item = items[0]

	return item


def dictfetchall(cursor):
    # "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]












