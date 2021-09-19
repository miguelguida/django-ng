from django.shortcuts import render
from django.http import HttpResponse 
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory


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

class RepresentadaListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Representada
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_agent = self.request.META['HTTP_USER_AGENT']
        keywords = ['Mobile','Opera Mini','Android']
        if any(word in user_agent for word in keywords):
            context['is_mobile'] = True
        else:
            context['is_mobile'] = False
        return context
   
class RepresentadaDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Representada


# Classes created for the forms challenge
class RepresentadaCreate( CreateView):
    model = Representada
    fields = '__all__'
    # permission_required = 'catalog.can_mark_returned'


class RepresentadaUpdate( UpdateView):
    model = Representada
    fields = '__all__'
    # permission_required = 'catalog.can_mark_returned'


class RepresentadaDelete( DeleteView):
    model = Representada
    success_url = reverse_lazy('representadas')
    # permission_required = 'catalog.can_mark_returned'


# - - - - - Pedido - - - - -

class PedidoListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Pedido
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_agent = self.request.META['HTTP_USER_AGENT']
        keywords = ['Mobile','Opera Mini','Android']
        if any(word in user_agent for word in keywords):
            context['is_mobile'] = True
        else:
            context['is_mobile'] = False
        return context
   
class PedidoDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Pedido


# # Classes created for the forms challenge
# class PedidoCreate( CreateView):
#     model = Pedido
#     form = PedidoForm()
#     # permission_required = 'catalog.can_mark_returned'

def pedido_create_view(request):
    """View function for renewing a specific BookInstance by librarian."""

    form = PedidoForm(request.POST or None)

        # Check if the form is valid:
    if form.is_valid():
        form.save()

    context = {
        'form': form,
    }

    return render(request, 'myapp/pedido_form.html', context)

class PedidoCreate(View):
    form_class = PedidoForm
    inline_formset = ItemPedidoInlineFormset
    template_name = 'myapp/pedido_form.html'

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
        if form.is_valid() and formset.is_valid():
            # Save the parent
            entity = form.save(commit=True)
            # Save the formset
            formset.instance = entity
            formset.save()

        return render(request,\
            self.template_name,\
            {'form': form, 'formset': formset})


class PedidoUpdate( UpdateView):
    model = Pedido
    fields = '__all__'
    # permission_required = 'catalog.can_mark_returned'


class PedidoDelete( DeleteView):
    model = Pedido
    success_url = reverse_lazy('pedidos')
    # permission_required = 'catalog.can_mark_returned'

# - - - - - Produto - - - - -

class ProdutoListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Produto
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_agent = self.request.META['HTTP_USER_AGENT']
        keywords = ['Mobile','Opera Mini','Android']
        if any(word in user_agent for word in keywords):
            context['is_mobile'] = True
        else:
            context['is_mobile'] = False
        return context

class ProdutoDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Produto


# Classes created for the forms challenge
class ProdutoCreate( CreateView):
    model = Produto
    fields = '__all__'
    # permission_required = 'catalog.can_mark_returned'


class ProdutoUpdate( UpdateView):
    model = Produto
    fields = '__all__'
    # permission_required = 'catalog.can_mark_returned'


class ProdutoDelete( DeleteView):
    model = Produto
    success_url = reverse_lazy('produtos')
    # permission_required = 'catalog.can_mark_returned'


# - - - - - Assistencia - - - - -

class ItemAssistenciaInline(InlineFormSetFactory):
    model = ItemAssistencia
    fields = '__all__'


class AssistenciaListView(generic.ListView):
    model = Assistencia
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_agent = self.request.META['HTTP_USER_AGENT']
        keywords = ['Mobile','Opera Mini','Android']
        if any(word in user_agent for word in keywords):
            context['is_mobile'] = True
        else:
            context['is_mobile'] = False
        return context
   


class AssistenciaDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Assistencia


# Classes created for the forms challenge
class AssistenciaCreate( View):
    form_class = AssistenciaForm
    inline_formset = ItemAssistenciaInlineFormset
    template_name = 'myapp/assistencia_form.html'

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
        print("FORM: ",form)
        print("FORMSET: ",formset)
        if form.is_valid() and formset.is_valid():
            # Save the parent
            
            entity = form.save(commit=True)
            # Save the formset
            formset.instance = entity
            formset.save()

        return render(request,\
            self.template_name,\
            {'form': form, 'formset': formset})


class AssistenciaUpdate( UpdateWithInlinesView):
    model = Assistencia
    inlines = [ItemAssistenciaInline]
    fields = '__all__'
    # permission_required = 'catalog.can_mark_returned'


class AssistenciaDelete( DeleteView):
    model = Assistencia
    success_url = reverse_lazy('assistencias')
    # permission_required = 'catalog.can_mark_returned'



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

