from django.urls import path
from . import views

urlpatterns = [
    path('', views.contato, name='contato'),
    path('lista/', views.lista_contatos, name='lista_contatos'),
    path('excluir/<int:id>/', views.excluir_contato, name='excluir_contato'),
]