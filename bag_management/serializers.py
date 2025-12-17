from rest_framework import serializers

from user_management.serializers import UserPartialSerializer
from .models import WasteBag, BagAssignmentHistory, WasteProduct, BagPickup


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

class BagPickupSerializer(serializers.ModelSerializer):
    class Meta:
        model = BagPickup
        fields = "__all__"

class BagPickupReadSerializer(serializers.ModelSerializer):
    user = UserPartialSerializer(source="user_id", read_only=True)
    bag = WasteBagSerializer(source="bag_id", read_only=True)

    class Meta:
        model = BagPickup
        fields = ["id", "user", "bag", "fulfilled", "created_on"]

