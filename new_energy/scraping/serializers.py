from rest_framework.serializers import ModelSerializer

from scraping.models import Facture

class FactureSereializer(ModelSerializer) :

    class Meta :
        model = Facture
        fields = ['name', 'path'] 