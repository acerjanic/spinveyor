from rest_framework import serializers

from app.models import Study, ReconProtocol, Recon

class ReconProtocolSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReconProtocol
        fields = ['name', 'nf_file']


class StudySerializer(serializers.ModelSerializer):
    recon_protocol = ReconProtocolSerializer(many=False, read_only=True)
    class Meta:
        model = Study
        fields = ['id','name', 'slug', 'recon_protocol']


class ReconSerializer(serializers.ModelSerializer):
    study = serializers.SlugRelatedField(many=False,
                                         read_only=False,
                                         slug_field='slug',
                                         queryset=Study.objects.all()
                                         )
    class Meta:
        model = Recon
        fields = ['id', 'study', 'subject_id', 'created_at', 'status', 'created_by', 'status_changed']

