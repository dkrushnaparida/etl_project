from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_sales_data, name='upload'),
    path('data/', views.view_sales_data, name='view_data'),
    path('validation/', views.validation_dashboard, name='validation'),
]
