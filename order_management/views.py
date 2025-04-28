from datetime import datetime, timezone

from rest_framework import serializers, status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wallet, WithdrawHistory, Item, Product
from .serializers import WalletSerializer, ProductSerializer, WithdrawHistorySerializer, ItemSerializer


class WalletRetrivApi(APIView):
    serializer_class = WalletSerializer

    def get(self, request):
        try:
            user_id = request.GET.get("user_id")
            queryset = Wallet.objects.filter(user=user_id).first()
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"count": queryset.count(), "results": data}, status=status.HTTP_200_OK)
        except serializers.ValidationError as ve:
            raise serializers.ValidationError(ve.detail)
        except Exception as ee:
            return Response({"message": str(ee)}, status=status.HTTP_400_BAD_REQUEST)


class WalletUpdateApi(UpdateAPIView):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user.id,
                        modified_on=timezone.now().astimezone(timezone.utc))


class ItemRetrivUpdateApi(RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user.id,
                        modified_on=timezone.now().astimezone(timezone.utc))


class ItemCreateApi(CreateAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id)


class ProductRetrivUpdateApi(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user.id,
                        modified_on=datetime.now().astimezone(timezone.utc))


class ProductCreateApi(CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id)


class ProductListApi(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class WithdrawHistoryRetrivApi(APIView):
    serializer_class = WithdrawHistorySerializer

    def get(self, request):
        try:
            wallet_id = request.GET.get("wallet_id")
            queryset = WithdrawHistory.objects.filter(wallet=wallet_id).first()
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"count": queryset.count(), "results": data}, status=status.HTTP_200_OK)
        except serializers.ValidationError as ve:
            raise serializers.ValidationError(ve.detail)
        except Exception as ee:
            return Response({"message": str(ee)}, status=status.HTTP_400_BAD_REQUEST)
