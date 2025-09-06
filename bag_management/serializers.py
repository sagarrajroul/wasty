from rest_framework.serializers import ModelSerializer
from .models import Bag


class BagSerializer(ModelSerializer):
    class Meta:
        model = Bag
        fields = "__all__"
