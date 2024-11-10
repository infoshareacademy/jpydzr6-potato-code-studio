import json

def load_products(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data.get('Products', [])
    except FileNotFoundError:
        print("JSON file not found.")
    except json.JSONDecodeError:
        print("JSON file decoding error.")
    return []

def display_product(product):
    if not isinstance(product, dict):
        return
    fields = {
        'Name': 'name_tag',
        'Price': 'price',
        'Expiry date': 'exp_date',
        'Discount': 'promo',
        'Producer': 'producer',
        'Weight': 'weight'
    }

    for name, key in fields.items():
        value = product.get(key, 'No data')
        if key == 'price' and isinstance(value, (int, float)):
            value = f"{value: .2f} PLN"
        print(f"{name}: {value}")

def display_products(products):
    if not products:
        print("No products to display.")
        return

    for product in products:
        display_product(product)
        print()
