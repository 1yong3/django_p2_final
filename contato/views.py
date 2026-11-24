from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContatoForm
from .models import Contato


def contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('lista_contatos')
    else:
        form = ContatoForm()

    return render(request, 'contato/contato.html', {'form': form})


def lista_contatos(request):
    contatos = Contato.objects.all()
    return render(request, 'contato/lista.html', {'contatos': contatos})


def excluir_contato(request, id):
    contato = get_object_or_404(Contato, id=id)
    contato.delete()
    return redirect('lista_contatos')