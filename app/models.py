from django.contrib.auth.models import User
from django.db import models


class Integrante(models.Model):
    """Equipe do Quem Somos, editável no Django admin e sincronizada ao Supabase."""

    CARGOS = [
        ('Criador', 'Criador'),
        ('Desenvolvedor', 'Desenvolvedor'),
        ('Tester', 'Tester'),
        ('Outro', 'Outro'),
    ]

    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=30, choices=CARGOS, default='Outro')
    biografia = models.TextField(blank=True)
    foto_url = models.CharField(
        max_length=300,
        blank=True,
        help_text='URL ou caminho local, ex.: /media/servicos/ic_quemsomos1.png',
    )
    ordem = models.PositiveIntegerField(
        default=0,
        help_text='Menor número aparece primeiro (use 2 para o Criador ficar no centro).',
    )
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Integrante'
        verbose_name_plural = 'Quem Somos (Equipe)'
        ordering = ['ordem', 'nome']

    def __str__(self):
        return f'{self.nome} — {self.cargo}'


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome


class Servico(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='servicos/', blank=True, null=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='servicos',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='pedidos',
    )
    data = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
    )

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-data']

    def __str__(self):
        return f'Pedido {self.id} - {self.usuario.username}'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='itens',
    )
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'

    def __str__(self):
        return f'{self.servico.nome} - {self.quantidade}x'

    @property
    def subtotal(self):
        return self.servico.preco * self.quantidade
