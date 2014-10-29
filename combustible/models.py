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


class Contrato(models.Model):
	secContrato = models.CharField(max_length=50, db_column='SEC_CONTRATO', primary_key=True)
	anoEje = models.IntegerField(null=True, db_column='ANO_EJE')
	secEjec = models.IntegerField(null=True, db_column='SEC_EJEC')
	tipoBien = models.CharField(max_length=2, db_column='TIPO_BIEN')
	nroDocumento = models.CharField(max_length=20, null=True, db_column='NRO_DOCUMENTO')
	proveedor = models.ForeignKey(Proveedor, null=True, db_column='PROVEEDOR')
	fechaContrato = models.DateField(null=True, db_column='FECHA') 
	fechaInicial = models.DateField(null=True, db_column='FECHA_INICIAL')
	fechaFinal = models.DateField(null=True, db_column='FECHA_FINAL')
	idProceso = models.CharField(null=True, max_length=10, db_column='ID_PROCESO')
	idContrato = models.CharField(null=True, max_length=10, db_column='ID_CONTRATO')
	moneda = models.CharField(max_length=5, null=True, db_column='MONEDA')
	valorMoneda = models.DecimalField(max_digits=12, null=True, decimal_places=2, db_column='VALOR_MONEDA')
	especTecnicas = models.TextField(max_length=500, null=True, db_column='ESPEC_TECNICAS')
	nroConsolidado = models.IntegerField(null=True, db_column='NRO_CONSOLID')
	anoProceso = models.IntegerField(null=True, db_column='ANO_PROCESO')
	nroProceso = models.IntegerField(null=True, db_column='NRO_PROCESO')
	
	def __unicode__(self):
		return self.secContrato

	class Meta:
		db_table = "SIG_CONTRATOS"


class FirmaCargaDatos(models.Model):
	nombreEntidad = models.CharField(max_length=50, null=True)
	huellaDigital = models.CharField(max_length=50, null=True)

	def __unicode__(self):
		return self.nombreEntidad



