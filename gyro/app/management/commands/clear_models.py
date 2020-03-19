from django.core.management.base import BaseCommand
from app.models import Study, ReconProtocol
class Command(BaseCommand):
    def handle(self, *args, **options):
        Study.objects.all().delete()
        ReconProtocol.objects.all().delete()