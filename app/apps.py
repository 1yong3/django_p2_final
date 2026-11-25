from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'app'
    verbose_name = 'Loja (Produtos)'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        # Registra os sinais que sincronizam a equipe com o Supabase.
        from . import signals  # noqa: F401
