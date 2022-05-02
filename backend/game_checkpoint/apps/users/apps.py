from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'game_checkpoint.apps.users'
    label = 'users'
    verbose_name = 'Users'

    def ready(self):
        import game_checkpoint.apps.users.signals
