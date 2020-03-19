


from rest_framework import viewsets
from app.api.serializers import StudySerializer, ReconProtocolSerializer
from app.models import Study, ReconProtocol

class StudyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Study.objects.all()
    serializer_class = StudySerializer

class ReconProtocolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ReconProtocol.objects.all()
    serializer_class = ReconProtocolSerializer
    