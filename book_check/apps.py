from django.apps import AppConfig


class BookCheckConfig(AppConfig):
    name = 'book_check'

    def ready(self):
        import book_check.signals

