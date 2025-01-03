from django.apps import AppConfig

class TransactionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transactions'

    def ready(self):
        import transactions.signals  # Asegúrate de que las señales se registren cuando se inicie la app
