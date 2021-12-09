from .models import Rp_Journal
from rest_framework import serializers


class JournalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rp_Journal
        fields = ['url', 'kd_jurnal', 'jdl_jurnal', 'pengarang', 'terbitan', 'abstract', 'refrensi', 'keywords', 'file']