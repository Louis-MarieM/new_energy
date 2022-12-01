from rest_framework.serializers import ModelSerializer

from scraping.models import Facture

class FactureSerializer(ModelSerializer) :

    class Meta :
        model = Facture
        fields = ['name', 'path']