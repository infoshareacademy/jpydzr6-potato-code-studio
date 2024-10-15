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
            removed_product = self.products.pop(index)  # Usuwa produkt z podanym indeksie
            print(f"Produkt {removed_product.name_tag} został usunięty.")
        else:
            print("Nieprawidłowy indeks!")

    def total_price(self):
        return  f"Twój koszyk jest warty: {sum(product.price for product in self.products)} PLN"

    def show_cart(self):
        if len(self.products) == 0:
            print("Twój koszyk jest pusty")
        else:
            for product in self.products:
                print(product)


