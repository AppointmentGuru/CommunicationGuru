from django.core.management.base import BaseCommand
from django.utils import timezone
from .models import Communication

class Command(BaseCommand):

    help = 'Send communications on a schedule'

    def handle(self, *args, **options):
        comms = Communication(
            send_date__gte=timezone.now()
        )
        for comm in comms: comm.send()