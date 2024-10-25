from django.urls import path
from .views import EVTypeListView, ChargeEstimateView

urlpatterns = [
    path('ev-types/', EVTypeListView.as_view(), name='ev-types'),
    path('estimate-charge/', ChargeEstimateView.as_view(), name='estimate-charge'),
]
