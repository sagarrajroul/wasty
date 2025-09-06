from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Bag
from .serializers import BagSerializer


class BagApi(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BagSerializer
    queryset = Bag.objects.all()


class BagListApi(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BagSerializer
    queryset = Bag.objects.all()


class BagDetailsApi(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BagSerializer
    queryset = Bag.objects.all()
