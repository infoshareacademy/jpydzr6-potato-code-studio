import json
from cart import Cart


def load_products(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data.get("Products", [])
    except FileNotFoundError:
        print("Nie znaleziono pliku JSON.")
    except json.JSONDecodeError:
        print("Błąd dekodowania pliku JSON.")
    return []


def display_product(product):
    if not isinstance(product, dict):
        return
    fields = {
        "Nazwa": "name_tag",
        "Cena": "price",
        "Data ważności": "exp_date",
        "Promocja": "promo",
        "Producent": "producer",
        "Waga": "weight",
    }

    for name, key in fields.items():
        value = product.get(key, "No data")
        if key == "price":
            try:
                value = f"{float(value): .2f} PLN"
            except ValueError:
                value = "Niepoprawna cena produktu"
        print(f"{name}: {value}")


def display_products(products, cart):
    if not products:
        print("Brak produktów do wyświetlenia.")
        return

    for product in products:
        display_product(product)
        print()

    while True:
        print("\n1. Dodaj produkt do koszyka")
        print("2. Wróć do głównego menu")

        option = input("Wybierz opcje: ")
        match option:
            case "1":
                new_product_name = input("\nNazwa produktu: ")
                cart.add_product_to_basket(new_product_name)
            case "2":
                break
            case _:
                print("Nie ma takiej opcji")
