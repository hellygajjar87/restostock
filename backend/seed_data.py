import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from inventory.models import Category, Item

def seed():
    # Categories
    categories = [
        "Vegetables", "Dairy", "Meat", "Beverages", "Spices", "Grains"
    ]
    
    cat_objs = {}
    for cat_name in categories:
        cat, created = Category.objects.get_or_create(name=cat_name)
        cat_objs[cat_name] = cat
        print(f"Category '{cat_name}' {'created' if created else 'already exists'}")

    # Items
    items = [
        {"name": "Tomatoes", "category": "Vegetables", "quantity": 50, "unit": "kg", "cost_per_unit": 40.0, "reorder_level": 10},
        {"name": "Milk", "category": "Dairy", "quantity": 20, "unit": "L", "cost_per_unit": 60.0, "reorder_level": 5},
        {"name": "Chicken Breast", "category": "Meat", "quantity": 15, "unit": "kg", "cost_per_unit": 250.0, "reorder_level": 5},
        {"name": "Coca Cola", "category": "Beverages", "quantity": 100, "unit": "bottles", "cost_per_unit": 20.0, "reorder_level": 20},
        {"name": "Black Pepper", "category": "Spices", "quantity": 5, "unit": "kg", "cost_per_unit": 800.0, "reorder_level": 1},
        {"name": "Basmati Rice", "category": "Grains", "quantity": 100, "unit": "kg", "cost_per_unit": 120.0, "reorder_level": 20},
    ]

    for item_data in items:
        cat_name = item_data.pop("category")
        item_data["category"] = cat_objs[cat_name]
        item, created = Item.objects.get_or_create(name=item_data["name"], defaults=item_data)
        if not created:
            for key, value in item_data.items():
                setattr(item, key, value)
            item.save()
        print(f"Item '{item.name}' {'created' if created else 'updated'}")

if __name__ == "__main__":
    seed()
