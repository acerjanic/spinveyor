


from rest_framework import viewsets
from app.api.serializers import StudySerializer, ReconProtocolSerializer, ReconSerializer
from app.models import Study, ReconProtocol, Recon

class StudyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Study.objects.all()
    serializer_class = StudySerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return Study.objects.all()
            return Study.objects.filter(users=self.request.user)


class ReconProtocolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ReconProtocol.objects.all()
    serializer_class = ReconProtocolSerializer
    

class ReconViewSet(viewsets.ModelViewSet):
    queryset = Recon.objects.all()
    serializer_class = ReconSerializer
