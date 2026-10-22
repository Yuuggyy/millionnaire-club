from django.urls import path

from . import views

urlpatterns = [
    path("submitOrder/", views.api_submit_order, name="api-submit-order"),
    path("callWaiter/", views.api_call_waiter, name="api-call-waiter"),
    path("stats/", views.api_stats, name="api-stats"),
]
