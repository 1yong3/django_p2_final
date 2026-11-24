from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("servico", views.servico, name="servico"),
    path("add-servico", views.addServico, name="addServico"),
    path("del-servico/<int:id_servico>", views.delServico, name="delServico"),
    path("edit-servico/<int:id_servico>", views.editServico, name="editServico"),

    path("integrantes", views.integrantes, name="integrantes"),
    path("add-integrante/", views.addIntegrante, name="addIntegrante"),
    path("del-integrante/<int:id_integrante>/", views.delIntegrante, name="delIntegrante"),
    path("quem-somos/", views.quem_somos, name="quem_somos"),

    path("categoria-api/", views.categoriasAPI, name="categoriasAPI"),
    path("categoria-api/<int:id_categoria>/", views.categoriaAPI, name="categoriaAPI"),
    path("produtos/", views.produtos, name="produtos"),
    path('minhas-pedidos/', views.minhas_pedidos, name="minhas_pedidos"),
    path('relatorio/', views.relatorios, name='relatorio'),
]
