from django.urls import path
from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    # path('<endereço>/',<MInhaView>.as_view(),name='<nome-da-url>'),
]
