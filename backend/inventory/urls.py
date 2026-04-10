from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'alerts', views.AlertViewSet)
router.register(r'categories', views.CategoryViewSet)

urlpatterns = [
    # Template Views
    path('', views.dashboard, name='dashboard'),
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('alerts/', views.alerts, name='alerts'),
    path('reports/', views.reports, name='reports'),
    
    # API Routes
    path('api/', include(router.urls)),
]
