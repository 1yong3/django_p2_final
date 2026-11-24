from django.shortcuts import render, redirect
from .models import Servico, Categoria, Pedido, ItemPedido
from .forms import FormServico
from .supabase_client import supabase
from .serializers import CategoriaSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from django.db.models import Count
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "index.html")


def servico(request):
    servicos = Servico.objects.filter(ativo=True).exclude(preco=0)

    busca = request.GET.get('busca')
    categoria = request.GET.get('categoria')
    preco = request.GET.get('preco')
    ordem = request.GET.get('ordem')

    # Filtro por nome
    if busca:
        servicos = servicos.filter(nome__icontains=busca)

    # Filtro por categoria
    categorias = Categoria.objects.filter(ativo=True).order_by('nome')

    if categoria:
        servicos = servicos.filter(categoria_id=categoria)

    # Filtro por preço
    if preco == 'baixo':
        servicos = servicos.filter(preco__lte=500)

    elif preco == 'medio':
        servicos = servicos.filter(
            preco__gte=500,
            preco__lte=1500
        )

    elif preco == 'alto':
        servicos = servicos.filter(preco__gt=1500)

    # Ordenação
    if ordem == 'menor':
        servicos = servicos.order_by('preco')

    elif ordem == 'maior':
        servicos = servicos.order_by('-preco')

    else:
        servicos = servicos.order_by('nome')

    # Informações após aplicação dos filtros
    total_servicos = servicos.count()
    tem_servicos = servicos.exists()

    mais_barato = servicos.order_by('preco').first()
    mais_caro = servicos.order_by('-preco').first()

    contexto = {
        'servico': servicos,
        'total_servicos': total_servicos,
        'tem_servicos': tem_servicos,
        'mais_barato': mais_barato,
        'mais_caro': mais_caro,
        'busca': busca,
        'categoria': categoria,
        'categorias': categorias,
        'preco': preco,
        'ordem': ordem,
    }

    return render(request, 'servico.html', contexto)


def addServico(request):
    form = FormServico(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("servico")

    return render(request, "add-servico.html", {"form": form})


def delServico(request, id_servico):
    servico = Servico.objects.get(id=id_servico)
    servico.delete()
    return redirect('servico')


def editServico(request, id_servico):
    servico = Servico.objects.get(id=id_servico)
    form = FormServico(request.POST or None, request.FILES, instance=servico)

    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('servico')
    return render(request, "edit-servico.html", {'form': form})


def integrantes(request):
    resposta = supabase.table("integrantes").select("*").execute()
    return render(request, "integrantes.html", {'integrantes': resposta.data})


def quem_somos(request):
    resposta = supabase.table("integrantes").select("*").execute()
    return render(request, "quem_somos.html", {'integrantes': resposta.data})


def addIntegrante(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        cargo = request.POST.get("cargo")
        biografia = request.POST.get("biografia")
        foto = request.POST.get("foto")

        supabase.table("integrantes").insert({
            "nome": nome,
            "cargo": cargo,
            "biografia": biografia,
            "foto_url": foto
        }).execute()

        return redirect("integrantes")

    return render(request, "add-integrante.html")


def delIntegrante(request, id_integrante):
    supabase.table("integrantes").delete().eq("id", id_integrante).execute()
    return redirect("integrantes")


@api_view(['GET', 'POST'])
def categoriasAPI(request):

    if request.method == 'GET':
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

    serializer = CategoriaSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET', 'PUT', 'DELETE'])
def categoriaAPI(request, id_categoria):

    try:
        categoria = Categoria.objects.get(id=id_categoria)

    except Categoria.DoesNotExist:
        return Response(
            {'erro': 'Categoria não encontrada.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CategoriaSerializer(
            categoria,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == 'DELETE':
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#terminar o produtos (aula faltada)
def produtos(request):
    servicos = Servico.objects.all()

    resposta = requests.get('https://fakestoreapi.com/products')
    produtos_api = resposta.json()

    if request.method == 'POST' and 'comprar' in request.POST:
        if request.user.is_authenticated:
            servico_id = request.POST.get('servico_id')
            servico = Servico.objects.get(id=servico_id)
            
            # Verificar se já existe um pedido em aberto para este usuário
            pedido, created = Pedido.objects.get_or_create(
                usuario=request.user,
                status='pendente'
            )
            
            # Verificar se o item já está no pedido
            item, item_created = ItemPedido.objects.get_or_create(
                pedido=pedido,
                servico=servico,
                defaults={'quantidade': 1}
            )
            if not item_created:
                item.quantidade += 1
                item.save()
            
            return redirect('minhas_pedidos')
        else:
            return redirect('login')

    return render(request, "produtos.html", {'produtos':servicos, 'produtos_api': produtos_api})


@login_required
def minhas_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-data')
    
    contexto = {
        'pedidos': pedidos,
    }
    return render(request, "minhas_pedidos.html", contexto)


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

    return render(request, 'relatorio.html', {
        'servicos_ativos': servicos_ativos,
        'servicos_inativos': servicos_inativos,
        'categorias_labels': [
            item['categoria__nome'] or 'Sem categoria'
            for item in categorias
        ],
        'categorias_valores': [
            item['quantidade']
            for item in categorias
        ],
    })