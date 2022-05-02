from django.apps import AppConfig

class CoreConfig(AppConfig):
    name = 'game_checkpoint.apps.core'
    verbose_name = "My Application"
    def ready(self):
            from .threads import start_threads
            start_threads()
