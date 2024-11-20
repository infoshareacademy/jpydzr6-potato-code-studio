

from product import  Product
class Cart:

    def __init__(self):
        self.products = []

    def add_product(self, product: Product):
        if isinstance(product, Product):
          self.products.append(product)

        else:
            raise TypeError("This has to be an instance of Product")

    def remove_product(self, index: int):
        if 0 <= index:
            removed_product = self.products.pop(index)  # It'll delete an item with selected index
            print(f"Produkt {removed_product.name_tag} został usunięty.")
        else:
            print("Nieprawidłowy indeks!")

    def total_price(self):
        total_price_of_products = {sum(product.price for product in self.products)}
        return f"Twój koszyk jest warty: {total_price_of_products} PLN" if len(self.products) > 0 else ""

    def show_cart(self):
        if len(self.products) == 0:
            print("Twój koszyk jest pusty")
        else:
            for product in self.products:
                print(product)

    def summary(self):
        self.show_cart()
        total_price = self.total_price()
        total_loyalty_points = self.get_points()

        print(f"\nŁączna kwota: {total_price} PLN")
        print(f"Łączna ilość punktów lojalnościowych: {total_loyalty_points}")