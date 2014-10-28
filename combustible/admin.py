from django.contrib import admin
from .models import Contrato, Ejecutora, TipoBien, FirmaCargaDatos


admin.site.register(TipoBien)
admin.site.register(Contrato)
admin.site.register(Ejecutora)
admin.site.register(FirmaCargaDatos)
