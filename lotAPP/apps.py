from django.apps import AppConfig

class LotappConfig(AppConfig):
    name = 'lotAPP'

    def ready(self):
        import lotAPP.signals
