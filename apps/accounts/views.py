from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema

from apps.accounts.models import CustomAccount
from apps.accounts.serializers import AccountRegistrationSerializer
from apps.utils.email_sender import SendEmail
from apps.utils.otp_generator import OTP_generator


@extend_schema(tags=["Auth"])
class AccountRegistrationView(APIView):
    """
     A view for creating new users. with POST request method and proper status codes
    """
    serializer_class = AccountRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get("email")
        user = CustomAccount.objects.filter(email=email).first()
        if user:
            return Response({"message": "User with this credentials already exists."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        otp = OTP_generator()
        cache.set(otp, email)
        SendEmail.send_email(subject="OTP for Activation",
                             body="Your Activation Code Is: " + otp,
                             to=[email])
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Auth"])
class AccountLoginView(TokenObtainPairView):
    """View for user to log in using JWT bearer Token"""
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        user = CustomAccount.objects.filter(email=email).first()
        if not user:
            return Response(
                {"detail": "No active account found with the given credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
