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
    path('assistencia/assistencias/', views.AssistenciaListView.as_view(), name='assistencias'),
    path('assistencia/<int:pk>', views.AssistenciaDetailView.as_view(), name='assistencia-detail'),
    path('assistencia/create/', views.AssistenciaCreate.as_view(), name='assistencia-create'),
    path('assistencia/<int:pk>/update/', views.AssistenciaUpdate.as_view(), name='assistencia-update'),
    path('assistencia/<int:pk>/delete/', views.AssistenciaDelete.as_view(), name='assistencia-delete'),
]