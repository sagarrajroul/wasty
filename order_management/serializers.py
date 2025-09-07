from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Wallet, Product, WithdrawHistory, Item


class WalletSerializer(ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"

    def update(self, instance, validated_data):
        try:
            with transaction.atomic:
                wallet = instance.id
                user = validated_data.get("modified_by")
                amount_withdrawn = instance.balance
                withdrawn_time = validated_data.get("modified_on")
                WithdrawHistory.objects.create(wallet=wallet, user=user, amount_withdrawn=amount_withdrawn,
                                               withdrawn_time=withdrawn_time)
                instance = super(WalletSerializer, self).update(instance, validated_data)
                return instance
        except serializers.ValidationError as ve:
            raise serializers.ValidationError(ve.detail)
        except Exception:
            raise serializers.ValidationError("Please provide valid details")


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductCreateSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "description", "price", "is_active")

    def create(self, validated_data):
        return super().create(validated_data)


class WithdrawHistorySerializer(ModelSerializer):
    class Meta:
        model = WithdrawHistory
        fields = "__all__"

class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ("name", "description","price", "is_active")

class ItemReadSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"
