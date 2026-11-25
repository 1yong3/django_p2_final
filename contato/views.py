from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from login.decorators import admin_required

from .forms import ContatoForm
from .models import Contato


def contato(request):
    """Formulário público de contato (não exige login)."""
    if request.method == 'POST':
        form = ContatoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Mensagem enviada com sucesso! Em breve entraremos em contato.',
            )
            return redirect('contato')

        messages.error(request, 'Verifique os campos e tente novamente.')
    else:
        form = ContatoForm()

    return render(request, 'contato/contato.html', {'form': form})


@admin_required
def lista_contatos(request):
    """Lista de mensagens recebidas — disponível apenas para administradores."""
    contatos = Contato.objects.all().order_by('-id')
    return render(request, 'lista.html', {'contatos': contatos})


@admin_required
def excluir_contato(request, id):
    contato_obj = get_object_or_404(Contato, id=id)
    contato_obj.delete()
    messages.success(request, 'Mensagem excluída com sucesso.')
    return redirect('lista_contatos')
