from rest_framework import serializers

from app.models import Study, ReconProtocol

class ReconProtocolSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReconProtocol
        fields = ['name', 'nf_file']

class StudySerializer(serializers.ModelSerializer):
    recon_protocol = ReconProtocolSerializer(many=False, read_only=True)
    class Meta:
        model = Study
        fields = ['name', 'slug', 'recon_protocol']




            