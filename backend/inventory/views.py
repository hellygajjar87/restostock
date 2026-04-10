from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum, F, DecimalField
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Item, Transaction, Alert, Category
from .serializers import ItemSerializer, TransactionSerializer, AlertSerializer, CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @action(detail=False, methods=['get'])
    def metrics(self, request):
        total_items = Item.objects.count()
        low_stock = Item.objects.filter(status='low-stock').count()
        out_of_stock = Item.objects.filter(status='out-of-stock').count()
        expiring = Item.objects.filter(status='expiring-soon').count()
        
        # Calculate total value using DB aggregation
        total_value = Item.objects.aggregate(
            total=Sum(F('quantity') * F('cost_per_unit'), output_field=DecimalField())
        )['total'] or 0
        
        return Response({
            'totalItems': total_items,
            'lowStockItems': low_stock,
            'outOfStockItems': out_of_stock,
            'expiringItems': expiring,
            'totalValue': float(total_value),
            'categories': Category.objects.count(),
        })

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-date')
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        # Override create to update inventory quantity
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        transaction_type = serializer.validated_data['type']
        quantity = serializer.validated_data['quantity']
        item = serializer.validated_data.get('item')
        
        if item:
            if transaction_type in ['purchase', 'return']:
                item.quantity += quantity
            elif transaction_type in ['usage', 'wastage']:
                item.quantity -= quantity
            
            # Populate required fields for Transaction
            serializer.validated_data['item_name'] = item.name
            serializer.validated_data['user'] = request.user.username if request.user.is_authenticated else 'System'
            
            item.save() # This now handles status update
            serializer.validated_data['balance_after'] = item.quantity
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all().order_by('-date')
    serializer_class = AlertSerializer

# Template Views
@login_required
def dashboard(request):
    total_items = Item.objects.count()
    low_stock = Item.objects.filter(status='low-stock').count()
    out_of_stock = Item.objects.filter(status='out-of-stock').count()
    expiring = Item.objects.filter(status='expiring-soon').count()
    total_value = Item.objects.aggregate(
        total=Sum(F('quantity') * F('cost_per_unit'), output_field=DecimalField())
    )['total'] or 0
    
    recent_transactions = Transaction.objects.all().order_by('-date')[:5]
    recent_alerts = Alert.objects.all().order_by('-date')[:5]
    
    context = {
        'totalItems': total_items,
        'lowStockItems': low_stock,
        'outOfStockItems': out_of_stock,
        'expiringItems': expiring,
        'totalValue': float(total_value),
        'categories': Category.objects.count(),
        'recent_transactions': recent_transactions,
        'recent_alerts': recent_alerts,
        'low_stock_count': low_stock + out_of_stock,
    }
    return render(request, 'inventory/dashboard.html', context)

@login_required
def inventory_list(request):
    category_id = request.GET.get('category')
    items = Item.objects.all().order_by('name')
    if category_id:
        items = items.filter(category_id=category_id)
    
    categories = Category.objects.all()
    context = {
        'items': items,
        'categories': categories,
        'low_stock_count': Item.objects.filter(status__in=['low-stock', 'out-of-stock']).count(),
    }
    return render(request, 'inventory/inventory_list.html', context)

@login_required
def transaction_list(request):
    transactions = Transaction.objects.all().order_by('-date')
    context = {
        'transactions': transactions,
        'low_stock_count': Item.objects.filter(status__in=['low-stock', 'out-of-stock']).count(),
    }
    return render(request, 'inventory/transaction_list.html', context)

@login_required
def alerts(request):
    alerts = Alert.objects.all().order_by('-date')
    context = {
        'alerts': alerts,
        'low_stock_count': Item.objects.filter(status__in=['low-stock', 'out-of-stock']).count(),
    }
    return render(request, 'inventory/alerts.html', context)

@login_required
def reports(request):
    # Dummy data for demonstration as in React
    context = {
        'low_stock_count': Item.objects.filter(status__in=['low-stock', 'out-of-stock']).count(),
    }
    return render(request, 'inventory/reports.html', context)
