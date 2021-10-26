from django.urls import path
from . import views

urlpatterns =[
	path('',views.index, name='index'),
]

urlpatterns += [
    path('representadas/', views.RepresentadaListView.as_view(), name='representadas'),
    path('representada/<int:pk>', views.RepresentadaDetailView.as_view(), name='representada-detail'),
    path('representada/create/', views.RepresentadaCreate.as_view(), name='representada-create'),
    path('representada/<int:pk>/update/', views.RepresentadaUpdate.as_view(), name='representada-update'),
    path('representada/<int:pk>/delete/', views.RepresentadaDelete.as_view(), name='representada-delete'),
]

urlpatterns += [
    path('pedidos/', views.PedidoListView.as_view(), name='pedidos'),
    path('pedido/<int:pk>', views.PedidoDetailView.as_view(), name='pedido-detail'),
    path('pedido/create/', views.PedidoCreate.as_view(), name='pedido-create'),
    path('pedido/<int:pk>/update/', views.PedidoUpdate.as_view(), name='pedido-update'),
    path('pedido/<int:pk>/delete/', views.PedidoDelete.as_view(), name='pedido-delete'),
]


urlpatterns += [
    path('produtos/', views.ProdutoListView.as_view(), name='produtos'),
    path('produto/<int:pk>', views.ProdutoDetailView.as_view(), name='produto-detail'),
    path('produto/create/', views.ProdutoCreate.as_view(), name='produto-create'),
    path('produto/<int:pk>/update/', views.ProdutoUpdate.as_view(), name='produto-update'),
    path('produto/<int:pk>/delete/', views.ProdutoDelete.as_view(), name='produto-delete'),
]

urlpatterns += [
    path('assistencias/', views.AssistenciaListView.as_view(), name='assistencias'),
    path('assistencia/<int:pk>', views.AssistenciaDetailView.as_view(), name='assistencia-detail'),
    path('assistencia/create/', views.AssistenciaCreate.as_view(), name='assistencia-create'),
    path('assistencia/<int:pk>/update/', views.AssistenciaUpdate.as_view(), name='assistencia-update'),
    path('assistencia/<int:pk>/delete/', views.AssistenciaDelete.as_view(), name='assistencia-delete'),
]

urlpatterns += [
    path('clientes/', views.ClienteListView.as_view(), name='clientes'),
    path('cliente/<int:pk>', views.ClienteDetailView.as_view(), name='cliente-detail'),
    path('cliente/create/', views.ClienteCreate.as_view(), name='cliente-create'),
    path('cliente/<int:pk>/update/', views.ClienteUpdate.as_view(), name='cliente-update'),
    path('cliente/<int:pk>/delete/', views.ClienteDelete.as_view(), name='cliente-delete'),
]

urlpatterns += [
    path('transportadoras/', views.TransportadoraListView.as_view(), name='transportadoras'),
    path('transportadora/<int:pk>', views.TransportadoraDetailView.as_view(), name='transportadora-detail'),
    path('transportadora/create/', views.TransportadoraCreate.as_view(), name='transportadora-create'),
    path('transportadora/<int:pk>/update/', views.TransportadoraUpdate.as_view(), name='transportadora-update'),
    path('transportadora/<int:pk>/delete/', views.TransportadoraDelete.as_view(), name='transportadora-delete'),
]

urlpatterns += [
    path('vendedores/', views.VendedorListView.as_view(), name='vendedores'),
    path('vendedor/<int:pk>', views.VendedorDetailView.as_view(), name='vendedor-detail'),
    path('vendedor/create/', views.VendedorCreate.as_view(), name='vendedor-create'),
    path('vendedor/<int:pk>/update/', views.VendedorUpdate.as_view(), name='vendedor-update'),
    path('vendedor/<int:pk>/delete/', views.VendedorDelete.as_view(), name='vendedor-delete'),
]

urlpatterns += [
    path('acabamentos/', views.AcabamentoListView.as_view(), name='acabamentos'),
    path('acabamento/<int:pk>', views.AcabamentoDetailView.as_view(), name='acabamento-detail'),
    path('acabamento/create/', views.AcabamentoCreate.as_view(), name='acabamento-create'),
    path('acabamento/<int:pk>/update/', views.AcabamentoUpdate.as_view(), name='acabamento-update'),
    path('acabamento/<int:pk>/delete/', views.AcabamentoDelete.as_view(), name='acabamento-delete'),
]

urlpatterns += [
    path('tecidos/', views.TecidoListView.as_view(), name='tecidos'),
    path('tecido/<int:pk>', views.TecidoDetailView.as_view(), name='tecido-detail'),
    path('tecido/create/', views.TecidoCreate.as_view(), name='tecido-create'),
    path('tecido/<int:pk>/update/', views.TecidoUpdate.as_view(), name='tecido-update'),
    path('tecido/<int:pk>/delete/', views.TecidoDelete.as_view(), name='tecido-delete'),
]