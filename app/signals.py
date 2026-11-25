"""Sincroniza a equipe editada no Django admin com a tabela Supabase.

O site continua lendo do Supabase (como pede o projeto), mas agora a equipe
pode ser gerenciada pelo /admin/ — ao salvar/excluir, o Django envia a
alteração para o Supabase automaticamente.
"""

import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Integrante
from .supabase_client import supabase

logger = logging.getLogger(__name__)


def _dados(integrante):
    return {
        'nome': integrante.nome,
        'cargo': integrante.cargo,
        'biografia': integrante.biografia,
        'foto_url': integrante.foto_url,
    }


@receiver(post_save, sender=Integrante)
def sincronizar_integrante_supabase(sender, instance, **kwargs):
    if supabase is None:
        return

    try:
        existentes = (
            supabase.table('integrantes')
            .select('id')
            .eq('nome', instance.nome)
            .execute()
            .data
        )

        if existentes:
            supabase.table('integrantes').update(_dados(instance)).eq(
                'id', existentes[0]['id']
            ).execute()
        else:
            supabase.table('integrantes').insert(_dados(instance)).execute()
    except Exception as exc:  # never breaks the admin save
        logger.warning('Não foi possível sincronizar integrante ao Supabase: %s', exc)


@receiver(post_delete, sender=Integrante)
def excluir_integrante_supabase(sender, instance, **kwargs):
    if supabase is None:
        return

    try:
        supabase.table('integrantes').delete().eq('nome', instance.nome).execute()
    except Exception as exc:  # never breaks the admin delete
        logger.warning('Não foi possível excluir integrante no Supabase: %s', exc)
