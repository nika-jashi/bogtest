from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Product
from apps.products.serializers import ProductCreationSerializer, ProductListSerializer


@extend_schema(tags=["product"])
class ProductCreationView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductCreationSerializer

    def post(self, request, *args, **kwargs):
        serializer = ProductCreationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(seller=request.user)
            serializer.save()
            return Response({"detail": "You Successfully Listed A Product"}, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["product"])
class ProductListView(APIView):
    serializer_class = ProductListSerializer

    def get(self, request):
        product_information = Product.objects.all()
        if not product_information:
            return Response({"detail": "No Products To Show"}, status=status.HTTP_200_OK)
        serializer = ProductListSerializer(product_information, many=True)
        return Response(serializer.data)