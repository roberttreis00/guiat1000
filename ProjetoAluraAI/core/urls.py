from django.urls import path
from .views import GuiaT1000

urlpatterns = [
    path('', GuiaT1000.as_view(), name='index'),
]