import os
import django
import sys
from datetime import datetime

# Setup Django environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from inventory.models import Category, Item, Transaction, Alert

def transition_to_veg():
    print("Starting Vegetarian Transition...")
    
    # 1. Create/Ensure new categories exist
    plant_protein, _ = Category.objects.get_or_create(name='Plant Proteins')
    veg_cat, _ = Category.objects.get_or_create(name='Vegetables')
    
    # 2. Update Items
    # Chicken Breast -> Hard Tofu
    items_to_update = Item.objects.filter(name='Chicken Breast')
    for item in items_to_update:
        print(f"Updating Item: {item.name} -> Hard Tofu")
        item.name = 'Hard Tofu'
        item.category = plant_protein
        item.supplier = 'Premium Soy Foods'
        item.save()
        
    # Salmon Fillets -> Portobello Mushrooms
    items_to_update = Item.objects.filter(name='Salmon Fillets')
    for item in items_to_update:
        print(f"Updating Item: {item.name} -> Portobello Mushrooms")
        item.name = 'Portobello Mushrooms'
        item.category = veg_cat
        item.save()
        
    # 3. Update Transactions
    transactions = Transaction.objects.filter(item_name='Chicken Breast')
    for tx in transactions:
        print(f"Updating Transaction for: {tx.item_name}")
        tx.item_name = 'Hard Tofu'
        tx.save()
        
    transactions = Transaction.objects.filter(item_name='Salmon Fillets')
    for tx in transactions:
        print(f"Updating Transaction for: {tx.item_name}")
        tx.item_name = 'Portobello Mushrooms'
        tx.save()
        
    # 4. Update Alerts
    alerts = Alert.objects.filter(item_name='Chicken Breast')
    for al in alerts:
        print(f"Updating Alert for: {al.item_name}")
        al.item_name = 'Hard Tofu'
        al.category = 'Plant Proteins'
        al.save()
        
    alerts = Alert.objects.filter(item_name='Salmon Fillets')
    for al in alerts:
        print(f"Updating Alert for: {al.item_name}")
        al.item_name = 'Portobello Mushrooms'
        al.category = 'Vegetables'
        al.save()
        
    # 5. Cleanup Categories
    for cat_name in ['Meat', 'Seafood']:
        try:
            cat = Category.objects.get(name=cat_name)
            if cat.items.count() == 0:
                print(f"Deleting empty category: {cat_name}")
                cat.delete()
        except Category.DoesNotExist:
            pass

    print("Transition completed successfully!")

if __name__ == "__main__":
    transition_to_veg()
