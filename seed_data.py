import os
import django
import sys
from datetime import datetime

# Setup Django environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from inventory.models import Category, Item, Transaction, Alert

def seed():
    print("Seeding data...")
    
    # 1. Categories
    categories_names = [
        'Vegetables', 'Plant Proteins', 'Oils & Condiments', 'Dairy', 
        'Dry Goods', 'Herbs & Spices', 'Beverages'
    ]
    category_map = {}
    for name in categories_names:
        cat, _ = Category.objects.get_or_create(name=name)
        category_map[name] = cat
    
    # 2. Items
    inventory_data = [
        {
            'id': '1', 'name': 'Tomatoes', 'category': 'Vegetables', 'quantity': 45, 'unit': 'kg',
            'reorderLevel': 20, 'costPerUnit': 3.5, 'supplier': 'Fresh Farm Co.',
            'expiryDate': '2026-04-15', 'location': 'Cold Storage A', 'status': 'in-stock',
        },
        {
            'id': '2', 'name': 'Hard Tofu', 'category': 'Plant Proteins', 'quantity': 12, 'unit': 'kg',
            'reorderLevel': 15, 'costPerUnit': 12.5, 'supplier': 'Premium Soy Foods',
            'expiryDate': '2026-04-09', 'location': 'Freezer B', 'status': 'low-stock',
        },
        {
            'id': '3', 'name': 'Olive Oil', 'category': 'Oils & Condiments', 'quantity': 28, 'unit': 'liters',
            'reorderLevel': 10, 'costPerUnit': 8.0, 'supplier': 'Mediterranean Imports',
            'expiryDate': '2027-01-20', 'location': 'Dry Storage', 'status': 'in-stock',
        },
        {
            'id': '4', 'name': 'Fresh Mozzarella', 'category': 'Dairy', 'quantity': 8, 'unit': 'kg',
            'reorderLevel': 10, 'costPerUnit': 9.5, 'supplier': 'Artisan Cheese Co.',
            'expiryDate': '2026-04-10', 'location': 'Cold Storage A', 'status': 'expiring-soon',
        },
        {
            'id': '5', 'name': 'Pasta (Spaghetti)', 'category': 'Dry Goods', 'quantity': 150, 'unit': 'kg',
            'reorderLevel': 50, 'costPerUnit': 2.2, 'supplier': 'Italian Imports',
            'expiryDate': '2027-08-15', 'location': 'Dry Storage', 'status': 'in-stock',
        },
        {
            'id': '6', 'name': 'Portobello Mushrooms', 'category': 'Vegetables', 'quantity': 0, 'unit': 'kg',
            'reorderLevel': 8, 'costPerUnit': 18.5, 'supplier': 'Ocean Fresh',
            'expiryDate': '2026-04-08', 'location': 'Freezer A', 'status': 'out-of-stock',
        },
        {
            'id': '7', 'name': 'Basil (Fresh)', 'category': 'Herbs & Spices', 'quantity': 3, 'unit': 'kg',
            'reorderLevel': 2, 'costPerUnit': 15.0, 'supplier': 'Herb Garden',
            'expiryDate': '2026-04-11', 'location': 'Cold Storage B', 'status': 'in-stock',
        },
        {
            'id': '8', 'name': 'Heavy Cream', 'category': 'Dairy', 'quantity': 6, 'unit': 'liters',
            'reorderLevel': 12, 'costPerUnit': 4.5, 'supplier': 'Dairy Best',
            'expiryDate': '2026-04-09', 'location': 'Cold Storage A', 'status': 'low-stock',
        },
        {
            'id': '9', 'name': 'Garlic', 'category': 'Vegetables', 'quantity': 18, 'unit': 'kg',
            'reorderLevel': 8, 'costPerUnit': 6.0, 'supplier': 'Fresh Farm Co.',
            'expiryDate': '2026-05-01', 'location': 'Dry Storage', 'status': 'in-stock',
        },
        {
            'id': '10', 'name': 'Butter', 'category': 'Dairy', 'quantity': 22, 'unit': 'kg',
            'reorderLevel': 15, 'costPerUnit': 7.5, 'supplier': 'Dairy Best',
            'expiryDate': '2026-05-15', 'location': 'Cold Storage A', 'status': 'in-stock',
        },
        {
            'id': '11', 'name': 'White Wine', 'category': 'Beverages', 'quantity': 45, 'unit': 'bottles',
            'reorderLevel': 30, 'costPerUnit': 12.0, 'supplier': 'Wine & Spirits Co.',
            'expiryDate': '2028-12-31', 'location': 'Wine Cellar', 'status': 'in-stock',
        },
        {
            'id': '12', 'name': 'Flour (All-Purpose)', 'category': 'Dry Goods', 'quantity': 85, 'unit': 'kg',
            'reorderLevel': 40, 'costPerUnit': 1.8, 'supplier': 'Bakery Supplies Inc.',
            'expiryDate': '2026-10-20', 'location': 'Dry Storage', 'status': 'in-stock',
        },
    ]
    
    item_map = {}
    for data in inventory_data:
        item, _ = Item.objects.update_or_create(
            id=data['id'],
            defaults={
                'name': data['name'],
                'category': category_map[data['category']],
                'quantity': data['quantity'],
                'unit': data['unit'],
                'reorder_level': data['reorderLevel'],
                'cost_per_unit': data['costPerUnit'],
                'supplier': data['supplier'],
                'expiry_date': datetime.strptime(data['expiryDate'], '%Y-%m-%d').date(),
                'location': data['location'],
                'status': data['status'],
            }
        )
        item_map[data['name']] = item

    # 3. Transactions
    transaction_data = [
        {'itemName': 'Tomatoes', 'type': 'purchase', 'quantity': 50, 'unit': 'kg', 'date': '2026-04-07T09:30:00', 'user': 'John Smith (Manager)', 'balanceAfter': 45},
        {'itemName': 'Hard Tofu', 'type': 'usage', 'quantity': 8, 'unit': 'kg', 'date': '2026-04-07T14:15:00', 'user': 'Maria Garcia (Chef)', 'balanceAfter': 12},
        {'itemName': 'Portobello Mushrooms', 'type': 'usage', 'quantity': 6, 'unit': 'kg', 'date': '2026-04-07T16:45:00', 'user': 'Maria Garcia (Chef)', 'balanceAfter': 0},
        {'itemName': 'Fresh Mozzarella', 'type': 'wastage', 'quantity': 2, 'unit': 'kg', 'date': '2026-04-07T10:00:00', 'user': 'David Lee (Staff)', 'balanceAfter': 8},
    ]
    
    for tr in transaction_data:
        Transaction.objects.update_or_create(
            item=item_map.get(tr['itemName']),
            item_name=tr['itemName'],
            date=tr['date'],
            defaults={
                'type': tr['type'],
                'quantity': tr['quantity'],
                'unit': tr['unit'],
                'user': tr['user'],
                'balance_after': tr['balanceAfter']
            }
        )
        
    # 4. Alerts
    alert_data = [
        {'type': 'out-of-stock', 'itemName': 'Portobello Mushrooms', 'message': 'Item is out of stock.', 'severity': 'critical', 'date': '2026-04-07T16:45:00', 'category': 'Vegetables'},
        {'type': 'low-stock', 'itemName': 'Hard Tofu', 'message': 'Stock level below reorder point.', 'severity': 'warning', 'date': '2026-04-07T14:15:00', 'category': 'Plant Proteins'},
    ]
    
    for al in alert_data:
        Alert.objects.update_or_create(
            item=item_map.get(al['itemName']),
            item_name=al['itemName'],
            date=al['date'],
            defaults={
                'type': al['type'],
                'message': al['message'],
                'severity': al['severity'],
                'category': al['category']
            }
        )
        
    print("Seeding completed successfully!")

if __name__ == "__main__":
    seed()
