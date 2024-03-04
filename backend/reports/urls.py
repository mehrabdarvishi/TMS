from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('revenue/', views.RevenueView.as_view(), name='revenue')
]