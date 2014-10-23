# -*- encoding: utf-8 -*-
import json

from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render

from .models import Contrato, Proveedor, TipoBien


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


def importarProveedoresSiga():
	proveedoresSiga = Proveedor.objects.using("remote").all()

	respuesta = {}
	try:
		for proveedorSiga in proveedoresSiga:
			proveedorI = Proveedor(idProveedor = proveedorSiga.idProveedor)
			proveedorI.nroRuc = proveedorSiga.nroRuc
			proveedorI.nombreProv = proveedorSiga.nombreProv
			proveedorI.save()

		respuesta["estado"] = True
		respuesta["mensaje"] = "Proveedores cargados correctamente"
	except:
		respuesta["estado"] = False
		respuesta["mensaje"] = "Error durante la carga de proveedores"
	
	return HttpResponse("Proveedores importados correctamente")


def importarContratosSiga(request):
	contratosSiga = Contrato.objects.using("remote").all()

	importarProveedoresSiga()

	respuesta = {}
	# try:
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

	respuesta["estado"] = True
	respuesta["mensaje"] = "Contratos SIGA Importados correctamente !!!"

	# except:
	# 	respuesta["estado"] = False	
	# 	respuesta["mensaje"] = "Error, Error al importar los contratos SIGA"
	

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







