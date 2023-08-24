from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('mark_done/<int:order_id>/', views.mark_order_done, name='mark_order_done'),
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),
]
