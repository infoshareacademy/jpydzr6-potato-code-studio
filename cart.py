import re


class Cart:
    def __init__(self, products: list):
        self.products = products
        self.basket = []

    def add_product_to_basket(self, new_product_name: str):
        try:
            if not re.match("^[A-Za-z ]+$", new_product_name):
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

    def remove_product(self, index: int):
        if 0 <= index:
            removed_product = self.products.pop(
                index
            )  # It'll delete an item with selected index
            print(f"Produkt {removed_product.name_tag} został usunięty.")
        else:
            print("Nieprawidłowy indeks!")

    def total_price(self):
        total_price_of_products = {sum(product.price for product in self.products)}
        return (
            f"Twój koszyk jest warty: {total_price_of_products} PLN"
            if len(self.products) > 0
            else ""
        )

    def show_cart(self):
        if len(self.products) == 0:
            print("Twój koszyk jest pusty")
        else:
            for product in self.products:
                print(product)
