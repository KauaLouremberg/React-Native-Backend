from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'autenticacao'

    def ready(self):
        import autenticacao.signals
