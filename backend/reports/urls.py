from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('revenue/', views.RevenueView.as_view(), name='revenue'),
    path('revenue/update/', views.RevenueFileUpdateView.as_view(), name='revenue-file-update'),
]