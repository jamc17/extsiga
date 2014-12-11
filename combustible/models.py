from django.db import models

class Ejecutora(models.Model):
	secEjec = models.IntegerField(db_column='sec_ejec', primary_key=True)
	nombre = models.CharField(max_length=250, null=True, db_column='nombre')
	ruc = models.CharField(max_length=11, null=True, db_column='ruc_ejec')
	localidad = models.CharField(max_length=70, null=True, db_column='localidad')
	lugar = models.CharField(max_length=250, null=True, db_column='lugar')
	lugarNum = models.CharField(max_length=15, null=True, db_column='lugar_num')

	def __unicode__(self):
		return self.nombre

	def direccion(self):
		return self.lugar + " " + self.lugarNum

	class Meta:
		db_table = "EJECUTORA"


# class SigEjecutora(models.Model):
# 	secEjec = models.CharField(max_length=50, db_column='sec_ejec', primary_key=True)
# 	ejecutura = models.ForeignKey(Ejecutora, db_column="sec_ejec")

# 	class Meta:
# 		db_table = "SIG_EJECUTORA"


class TipoBien(models.Model):
	nombre = models.CharField(max_length=15)
	sigla = models.CharField(max_length=2)

	def __unicode__(self):
		return self.nombre


class Proveedor(models.Model):
	idProveedor = models.IntegerField(db_column='PROVEEDOR', primary_key=True)
	nroRuc = models.CharField(max_length=11, null=True, db_column='NRO_RUC')
	nombreProv = models.CharField(max_length=250, null=True, db_column='NOMBRE_PROV')

	def __unicode__(self):
		return self.nombreProv

	class Meta:
		db_table = "SIG_CONTRATISTAS"


class CentroCosto(models.Model):
	anoEje = models.IntegerField(db_column='ANO_EJE')
	secEjec = models.IntegerField(db_column='SEC_EJEC')
	centroCosto = models.CharField(max_length=15, db_column="CENTRO_COSTO")
	nombreDepend = models.CharField(max_length=100, db_column="NOMBRE_DEPEND")

	class Meta:
		db_table = "SIG_CENTRO_COSTO"


class Contrato(models.Model):
	secContrato = models.CharField(max_length=50, db_column='SEC_CONTRATO', primary_key=True)
	anoEje = models.IntegerField(null=True, db_column='ANO_EJE')
	secEjec = models.IntegerField(null=True, db_column='SEC_EJEC')
	tipoContrato = models.SmallIntegerField(null=True, db_column='TIPO_CONTRATO')
	nroContrato = models.IntegerField(null=True, db_column='NRO_CONTRATO')
	tipoBien = models.CharField(max_length=2, db_column='TIPO_BIEN')
	nroDocumento = models.CharField(max_length=20, null=True, db_column='NRO_DOCUMENTO')
	proveedor = models.ForeignKey(Proveedor, null=True, db_column='PROVEEDOR')
	fechaContrato = models.DateField(null=True, db_column='FECHA') 
	fechaInicial = models.DateField(null=True, db_column='FECHA_INICIAL')
	fechaFinal = models.DateField(null=True, db_column='FECHA_FINAL')
	idProceso = models.CharField(null=True, max_length=10, db_column='ID_PROCESO')
	idContrato = models.CharField(null=True, max_length=10, db_column='ID_CONTRATO')
	moneda = models.CharField(max_length=5, null=True, db_column='MONEDA')
	valorMoneda = models.DecimalField(max_digits=16, decimal_places=2, null=True, db_column='VALOR_MONEDA')
	especTecnicas = models.TextField(max_length=500, null=True, db_column='ESPEC_TECNICAS')
	nroConsolidado = models.IntegerField(null=True, db_column='NRO_CONSOLID')
	anoProceso = models.IntegerField(null=True, db_column='ANO_PROCESO')
	nroProceso = models.IntegerField(null=True, db_column='NRO_PROCESO')
	estado = models.SmallIntegerField(default = 0)
	
	def __unicode__(self):
		return self.secContrato

	class Meta:
		db_table = "SIG_CONTRATOS"


class ContratoDet(models.Model):
	# anoEje = models.IntegerField(db_column="ANO_EJE")
	# secEjec = models.ForeignKey(Ejecutora, db_column="SEC_EJEC")
	# nroContrato = models.IntegerField(db_column="NRO_CONTRATO")
	contrato = models.ForeignKey(Contrato)
	anoProceso = models.IntegerField(db_column="ANO_PROCESO")
	valorMoneda = models.DecimalField(max_digits=16, decimal_places=2, null=True, db_column='VALOR_MONEDA')

	class Meta:
		db_table = "SIG_CONTRATO_DET"


class ContratoSecuencia(models.Model):
	# contrato = models.ForeignKey(Contrato)
	contratoDet = models.ForeignKey(ContratoDet)
	secFase = models.SmallIntegerField(db_column="SEC_FASE")
	# anoProceso = models.IntegerField(db_column="ANO_PROCESO")
	faseContrato = models.CharField(max_length="1", db_column="FASE_CONTRATO")
	estadoFase = models.CharField(max_length="1", db_column="ESTADO_FASE")
	flagComprometido = models.CharField(max_length="1", db_column="FLAG_COMPROMETIDO")

	class Meta:
		db_table = "SIG_CONTRATO_SECUENCIA"


class ContratoDetPptal(models.Model):
	contratoSecuencia = models.ForeignKey(ContratoSecuencia)
	# anoProceso = models.IntegerField(db_column="ANO_PROCESO")
	# secFase = models.IntegerField(db_column="SEC_FASE")
	# secFase = models.ForeignKey(ContratoSecuencia)
	secDetPptal = models.IntegerField(db_column="SEC_DET_PPTAL")
	fuenteFinanc = models.CharField(max_length="2", db_column="FUENTE_FINANC")
	secFunc = models.IntegerField(max_length="4", db_column="SEC_FUNC")
	clasificador = models.CharField(max_length="20", db_column="CLASIFICADOR")
	valorMoneda = models.DecimalField(max_digits=16, decimal_places=2, db_column="VALOR_MONEDA")
	idClasificador = models.CharField(max_length="10", db_column="ID_CLASIFICADOR")
	
	class Meta:
		db_table = "SIG_CONTRATO_DET_PPTAL"


class ContratoDetDepe(models.Model):
	# contrato = models.ForeignKey(Contrato)
	contratoDetPptal = models.ForeignKey(ContratoDetPptal)
	anoProceso = models.IntegerField(db_column="ANO_PROCESO")
	secFase = models.ForeignKey(ContratoSecuencia)
	secDetPptal = models.IntegerField(db_column="SEC_DET_PPTAL")
	secDetDepe = models.IntegerField(db_column="SEC_DET_DEPE")
	centroCosto = models.CharField(max_length="15")
	valorSoles = models.DecimalField(max_digits=12, decimal_places=2, db_column="VALOR_SOLES")

	class Meta:
		db_table = "SIG_CONTRATO_DET_DEPE"


class CatalogoBienServ(models.Model):
	secEjec = models.IntegerField(db_column='SEC_EJEC')
	tipoBien = models.CharField(max_length=1, db_column='TIPO_BIEN')
	grupoBien = models.CharField(max_length=2, db_column='GRUPO_BIEN')
	claseBien = models.CharField(max_length=2, db_column='CLASE_BIEN')
	familiaBien = models.CharField(max_length=4, db_column='FAMILIA_BIEN')
	itemBien = models.CharField(max_length=4, db_column='ITEM_BIEN')
	nombreItem = models.CharField(max_length=150, db_column='NOMBRE_ITEM')
	codigoItem = models.CharField(max_length=12, db_column='CODIGO_ITEM')
	
	class Meta:
		db_table = "CATALOGO_BIEN_SERV"



class ContratoItem(models.Model):
	contrato = models.ForeignKey(Contrato)
	nroItem = models.IntegerField(db_column="NRO_ITEM")
	item = models.ForeignKey(CatalogoBienServ)
	unidadMedida = models.IntegerField(db_column="UNIDAD_MEDIDA")
	cantidad = models.DecimalField(max_digits=20, decimal_places=6, db_column="CANTIDAD")
	cantidadAdjudica = models.DecimalField(max_digits=20, decimal_places=6, db_column="CANTIDAD_ADJUDICA")
	moneda = models.CharField(max_length=6, db_column="MONEDA")
	precioMoneda = models.DecimalField(max_digits=16, decimal_places=6, db_column="PRECIO_MONEDA")
	valorMoneda = models.DecimalField(max_digits=16, decimal_places=2, db_column="VALOR_MONEDA")
	valorSoles = models.DecimalField(max_digits=16, decimal_places=2, db_column="VALOR_SOLES")
	cantidadAjustada = models.DecimalField(max_digits=20, decimal_places=6, null=True, db_column="CANTIDAD_AJUSTADA")
	valorMonedaAjustado = models.DecimalField(max_digits=16, decimal_places=2, null=True, db_column="VALOR_MONEDA_AJUSTADO")

	class Meta:
		db_table = "SIG_CONTRATO_ITEM"



class FirmaCargaDatos(models.Model):
	nombreEntidad = models.CharField(max_length=50, null=True)
	huellaDigital = models.CharField(max_length=50, null=True)

	def __unicode__(self):
		return self.nombreEntidad



