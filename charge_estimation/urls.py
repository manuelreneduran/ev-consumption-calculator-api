from django.urls import path
from .views import EVTypeListView, EVTypeDropdownView, ChargeEstimateView

urlpatterns = [
    path('evs/', EVTypeListView.as_view(), name='ev_type_list'),
    path('evs/dropdown/', EVTypeDropdownView.as_view(), name='ev_type_dropdown'),
    path('estimate-charge/', ChargeEstimateView.as_view(), name='estimate-charge'),
]
