import json

def load_products(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data.get('Products', [])
    except FileNotFoundError:
        print("Nie znaleziono pliku JSON.")
    except json.JSONDecodeError:
        print("Błąd dekodowania pliku JSON.")
    return []

def display_product(product):
    if not isinstance(product, dict):
        return
    fields = {
        'Nazwa': 'name_tag',
        'Cena': 'price',
        'Data ważności': 'exp_date',
        'Promocja': 'promo',
        'Producent': 'producer',
        'Waga': 'weight'
    }

    for name, key in fields.items():
        value = product.get(key, 'No data')
        if key == 'price':
            try:
                value = f"{float(value): .2f} PLN"
            except ValueError:
                value = "Niepoprawna cena produktu"
        print(f"{name}: {value}")

def display_products(products):
    if not products:
        print("Brak produktów do wyświetlenia.")
        return

    for product in products:
        display_product(product)
        print()
