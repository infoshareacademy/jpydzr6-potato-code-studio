import re
from typing import List
from product import Product
from products_display import load_products


class Cart:
    product_name_validation = "^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż ]+$"
    product_data = load_products("list_of_products.json")

    def __init__(self):
        self.basket: List[Product] = []

    def add_product_to_basket(self, new_product_name: str):
        try:
            if not re.match(self.product_name_validation, new_product_name):
                print("\nNazwa produktu nie może być liczbą lub znakiem specjalnym.")
                return

            product = next(
                (p for p in self.product_data if p["name_tag"] == new_product_name),
                None,
            )
            if product:
                self.basket.append(product)
                print(f"\nProdukt {new_product_name} został dodany!")
            else:
                print(f"\nProdukt {new_product_name} nie został znaleziony!")
        except AttributeError as e:
            print(f"\nError: {e}.")

    def remove_product(self, new_product_name: str):
        try:
            if not re.match(self.product_name_validation, new_product_name):
                print("\nNazwa produktu nie może być liczbą lub znakiem specjalnym.")
                return

            product = next(
                (p for p in self.basket if p["name_tag"] == new_product_name), None
            )
            if product:
                self.basket.remove(product)
                print(f"\nProdukt {new_product_name} został usunięty!")
            else:
                print(f"\nProdukt {new_product_name} nie został znaleziony!")
        except AttributeError as e:
            print(f"\nError: {e}.")

    def add_to_cart_menu(self):
        while True:
            print("\n1. Dodaj produkt do koszyka")
            print("2. Wróć do głównego menu")

            option = input("Wybierz opcje: ")
            match option:
                case "1":
                    new_product_name = input("\nNazwa produktu: ")
                    self.add_product_to_basket(new_product_name)
                case "2":
                    break
                case _:
                    print("Nie ma takiej opcji")

    def total_price(self):
        try:
            if len(self.basket) == 0:
                print("Twój koszyk jest pusty")
            total_price_of_products = sum(product["price"] for product in self.basket)
            print(f"Twój koszyk jest warty: {total_price_of_products} PLN")
            return total_price_of_products
        except Exception as e:
            print(f"Nieoczekiwany błąd: {e}")

    def get_points(self) -> int:
        return sum(int(product["loyalty_points"]) for product in self.basket)

    def show_cart(self):
        if len(self.basket) == 0:
            print("Twój koszyk jest pusty")
        else:
            for product in self.basket:
                name = product.get("name_tag", "Unknown")
                price = product.get("price", 0.0)

                try:
                    price = float(price)
                except ValueError:
                    price = 0.0

                print(f"- {name}, cena: {price:.2f} PLN")

    def summary(self):
        self.show_cart()
        total_price = self.total_price()
        total_loyalty_points = self.get_points()

        print(f"\nŁączna kwota: {total_price:.2f} PLN")
        print(f"Łączna ilość punktów lojalnościowych: {total_loyalty_points}")
