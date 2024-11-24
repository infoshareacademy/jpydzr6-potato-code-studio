import re
from typing import List
from product import Product


class Cart:
    def __init__(self, products: list):
        self.products = products
        self.basket: List[Product] = []

    def add_product_to_basket(self, new_product_name: str):
        try:
            if not re.match("^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż ]+$", new_product_name):
                print("\nNazwa produktu nie może być liczbą lub znakiem specjalnym.")
                return

            product = next(
                (p for p in self.products if p["name_tag"] == new_product_name), None
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
            if not re.match("^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż ]+$", new_product_name):
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

    def total_price(self):
        total_price_of_products = {sum(product.price for product in self.products)}
        return (
            f"Twój koszyk jest warty: {total_price_of_products} PLN"
            if len(self.products) > 0
            else ""
        )

    def show_cart(self):
        if len(self.basket) == 0:
            print("Twój koszyk jest pusty")
        else:
            for product in self.basket:
                print(f"- {product['name_tag']}, cena: {product['price']:.2f} PLN\n")

    def summary(self):
        self.show_cart()
        total_price = self.total_price()
        total_loyalty_points = self.get_points()

        print(f"\nŁączna kwota: {total_price} PLN")
        print(f"Łączna ilość punktów lojalnościowych: {total_loyalty_points}")
