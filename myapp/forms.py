from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.

from django import forms
from django.forms import ModelForm
from .models import *
from django.forms.models import inlineformset_factory

# ItemAssistenciaFormset = inlineformset_factory(Assistencia, ItemAssistencia, extra=1)
class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'

class ItemPedidoForm(ModelForm):
    class Meta:
        model = ItemPedido
        fields = '__all__'

ItemPedidoInlineFormset = inlineformset_factory(Pedido, ItemPedido, fields='__all__', extra=1)

class AssistenciaForm(ModelForm):
    class Meta:
        model = Assistencia
        fields = '__all__'

class ItemAssistenciaForm(ModelForm):
    class Meta:
        model = ItemAssistencia
        fields = '__all__'

ItemAssistenciaInlineFormset = inlineformset_factory(Assistencia, ItemAssistencia, fields='__all__', extra=1)