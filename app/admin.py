from django.contrib import admin

from .models import Categoria, ItemPedido, Pedido, Servico


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo']
    list_filter = ['ativo']
    search_fields = ['nome']


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'preco', 'ativo', 'criado_em']
    list_filter = ['ativo', 'categoria']
    search_fields = ['nome', 'descricao']
    list_per_page = 25


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ['subtotal']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'data', 'total', 'status']
    list_filter = ['status', 'data']
    search_fields = ['usuario__username']
    inlines = [ItemPedidoInline]
