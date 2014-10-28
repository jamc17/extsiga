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
	anoEje = models.CharField(max_length=4, null=True, db_column='ANO_EJE')
	secEjec = models.IntegerField(null=True, db_column='SEC_EJEC')
	tipoBien = models.CharField(max_length=1, null=True, db_column='TIPO_BIEN')
	nroDocumento = models.CharField(max_length=20, null=True, db_column='NRO_DOCUMENTO')
	proveedor = models.ForeignKey(Proveedor, null=True, db_column='PROVEEDOR')
	glosa = models.TextField(max_length=500, null=True, db_column='GLOSA')
	especTecnicas = models.TextField(max_length=500, null=True, db_column='ESPEC_TECNICAS')

	def __unicode__(self):
		return self.secContrato

	class Meta:
		db_table = "SIG_CONTRATOS"


class TipoBien(models.Model):
	nombre = models.CharField(max_length=15)
	sigla = models.CharField(max_length=2)

	def __unicode__(self):
		return self.nombre


class FirmaCargaDatos(models.Model):
	nombreEntidad = models.CharField(max_length=50, null=True)
	huellaDigital = models.CharField(max_length=50, null=True)

	def __unicode__(self):
		return self.nombreEntidad



