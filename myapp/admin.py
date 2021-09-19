from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Representada)
admin.site.register(Produto)
admin.site.register(Cliente)
admin.site.register(Transportadora)
admin.site.register(Acabamento)
admin.site.register(Tecido)
admin.site.register(Assistencia)
admin.site.register(Pedido)
admin.site.register(ItemAssistencia)
admin.site.register(ItemPedido)
admin.site.register(Vendedor)
admin.site.register(FormaPagamento)