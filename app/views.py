from decimal import Decimal

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from login.decorators import admin_required, is_admin

from .forms import FormServico
from .models import Categoria, Integrante, ItemPedido, Pedido, Servico
from .serializers import CategoriaSerializer
from .supabase_client import supabase


# =====================================================
# HOME
# =====================================================
def index(request):
    return render(request, 'index.html')


# =====================================================
# SERVIÇOS (listagem + filtros + estatísticas + CRUD)
# =====================================================
@login_required
def servico(request):
    servicos = Servico.objects.filter(ativo=True).exclude(preco=0)

    busca = request.GET.get('busca')
    categoria = request.GET.get('categoria')
    preco = request.GET.get('preco')
    ordem = request.GET.get('ordem')

    if busca:
        servicos = servicos.filter(nome__icontains=busca)

    categorias = Categoria.objects.filter(ativo=True).order_by('nome')

    if categoria:
        servicos = servicos.filter(categoria_id=categoria)

    if preco == 'baixo':
        servicos = servicos.filter(preco__lte=500)
    elif preco == 'medio':
        servicos = servicos.filter(preco__gte=500, preco__lte=1500)
    elif preco == 'alto':
        servicos = servicos.filter(preco__gt=1500)

    if ordem == 'menor':
        servicos = servicos.order_by('preco')
    elif ordem == 'maior':
        servicos = servicos.order_by('-preco')
    else:
        servicos = servicos.order_by('nome')

    contexto = {
        'servico': servicos,
        'total_servicos': servicos.count(),
        'tem_servicos': servicos.exists(),
        'mais_barato': servicos.order_by('preco').first(),
        'mais_caro': servicos.order_by('-preco').first(),
        'busca': busca,
        'categoria': categoria,
        'categorias': categorias,
        'preco': preco,
        'ordem': ordem,
        'pode_gerenciar': is_admin(request.user),
    }

    return render(request, 'servico.html', contexto)


@admin_required
def addServico(request):
    form = FormServico(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Serviço cadastrado com sucesso.')
        return redirect('servico')

    return render(request, 'add-servico.html', {'form': form})


@admin_required
def delServico(request, id_servico):
    servico_obj = get_object_or_404(Servico, id=id_servico)
    servico_obj.delete()
    messages.success(request, 'Serviço excluído com sucesso.')
    return redirect('servico')


@admin_required
def editServico(request, id_servico):
    servico_obj = get_object_or_404(Servico, id=id_servico)
    form = FormServico(
        request.POST or None,
        request.FILES or None,
        instance=servico_obj,
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Serviço atualizado com sucesso.')
        return redirect('servico')

    return render(request, 'edit-servico.html', {'form': form})


# =====================================================
# EQUIPE (Supabase) - listar / adicionar / editar / excluir
# =====================================================
def _buscar_integrantes():
    if supabase is None:
        return []

    try:
        return supabase.table('integrantes').select('*').execute().data
    except Exception:
        return []


# Ordem de exibição em "Quem Somos": o Criador deve ficar no meio.
ORDEM_CARGOS_QUEM_SOMOS = {
    'desenvolvedor': 0,
    'criador': 1,
    'tester': 2,
}


def _ordenar_integrantes(integrantes):
    # A ordem definida no admin (campo "ordem") tem prioridade. Quem não estiver
    # cadastrado no admin é ordenado pelos cargos: Desenvolvedor, Criador, Tester.
    try:
        ordens = {
            (i.nome or '').strip().lower(): i.ordem
            for i in Integrante.objects.filter(ativo=True)
        }
    except Exception:
        ordens = {}

    return sorted(
        integrantes,
        key=lambda item: (
            ordens.get(
                (item.get('nome') or '').strip().lower(),
                100 + ORDEM_CARGOS_QUEM_SOMOS.get(
                    (item.get('cargo') or '').strip().lower(),
                    99,
                ),
            ),
            str(item.get('nome') or '').lower(),
        ),
    )


def _integrantes_locais():
    """Equipe cadastrada no Django admin (usada como fallback do Supabase)."""
    try:
        return [
            {
                'id': i.pk,
                'nome': i.nome,
                'cargo': i.cargo,
                'biografia': i.biografia,
                'foto_url': i.foto_url,
            }
            for i in Integrante.objects.filter(ativo=True)
        ]
    except Exception:
        return []


# Equipe exibida em "Quem Somos" quando o Supabase está indisponível/sem dados.
# As fotos são os ícones locais enviados para media/servicos.
EQUIPE_PADRAO = [
    {
        'id': 'local-1',
        'nome': 'Iago',
        'cargo': 'Criador',
        'biografia': (
            'Idealizador do Mind Palace, responsável pela visão do projeto '
            'e pela experiência do usuário.'
        ),
        'foto_url': '/media/servicos/ic_quemsomos1.png',
    },
    {
        'id': 'local-2',
        'nome': 'Diogenes',
        'cargo': 'Desenvolvedor',
        'biografia': (
            'Responsável pela implementação do sistema, integrações e '
            'banco de dados.'
        ),
        'foto_url': '/media/servicos/icone_quemomos3-removebg-preview.png',
    },
    {
        'id': 'local-3',
        'nome': 'Platão',
        'cargo': 'Tester',
        'biografia': (
            'Garante a qualidade das entregas com testes e validação das '
            'funcionalidades.'
        ),
        'foto_url': '/media/servicos/icone_quemsomos2-removebg-preview.png',
    },
]


@admin_required
def integrantes(request):
    # A equipe é gerenciada no banco do site (o mesmo do /admin/). Se o
    # Supabase estiver configurado, os sinais mantêm a tabela remota sincronizada.
    return render(request, 'integrantes.html', {
        'integrantes': Integrante.objects.all().order_by('ordem', 'nome'),
    })


def quem_somos(request):
    integrantes = _ordenar_integrantes(_buscar_integrantes())

    # Se o Supabase falhar, usa a equipe cadastrada no Django admin; se o
    # admin também estiver vazio, usa a equipe padrão do projeto.
    if not integrantes:
        integrantes = _ordenar_integrantes(_integrantes_locais())
    if not integrantes:
        integrantes = _ordenar_integrantes(EQUIPE_PADRAO)

    return render(request, 'quem_somos.html', {
        'integrantes': integrantes,
    })


def _msg_sincronizacao():
    return ' Sincronizado com o Supabase.' if supabase is not None else ''


@admin_required
def addIntegrante(request):
    if request.method == 'POST':
        try:
            Integrante.objects.create(
                nome=(request.POST.get('nome') or '').strip(),
                cargo=(request.POST.get('cargo') or 'Outro').strip(),
                biografia=(request.POST.get('biografia') or '').strip(),
                foto_url=(request.POST.get('foto') or '').strip(),
                ordem=int(request.POST.get('ordem') or 0),
                ativo=request.POST.get('ativo') in ('on', '1', 'true', 'True'),
            )
            messages.success(
                request,
                'Integrante cadastrado com sucesso.' + _msg_sincronizacao(),
            )
        except Exception:
            messages.error(request, 'Não foi possível cadastrar o integrante.')

        return redirect('integrantes')

    return render(request, 'add-integrante.html')


@admin_required
def editIntegrante(request, id_integrante):
    integrante = get_object_or_404(Integrante, id=id_integrante)

    if request.method == 'POST':
        try:
            integrante.nome = (request.POST.get('nome') or '').strip()
            integrante.cargo = (request.POST.get('cargo') or 'Outro').strip()
            integrante.biografia = (request.POST.get('biografia') or '').strip()
            integrante.foto_url = (request.POST.get('foto') or '').strip()
            integrante.ordem = int(request.POST.get('ordem') or 0)
            integrante.ativo = request.POST.get('ativo') in (
                'on', '1', 'true', 'True'
            )
            integrante.save()

            messages.success(
                request,
                'Integrante atualizado com sucesso.' + _msg_sincronizacao(),
            )
        except Exception:
            messages.error(request, 'Não foi possível atualizar o integrante.')

        return redirect('integrantes')

    return render(request, 'edit-integrante.html', {'integrante': integrante})


@admin_required
def delIntegrante(request, id_integrante):
    try:
        integrante = get_object_or_404(Integrante, id=id_integrante)
        integrante.delete()
        messages.success(
            request,
            'Integrante excluído com sucesso.' + _msg_sincronizacao(),
        )
    except Exception:
        messages.error(request, 'Não foi possível excluir o integrante.')

    return redirect('integrantes')


# =====================================================
# API DE CATEGORIAS (Django REST Framework)
# =====================================================
@api_view(['GET', 'POST'])
def categoriasAPI(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

    serializer = CategoriaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def categoriaAPI(request, id_categoria):
    try:
        categoria = Categoria.objects.get(id=id_categoria)
    except Categoria.DoesNotExist:
        return Response(
            {'erro': 'Categoria não encontrada.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == 'GET':
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    categoria.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# =====================================================
# PRODUTOS (local + API externa) e COMPRA
# =====================================================
def _recalcular_total(pedido):
    total = sum(
        (item.servico.preco * item.quantidade for item in pedido.itens.all()),
        Decimal('0'),
    )
    pedido.total = total
    pedido.save(update_fields=['total'])


def _normalizar_fakestore(dados):
    """Converte a resposta da Fake Store API no formato usado pelo template."""
    if not isinstance(dados, list):
        return []

    return [
        {
            'title': item.get('title', ''),
            'description': item.get('description', ''),
            'price': item.get('price', ''),
            'image': item.get('image', ''),
        }
        for item in dados
        if isinstance(item, dict)
    ]


def _normalizar_dummyjson(dados):
    """Converte a resposta da DummyJSON no formato usado pelo template."""
    if not isinstance(dados, dict):
        return []

    itens = dados.get('products', [])
    if not isinstance(itens, list):
        return []

    produtos = []
    for item in itens:
        if not isinstance(item, dict):
            continue

        imagens = item.get('images') or []
        imagem = item.get('thumbnail') or (imagens[0] if imagens else '')

        produtos.append({
            'title': item.get('title', ''),
            'description': item.get('description', ''),
            'price': item.get('price', ''),
            'image': imagem,
        })

    return produtos


# API externa usada na página de produtos. A primeira que responder com JSON
# válido é utilizada; se todas falharem, a página continua funcionando sem os
# produtos externos (evita JSONDecodeError/500).
FONTES_PRODUTOS_API = (
    ('https://fakestoreapi.com/products', _normalizar_fakestore),
    ('https://dummyjson.com/products?limit=4', _normalizar_dummyjson),
)


def _buscar_produtos_api(limite=4):
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; MindPalace/1.0)',
        'Accept': 'application/json',
    }

    for url, normalizar in FONTES_PRODUTOS_API:
        try:
            resposta = requests.get(url, timeout=8, headers=headers)
            resposta.raise_for_status()

            content_type = resposta.headers.get('Content-Type', '').lower()
            if 'json' not in content_type:
                continue

            dados = resposta.json()
        except (requests.RequestException, ValueError):
            continue

        produtos = normalizar(dados)
        if produtos:
            return produtos[:limite]

    return []


def produtos(request):
    servicos = Servico.objects.filter(ativo=True)
    produtos_api = _buscar_produtos_api()

    if request.method == 'POST' and 'comprar' in request.POST:
        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')

        servico_obj = get_object_or_404(
            Servico,
            id=request.POST.get('servico_id'),
        )

        pedido, _ = Pedido.objects.get_or_create(
            usuario=request.user,
            status='pendente',
        )

        item, criado = ItemPedido.objects.get_or_create(
            pedido=pedido,
            servico=servico_obj,
            defaults={'quantidade': 1},
        )
        if not criado:
            item.quantidade += 1
            item.save(update_fields=['quantidade'])

        _recalcular_total(pedido)
        messages.success(
            request,
            f'"{servico_obj.nome}" adicionado aos seus pedidos.',
        )
        return redirect('minhas_pedidos')

    return render(request, 'produtos.html', {
        'servicos': servicos,
        'produtos': servicos,
        'produtos_api': produtos_api,
    })


@login_required
def minhas_pedidos(request):
    pedidos = (
        Pedido.objects
        .filter(usuario=request.user)
        .prefetch_related('itens__servico')
        .order_by('-data')
    )

    for pedido in pedidos:
        _recalcular_total(pedido)

    return render(request, 'minhas_pedidos.html', {'pedidos': pedidos})


# =====================================================
# RELATÓRIOS (gráficos e indicadores)
# =====================================================
@admin_required
def relatorios(request):
    servicos = Servico.objects.all()

    servicos_ativos = servicos.filter(ativo=True).count()
    servicos_inativos = servicos.filter(ativo=False).count()

    categorias = (
        servicos
        .values('categoria__nome')
        .annotate(quantidade=Count('id'))
        .order_by('categoria__nome')
    )

    precos = [s.preco for s in servicos if s.preco is not None]
    preco_medio = (sum(precos, Decimal('0')) / len(precos)) if precos else 0

    return render(request, 'relatorio.html', {
        'servicos_ativos': servicos_ativos,
        'servicos_inativos': servicos_inativos,
        'total_servicos': servicos.count(),
        'preco_medio': preco_medio,
        'total_pedidos': Pedido.objects.count(),
        'categorias_labels': [
            item['categoria__nome'] or 'Sem categoria'
            for item in categorias
        ],
        'categorias_valores': [
            item['quantidade']
            for item in categorias
        ],
    })
