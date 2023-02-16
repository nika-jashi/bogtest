from django.urls import path
from apps.accounts.views import (AccountRegistrationView,
                                 AccountLoginView)

urlpatterns = [
    path('registration/', AccountRegistrationView.as_view(), name='registration'),
    path('login/', AccountLoginView.as_view(), name='account_login'),
]
