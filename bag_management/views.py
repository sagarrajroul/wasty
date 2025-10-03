import uuid

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, serializers
from .models import WasteBag, BagAssignmentHistory, WasteProduct
from .serializers import WasteBagSerializer, BagAssignmentHistorySerializer, WasteProductSerializer, \
    WasteBagCreateSerializer
import qrcode
import io

class CreateBagApi(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WasteBagCreateSerializer
    queryset = WasteBag.objects.all()


class AssignAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WasteBagCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = WasteBagCreateSerializer(request.data)
        qr_code = serializer.data.get("qr_code")
        if not qr_code:
            return Response({"error": "QR code required or invalid qr code"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bag = WasteBag.objects.get(qr_code=qr_code)
        except WasteBag.DoesNotExist:
            return Response({"error": "Invalid QR code"}, status=status.HTTP_404_NOT_FOUND)

        if bag.is_assigned:
            return Response({"error": "This bag is already assigned"}, status=status.HTTP_400_BAD_REQUEST)

        bag.assigned_to = request.user
        bag.is_assigned = True
        bag.save()

        BagAssignmentHistory.objects.create(bag=bag, user=request.user)

        return Response({"message": "Bag assigned successfully", "bag_id": bag.id})


class UnassignBagAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WasteBagCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = WasteBagCreateSerializer(request.data)
        qr_code = serializer.data.get("qr_code")
        if not qr_code:
            return Response({"error": "QR code required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bag = WasteBag.objects.get(qr_code=qr_code, assigned_to=request.user)
        except WasteBag.DoesNotExist:
            return Response({"error": "Bag not found or not assigned to you"}, status=status.HTTP_404_NOT_FOUND)

        BagAssignmentHistory.objects.create(bag=bag, user=request.user)

        bag.assigned_to = None
        bag.is_assigned = False
        bag.save()

        return Response({"message": "Bag unassigned successfully", "bag_id": bag.id})


class MyBagsAPIView(ListAPIView):
    serializer_class = WasteBagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WasteBag.objects.filter(assigned_to=self.request.user)


class UserBagHistoryAPIView(ListAPIView):
    serializer_class = BagAssignmentHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return BagAssignmentHistory.objects.filter(user__id=user_id).order_by("-assign_on")


class CheckBagApi(APIView):
    serializer_class = WasteBagSerializer

    def get(self, request, qr_code):
        try:
            queryset = WasteBag.objects.filter(qr_code=qr_code).first()
            serializer = self.serializer_class(queryset)
            data = serializer.data
            return Response({"results": data}, status=status.HTTP_200_OK)
        except serializers.ValidationError as ve:
            raise serializers.ValidationError(ve.detail)
        except Exception as ee:
            return Response({"message": str(ee)}, status=status.HTTP_400_BAD_REQUEST)


class AddWasteProductAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, bag_id):
        try:
            bag = WasteBag.objects.get(id=bag_id, assigned_to=request.user)
        except WasteBag.DoesNotExist:
            return Response({"error": "Bag not found or not assigned to you"}, status=status.HTTP_404_NOT_FOUND)

        # Get the latest open session
        session = BagAssignmentHistory.objects.filter(
            bag=bag, user=request.user
        ).last()

        if not session:
            return Response({"error": "No active session found for this bag"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = WasteProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(session=session)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BagProductHistoryAPIView(ListAPIView):
    serializer_class = WasteProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        bag_id = self.kwargs["bag_id"]
        return WasteProduct.objects.filter(
            session__bag_id=bag_id,
            session__user=self.request.user
        ).order_by("-created_at")


class WasteBagQRCodeView(APIView):
    """
    Generate QR code for a WasteBag given its ID.
    """

    def get(self, request, *args, **kwargs):
        try:
            qr_code = uuid.uuid4()
            bag = WasteBag.objects.create(qr_code=qr_code)

            # Generate QR code with the bag.qr_code (UUID)
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(bag.qr_code)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            return HttpResponse(buffer, content_type="image/png")
        except Exception as ee:
            return  Response(str(ee))