from django.shortcuts import render
from django.http import HttpResponse 
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib import messages
import os
from xhtml2pdf import pisa

import datetime


from django.views import generic
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import *
from .forms import *

# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	return render(request, 'index.html')


# - - - - - Representada - - - - -
REPRESENTADA_ORDER_OPTIONS = [
        ['', ''],
        ['nome', 'Nome'],
        ['lastUpdate', 'Última atualização'],
    ]
class RepresentadaListView(generic.ListView):
    model = Representada
    paginate_by = 50

    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '')
        order = self.request.GET.get('orderby', '')
        asc_desc = self.request.GET.get('asc_desc', '')

        if order != '':
            if asc_desc == "desc" and order[0] != '-':
                order = '-' + order
            elif asc_desc == "asc" and order[0] == '-':
                order = order[:1]

        if filter_val != '' and order != '':
            new_context = Representada.objects.filter(
                nome__startswith=filter_val,
            ).order_by(order)
        elif order != '':
            new_context = Representada.objects.all().order_by(order)
        elif filter_val != '':
            new_context = Representada.objects.filter(
                nome__startswith=filter_val,
            )
        else:
            new_context = Representada.objects.all()
        return new_context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_agent = self.request.META['HTTP_USER_AGENT']
        keywords = ['Mobile','Opera Mini','Android']
        if any(word in user_agent for word in keywords):
            context['is_mobile'] = True
        else:
            context['is_mobile'] = False

        context['filter'] = self.request.GET.get('filter', '')
        context['orderby'] = self.request.GET.get('orderby', '')
        context['options'] = REPRESENTADA_ORDER_OPTIONS
        context['asc_desc'] = self.request.GET.get('asc_desc', 'asc')
        context['asc_desc_options'] = [['asc', 'Crescente'],['desc', 'Decrescente']]
        return context
   
class RepresentadaDetailView(generic.DetailView):
    
    model = Representada


# Classes created for the forms challenge
class RepresentadaCreate( CreateView):
    model = Representada
    fields = '__all__'
    success_url = reverse_lazy('representadas')


class RepresentadaUpdate( UpdateView):
    model = Representada
    fields = '__all__'
    success_url = reverse_lazy('representadas')


class RepresentadaDelete( DeleteView):
    model = Representada
    success_url = reverse_lazy('representadas')
    


# - - - - - Pedido - - - - -
PEDIDO_ORDER_OPTIONS = [
        ['', ''],
        ['ordemCompra', 'Ordem Compra'],
        ['lastUpdate', 'Última atualização'],
    ]
class PedidoListView(generic.ListView):
    model = Pedido
    paginate_by = 50

    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '')
        order = self.request.GET.get('orderby', '')
        asc_desc = self.request.GET.get('asc_desc', '')

        if order != '':
            if asc_desc == "desc" and order[0] != '-':
                order = '-' + order
            elif asc_desc == "asc" and order[0] == '-':
                order = order[:1]

        if filter_val != '' and order != '':
            new_context = Pedido.objects.filter(
                ordemCompra__startswith=filter_val,
            ).order_by(order)
        elif order != '':
            new_context = Pedido.objects.all().order_by(order)
        elif filter_val != '':
            new_context = Pedido.objects.filter(
                ordemCompra__startswith=filter_val,
            )
        else:
            new_context = Pedido.objects.all()
        return new_context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_agent = self.request.META['HTTP_USER_AGENT']
        keywords = ['Mobile','Opera Mini','Android']
        if any(word in user_agent for word in keywords):
            context['is_mobile'] = True
        else:
            context['is_mobile'] = False

        context['filter'] = self.request.GET.get('filter', '')
        context['orderby'] = self.request.GET.get('orderby', '')
        context['options'] = PEDIDO_ORDER_OPTIONS
        context['asc_desc'] = self.request.GET.get('asc_desc', 'asc')
        context['asc_desc_options'] = [['asc', 'Crescente'],['desc', 'Decrescente']]
        return context


class PedidoDetailView(generic.DetailView):
    
    model = Pedido




class PedidoCreate( View):
    form_class = PedidoForm
    inline_formset = ItemPedidoInlineFormset
    template_name = 'myapp/pedido_form.html'

    def get_success_url(self):
        return reverse_lazy('pedidos') # kwargs={'pk': self.object.pk}

    def get(self, request, *args, **kwargs):
        """handle form display"""
        form = self.form_class()
        formset = self.inline_formset(instance=Pedido())     
        return render(request,\
            self.template_name,\
            {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        """handle form submission"""
        form = self.form_class(request.POST)
        formset = self.inline_formset(request.POST, instance=Pedido())
        
        valorBruto = 0
        valorIpi = 0
        valorTotal =0
        valorComissao =0
        if form.is_valid():
            # Save the parent
            entity = form.save(commit=True)
            # Save the formset
            for f in formset:
                if f.is_valid():
                    f.clean()
                    # print("CLEAN ",f.cleaned_data)
                    if len(f.cleaned_data) > 0:
                        item = f.save(commit=False)
                        item.pedido = entity
                        valorBruto += item.produto.valor * item.quantidade
                        # print("ITEM: ",item)
                        # print("ENTUTY: ",entity)
                        item.save()
                # print("VALID ",f.is_valid())
                # print("CLEAN ",f.cleaned_data)

            valor_descontos = valorBruto * (( entity.desconto1 + entity.desconto2 + entity.desconto3 + entity.desconto4 + entity.desconto5)/100)
            valor_desconto_aplicado = valorBruto - valor_descontos
            valorIpi = valor_desconto_aplicado * (entity.ipi/100)
            valorTotal = valor_desconto_aplicado + valorIpi
            valorComissao = valorTotal*(entity.porcentagemComissao/100)

            entity.valorBruto = valorBruto
            entity.valorIpi = valorIpi
            entity.valorTotal = valorTotal
            entity.valorComissao = valorComissao
            print("VALORES")
            print(entity.valorBruto,"\n",entity.valorIpi,"\n",entity.valorTotal,"\n",entity.valorComissao,"\n")
            entity.save()

        return HttpResponseRedirect(self.get_success_url())


class PedidoUpdate( UpdateView):
    model = Pedido
    form_class = PedidoForm
    inline_formset = ItemPedidoInlineFormset
    template_name = 'myapp/pedido_form.html'

    def get_success_url(self):
        return reverse_lazy('pedidos') # kwargs={'pk': self.object.pk}

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Pedido, pk=self.kwargs['pk'])
        form = self.form_class(instance=self.object)
        formset = self.inline_formset(instance=self.object)
        return render(request,\
            self.template_name,\
            {'form': form, 'formset': formset})


    def post(self, request, *args, **kwargs):
        """handle form submission"""
        self.object = get_object_or_404(Pedido, pk=self.kwargs['pk'])
        form = self.form_class(request.POST,instance=self.object)
        formset = self.inline_formset(request.POST, instance=self.object)
                        
        if form.is_valid():
            # Save the parent
            entity = form.save()
            # Save the formset
            for f in formset:
                if f.is_valid():
                    f.clean()
                    
                    if len(f.cleaned_data) > 0:
                        f.save()
                

        return HttpResponseRedirect(self.get_success_url())


class PedidoDelete( DeleteView):
    model = Pedido
    success_url = reverse_lazy('pedidos')
    

# - - - - - Produto - - - - -
PRODUTO_ORDER_OPTIONS = [
        ['', ''],
        ['nome', 'Nome'],
        ['lastUpdate', 'Última atualização'],
    ]
class ProdutoListView(generic.ListView):
    model = Produto
    paginate_by = 50

    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '')
        order = self.request.GET.get('orderby', '')
        asc_desc = self.request.GET.get('asc_desc', '')

        if order != '':
            if asc_desc == "desc" and order[0] != '-':
                order = '-' + order
            elif asc_desc == "asc" and order[0] == '-':
                order = order[:1]

        if filter_val != '' and order != '':
            new_context = Produto.objects.filter(
                nome__startswith=filter_val,
            ).order_by(order)
        elif order != '':
            new_context = Produto.objects.all().order_by(order)
        elif filter_val != '':
            new_context = Produto.objects.filter(
                nome__startswith=filter_val,
            )
        else:
            new_context = Produto.objects.all()
        return new_context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_agent = self.request.META['HTTP_USER_AGENT']
        keywords = ['Mobile','Opera Mini','Android']
        if any(word in user_agent for word in keywords):
            context['is_mobile'] = True
        else:
            context['is_mobile'] = False

        context['filter'] = self.request.GET.get('filter', '')
        context['orderby'] = self.request.GET.get('orderby', '')
        context['options'] = PRODUTO_ORDER_OPTIONS
        context['asc_desc'] = self.request.GET.get('asc_desc', 'asc')
        context['asc_desc_options'] = [['asc', 'Crescente'],['desc', 'Decrescente']]
        return context



class ProdutoDetailView(generic.DetailView):
    
    model = Produto


# Classes created for the forms challenge
class ProdutoCreate( CreateView):
    model = Produto
    fields = '__all__'
    success_url = reverse_lazy('produtos')


class ProdutoUpdate( UpdateView):
    model = Produto
    fields = '__all__'
    success_url = reverse_lazy('produtos')


class ProdutoDelete( DeleteView):
    model = Produto
    success_url = reverse_lazy('produtos')
    


# - - - - - Assistencia - - - - -
ASSISTENCIA_ORDER_OPTIONS = [
        ['', ''],
        ['numeroSolicitacao', 'Numero Solicitacao'],
        ['lastUpdate', 'Última atualização'],
    ]
class AssistenciaListView(generic.ListView):
    model = Assistencia
    paginate_by = 50

    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '')
        order = self.request.GET.get('orderby', '')
        asc_desc = self.request.GET.get('asc_desc', '')

        if order != '':
            if asc_desc == "desc" and order[0] != '-':
                order = '-' + order
            elif asc_desc == "asc" and order[0] == '-':
                order = order[:1]

        if filter_val != '' and order != '':
            new_context = Assistencia.objects.filter(
                numeroSolicitacao__startswith=filter_val,
            ).order_by(order)
        elif order != '':
            new_context = Assistencia.objects.all().order_by(order)
        elif filter_val != '':
            new_context = Assistencia.objects.filter(
                numeroSolicitacao__startswith=filter_val,
            )
        else:
            new_context = Assistencia.objects.all()
        return new_context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_agent = self.request.META['HTTP_USER_AGENT']
        keywords = ['Mobile','Opera Mini','Android']
        if any(word in user_agent for word in keywords):
            context['is_mobile'] = True
        else:
            context['is_mobile'] = False

        context['filter'] = self.request.GET.get('filter', '')
        context['orderby'] = self.request.GET.get('orderby', '')
        context['options'] = ASSISTENCIA_ORDER_OPTIONS
        context['asc_desc'] = self.request.GET.get('asc_desc', 'asc')
        context['asc_desc_options'] = [['asc', 'Crescente'],['desc', 'Decrescente']]
        return context
   


class AssistenciaDetailView(generic.DetailView):
    
    model = Assistencia


# Classes created for the forms challenge
class AssistenciaCreate( View):
    form_class = AssistenciaForm
    inline_formset = ItemAssistenciaInlineFormset
    template_name = 'myapp/assistencia_form.html'

    def get_success_url(self):
        return reverse_lazy('assistencias') # kwargs={'pk': self.object.pk}

    def get(self, request, *args, **kwargs):
        """handle form display"""
        form = self.form_class()
        formset = self.inline_formset(instance=Assistencia())
        return render(request,\
            self.template_name,\
            {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        """handle form submission"""
        form = self.form_class(request.POST)
        formset = self.inline_formset(request.POST, instance=Assistencia())
        
        if form.is_valid():
            # Save the parent
            entity = form.save(commit=True)
            # Save the formset
            for f in formset:
                if f.is_valid():
                    f.clean()
                    print("CLEAN ",f.cleaned_data)
                    if len(f.cleaned_data) > 0:
                        item = f.save(commit=False)
                        item.assistencia = entity
                        print("ITEM: ",item)
                        print("ENTUTY: ",entity)
                        item.save()
                print("VALID ",f.is_valid())
                print("CLEAN ",f.cleaned_data)

        return HttpResponseRedirect(self.get_success_url())


class AssistenciaUpdate( UpdateView):
    model = Assistencia
    form_class = AssistenciaForm
    inline_formset = ItemAssistenciaInlineFormset
    template_name = 'myapp/assistencia_form.html'

    def get_success_url(self):
        return reverse_lazy('assistencias') # kwargs={'pk': self.object.pk}

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Assistencia, pk=self.kwargs['pk'])
        form = self.form_class(instance=self.object)
        formset = self.inline_formset(instance=self.object)
        return render(request,\
            self.template_name,\
            {'form': form, 'formset': formset})


    def post(self, request, *args, **kwargs):
        """handle form submission"""
        self.object = get_object_or_404(Assistencia, pk=self.kwargs['pk'])
        form = self.form_class(request.POST,instance=self.object)
        formset = self.inline_formset(request.POST, instance=self.object)
                        
        if form.is_valid():
            # Save the parent
            entity = form.save()
            # Save the formset
            for f in formset:
                if f.is_valid():
                    f.clean()
                    print("@@@   3423 CLEAN ",f.cleaned_data)
                    if len(f.cleaned_data) > 0:
                        # item = f.save(commit=False)
                        # item.instance = entity
                        f.save()
                print("VALID ",f.is_valid())
                print("CLEAN ",f.cleaned_data)

        return HttpResponseRedirect(self.get_success_url())
    
    # def form_valid(self, form):
    #     print(form.cleaned_data)
    #     messages.add_message(
    #         self.request,
    #         messages.SUCCESS,
    #         'The publisher was added.'
    #     )
    #     return super().form_valid(form)


class AssistenciaDelete( DeleteView):
    model = Assistencia
    success_url = reverse_lazy('assistencias')
    



# - - - - - Cliente - - - - -

class ClienteListView(generic.ListView):
    
    model = Cliente
    paginate_by = 50
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_agent = self.request.META['HTTP_USER_AGENT']
        keywords = ['Mobile','Opera Mini','Android']
        if any(word in user_agent for word in keywords):
            context['is_mobile'] = True
        else:
            context['is_mobile'] = False
        return context
   
class ClienteDetailView(generic.DetailView):
    
    model = Cliente


# Classes created for the forms challenge
class ClienteCreate( CreateView):
    model = Cliente
    fields = '__all__'
    success_url = reverse_lazy('clientes')


class ClienteUpdate( UpdateView):
    model = Cliente
    fields = '__all__'
    success_url = reverse_lazy('clientes')


class ClienteDelete( DeleteView):
    model = Cliente
    success_url = reverse_lazy('clientes')
    


# - - - - - Transportadora - - - - -

class TransportadoraListView(generic.ListView):
    model = Transportadora
    paginate_by = 50
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_agent = self.request.META['HTTP_USER_AGENT']
        keywords = ['Mobile','Opera Mini','Android']
        if any(word in user_agent for word in keywords):
            context['is_mobile'] = True
        else:
            context['is_mobile'] = False
        return context

class TransportadoraDetailView(generic.DetailView):    
    model = Transportadora

class TransportadoraCreate( CreateView):
    model = Transportadora
    fields = '__all__'
    success_url = reverse_lazy('transportadoras')
    
class TransportadoraUpdate( UpdateView):
    model = Transportadora
    fields = '__all__'
    success_url = reverse_lazy('transportadoras')
    
class TransportadoraDelete( DeleteView):
    model = Transportadora
    success_url = reverse_lazy('transportadoras')
    


# - - - - - Vendedor - - - - -

class VendedorListView(generic.ListView):
    model = Vendedor
    paginate_by = 50
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_agent = self.request.META['HTTP_USER_AGENT']
        keywords = ['Mobile','Opera Mini','Android']
        if any(word in user_agent for word in keywords):
            context['is_mobile'] = True
        else:
            context['is_mobile'] = False
        return context
   
class VendedorDetailView(generic.DetailView):
    model = Vendedor

class VendedorCreate( CreateView):
    model = Vendedor
    fields = '__all__'
    success_url = reverse_lazy('vendedores')
    
class VendedorUpdate( UpdateView):
    model = Vendedor
    fields = '__all__'
    success_url = reverse_lazy('vendedores')
    
class VendedorDelete( DeleteView):
    model = Vendedor
    success_url = reverse_lazy('vendedores')


# - - - - - Acabamento - - - - -
ACABAMENTO_ORDER_OPTIONS = [
        ['', ''],
        ['acabamento', 'Acabamento'],
        ['lastUpdate', 'Última atualização'],
    ]
class AcabamentoListView(generic.ListView):
    model = Acabamento
    paginate_by = 50

    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '')
        order = self.request.GET.get('orderby', '')
        asc_desc = self.request.GET.get('asc_desc', '')

        if order != '':
            if asc_desc == "desc" and order[0] != '-':
                order = '-' + order
            elif asc_desc == "asc" and order[0] == '-':
                order = order[:1]

        if filter_val != '' and order != '':
            new_context = Acabamento.objects.filter(
                acabamento__startswith=filter_val,
            ).order_by(order)
        elif order != '':
            new_context = Acabamento.objects.all().order_by(order)
        elif filter_val != '':
            new_context = Acabamento.objects.filter(
                acabamento__startswith=filter_val,
            )
        else:
            new_context = Acabamento.objects.all()
        return new_context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_agent = self.request.META['HTTP_USER_AGENT']
        keywords = ['Mobile','Opera Mini','Android']
        if any(word in user_agent for word in keywords):
            context['is_mobile'] = True
        else:
            context['is_mobile'] = False

        context['filter'] = self.request.GET.get('filter', '')
        context['orderby'] = self.request.GET.get('orderby', '')
        context['options'] = ACABAMENTO_ORDER_OPTIONS
        context['asc_desc'] = self.request.GET.get('asc_desc', 'asc')
        context['asc_desc_options'] = [['asc', 'Crescente'],['desc', 'Decrescente']]
        return context
   
class AcabamentoDetailView(generic.DetailView):
    model = Acabamento

class AcabamentoCreate( CreateView):
    model = Acabamento
    fields = '__all__'
    success_url = reverse_lazy('acabamentos')
    
class AcabamentoUpdate( UpdateView):
    model = Acabamento
    fields = '__all__'
    success_url = reverse_lazy('acabamentos')
    
class AcabamentoDelete( DeleteView):
    model = Acabamento
    success_url = reverse_lazy('acabamentos')


# - - - - - Tecido - - - - -
TECIDO_ORDER_OPTIONS = [
        ['', ''],
        ['tecido', 'Tecido'],
        ['lastUpdate', 'Última atualização'],
    ]
class TecidoListView(generic.ListView):
    model = Tecido
    paginate_by = 50

    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '')
        order = self.request.GET.get('orderby', '')
        asc_desc = self.request.GET.get('asc_desc', '')

        if order != '':
            if asc_desc == "desc" and order[0] != '-':
                order = '-' + order
            elif asc_desc == "asc" and order[0] == '-':
                order = order[:1]

        if filter_val != '' and order != '':
            new_context = Tecido.objects.filter(
                tecido__startswith=filter_val,
            ).order_by(order)
        elif order != '':
            new_context = Tecido.objects.all().order_by(order)
        elif filter_val != '':
            new_context = Tecido.objects.filter(
                tecido__startswith=filter_val,
            )
        else:
            new_context = Tecido.objects.all()
        return new_context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_agent = self.request.META['HTTP_USER_AGENT']
        keywords = ['Mobile','Opera Mini','Android']
        if any(word in user_agent for word in keywords):
            context['is_mobile'] = True
        else:
            context['is_mobile'] = False

        context['filter'] = self.request.GET.get('filter', '')
        context['orderby'] = self.request.GET.get('orderby', '')
        context['options'] = TECIDO_ORDER_OPTIONS
        context['asc_desc'] = self.request.GET.get('asc_desc', 'asc')
        context['asc_desc_options'] = [['asc', 'Crescente'],['desc', 'Decrescente']]
        return context
   
class TecidoDetailView(generic.DetailView):
    model = Tecido

class TecidoCreate( CreateView):
    model = Tecido
    fields = '__all__'
    success_url = reverse_lazy('tecidos')
    
class TecidoUpdate( UpdateView):
    model = Tecido
    fields = '__all__'
    success_url = reverse_lazy('tecidos')
    
class TecidoDelete( DeleteView):
    model = Tecido
    success_url = reverse_lazy('tecidos')


# - - - - - FormaPagamento - - - - -
FORMAPAGAMENTO_ORDER_OPTIONS = [
        ['', ''],
        ['formaDePagamento', 'Forma de Pagamento'],
        ['lastUpdate', 'Última atualização'],
    ]
class FormaPagamentoListView(generic.ListView):
    model = FormaPagamento
    paginate_by = 50

    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '')
        order = self.request.GET.get('orderby', '')
        asc_desc = self.request.GET.get('asc_desc', '')

        if order != '':
            if asc_desc == "desc" and order[0] != '-':
                order = '-' + order
            elif asc_desc == "asc" and order[0] == '-':
                order = order[:1]

        if filter_val != '' and order != '':
            new_context = FormaPagamento.objects.filter(
                formaDePagamento__startswith=filter_val,
            ).order_by(order)
        elif order != '':
            new_context = FormaPagamento.objects.all().order_by(order)
        elif filter_val != '':
            new_context = FormaPagamento.objects.filter(
                formaDePagamento__startswith=filter_val,
            )
        else:
            new_context = FormaPagamento.objects.all()
        return new_context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_agent = self.request.META['HTTP_USER_AGENT']
        keywords = ['Mobile','Opera Mini','Android']
        if any(word in user_agent for word in keywords):
            context['is_mobile'] = True
        else:
            context['is_mobile'] = False

        context['filter'] = self.request.GET.get('filter', '')
        context['orderby'] = self.request.GET.get('orderby', '')
        context['options'] = FORMAPAGAMENTO_ORDER_OPTIONS
        context['asc_desc'] = self.request.GET.get('asc_desc', 'asc')
        context['asc_desc_options'] = [['asc', 'Crescente'],['desc', 'Decrescente']]
        return context
   
class FormaPagamentoDetailView(generic.DetailView):
    model = FormaPagamento

class FormaPagamentoCreate( CreateView):
    model = FormaPagamento
    fields = '__all__'
    success_url = reverse_lazy('formasPagamento')
    
class FormaPagamentoUpdate( UpdateView):
    model = FormaPagamento
    fields = '__all__'
    success_url = reverse_lazy('formasPagamento')
    
class FormaPagamentoDelete( DeleteView):
    model = FormaPagamento
    success_url = reverse_lazy('formasPagamento')
    



def pedido_pdf_view(request, *args, **kwargs):
    template_path = 'myapp/pedido_pdf.html'
    pk = kwargs.get('pk')
    pedido = get_object_or_404(Pedido, pk=pk)
    itemsPedido = ItemPedido.objects.filter(pedido=pedido)

    valor_produtos = 0
    for item in itemsPedido:
        valor_produtos += item.produto.valor * item.quantidade
    
    valor_descontos = valor_produtos * (( pedido.desconto1 + pedido.desconto2 + pedido.desconto3 + pedido.desconto4 + pedido.desconto5)/100)
    valor_desconto_aplicado = valor_produtos - valor_descontos
    valor_ipi = valor_desconto_aplicado * (pedido.ipi/100)
    valor_total_pedido = valor_desconto_aplicado + valor_ipi

    context = {'pedido': pedido, 
               'itemsPedido': itemsPedido,
               'valor_produtos': valor_produtos,
               'valor_descontos': valor_descontos,
               'valor_desconto_aplicado': valor_desconto_aplicado,
               'valor_ipi': valor_ipi,
               'valor_total_pedido': valor_total_pedido,}
    # Create a Django response object, and specify content_type as pdf
    # response = HttpResponse(content_type='application/pdf')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="pedido_'+pedido.ordemCompra+'.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response












# class MyView(UpdateView): # FormView, CreateView, etc
#     def get_context_data(self, **kwargs):
#         ctx = super(MyView, self).get_context_data(**kwargs)
#         ctx['named_formsets'] = self.get_named_formsets()
#         return ctx

#     def get_named_formsets(self):
#         return {
#             'followup': FollowUpFormSet(self.request.POST or None, prefix='followup'),
#             'action': ActionFormSet(self.request.POST or None, prefix='action'),
#         }

#     def form_valid(self, form):
#         named_formsets = self.get_named_formsets()
#         if not all((x.is_valid() for x in named_formsets.values())):
#             return self.render_to_response(self.get_context_data(form=form))

#         self.object = form.save()

#         # for every formset, attempt to find a specific formset save function
#         # otherwise, just save.
#         for name, formset in named_formsets.items():
#             formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
#             if formset_save_func is not None:
#                 formset_save_func(formset)
#             else:
#                 formset.save()
#         return http.HttpResponseRedirect('')

#     def formset_followup_valid(self, formset):
#         """
#         Hook for custom formset saving.. useful if you have multiple formsets
#         """
#         followups = formset.save(commit=False) # self.save_formset(formset, contact)
#         for followup in followups:
#             followup.who = self.request.user
#             followup.contact = self.object
#             followup.save()

# def post(self, request, *args, **kwargs):
#         """handle form submission"""
#         self.object = self.get_object()
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         formset = self.inline_formset(request.POST, instance=self.object)
#         print("@@@@@@@@@@@@@   ",self.kwargs['pk'])
#         print("FORM: ",form)
#         print("FORMSET: ",formset)
#         if form.is_valid() and formset.is_valid():
#             # Save the parent
            
#             return self.form_valid(form, formset)
#         return self.form_invalid(form, formset)

#     def form_valid(self, form, formset):
#         self.object = form.save()
#         formset.instance = self.object
#         formset.save()

#         return HttpResponseRedirect(self.get_success_url())