from rest_framework import serializers
from .models import WasteBag, BagAssignmentHistory, WasteProduct


class WasteBagSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteBag
        fields = "__all__"


class WasteBagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteBag
        fields = ("qr_code",)


class WasteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteProduct
        fields = ["id", "name", "weight", "category", "created_at"]


class BagAssignmentHistorySerializer(serializers.ModelSerializer):
    products = WasteProductSerializer(many=True, read_only=True)
    bag_qr = serializers.CharField(source="bag.qr_code", read_only=True)

    class Meta:
        model = BagAssignmentHistory
        fields = ["id", "bag_qr", "user", "assign_on", "products"]
