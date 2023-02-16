from django.urls import path

from apps.products.views import (ProductCreationView,
                                 ProductListView,)

urlpatterns = [
    path('create/', ProductCreationView.as_view(), name='product-creation'),
    path('list/', ProductListView.as_view(), name='product-list'),
]