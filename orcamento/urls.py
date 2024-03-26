from django.urls import path
from .views import OrcamentoCreate, OrcamentoIndexView, OrcamentoList, OrcamentoDelete, OrcamentoUpdate

urlpatterns = [
    path('orcamento/', OrcamentoIndexView.as_view(), name='index-orcamento'),
    path('registrar/orcamento/', OrcamentoCreate.as_view(), name='registrar-orcamento'),
    path('listar/orcamento/', OrcamentoList.as_view(), name='listar-orcamento'),
    path('editar/orcamento/<int:pk>/', OrcamentoUpdate.as_view(), name='editar-orcamento'),
    path('excluir/orcamento/<int:pk>/', OrcamentoDelete.as_view(), name='excluir-orcamento'),
]
