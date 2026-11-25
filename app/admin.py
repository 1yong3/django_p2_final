from django.contrib import admin
from django.utils.html import format_html

from .models import Categoria, ItemPedido, Pedido, Servico


admin.site.site_header = 'Mind Palace — Administração'
admin.site.site_title = 'Mind Palace'
admin.site.index_title = 'Gerenciamento do site'


@admin.action(description='Ativar selecionados (mostrar no site)')
def ativar_produtos(modeladmin, request, queryset):
    total = queryset.update(ativo=True)
    modeladmin.message_user(
        request,
        f'{total} produto(s) ativado(s). Eles já aparecem em /produtos/.',
    )


@admin.action(description='Desativar selecionados (ocultar do site)')
def desativar_produtos(modeladmin, request, queryset):
    total = queryset.update(ativo=False)
    modeladmin.message_user(
        request,
        f'{total} produto(s) desativado(s). Eles não aparecem mais em /produtos/.',
    )


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo', 'total_produtos']
    list_filter = ['ativo']
    search_fields = ['nome']
    list_editable = ['ativo']

    @admin.display(description='Produtos')
    def total_produtos(self, obj):
        return obj.servicos.count()


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = [
        'miniatura',
        'nome',
        'categoria',
        'preco',
        'ativo',
        'criado_em',
    ]
    list_display_links = ['miniatura', 'nome']
    list_editable = ['preco', 'ativo']
    list_filter = ['ativo', 'categoria']
    search_fields = ['nome', 'descricao']
    list_per_page = 25
    ordering = ['nome']
    save_on_top = True
    actions = [ativar_produtos, desativar_produtos]

    fieldsets = (
        ('Produto', {
            'fields': ('nome', 'descricao', 'preco', 'categoria'),
            'description': (
                'O nome, a descrição e o preço aparecem no cartão do produto '
                'na página /produtos/ do site.'
            ),
        }),
        ('Exibição no site', {
            'fields': ('imagem', 'ativo'),
            'description': (
                'Produtos com "Ativo" marcado aparecem em /produtos/ e podem '
                'ser comprados por usuários logados. Desmarque "Ativo" para '
                'ocultar o produto sem excluí-lo.'
            ),
        }),
    )

    @admin.display(description='Imagem')
    def miniatura(self, obj):
        if not obj.imagem:
            return '—'

        return format_html(
            '<img src="{}" alt="{}" style="height:42px;width:42px;'
            'object-fit:contain;border-radius:8px;background:#eef3f0;'
            'padding:3px;border:1px solid #e3eae5;">',
            obj.imagem.url,
            obj.nome,
        )


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
