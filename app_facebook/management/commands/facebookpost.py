from django.core.management import BaseCommand
from app_facebook.services.wall_post_service import WallPostService


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('message', type=str)

    def handle(self, *args, **options):
        message = options['message']

        WallPostService().post(message=message)
