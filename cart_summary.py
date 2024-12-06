from product import Product
from mod_loyalty import Mod_loyalty
import unicodedata

class CartSummary(Mod_loyalty):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "\n".join(
            f"{product.name_tag}: {product.price} PLN"
            for product in self.products
        )

    def show_cart(self):
        if not self.products:
            print("Twój koszyk jest pusty")
        else:
            print("\nProdukty w koszyku:")
            for product in self.products:
                print(f"- {product.name_tag}: {product.price} PLN, Punkty lojalnościowe: {product.price * 5}")

    def total_price(self):
        return sum(product.price for product in self.products)

    def summary(self):
        self.show_cart()
        total_price = self.total_price()
        total_loyalty_points = self.get_points()

        print(f"\nŁączna kwota: {total_price} PLN")
        print(f"Łączna ilość punktów lojalnościowych: {total_loyalty_points}")

    def add_product(self, product: Product):
        if isinstance(product, Product):
            self.products.append(product)
            self.add_points(product.price)
        else:
            raise TypeError("Produkt musi być instancją klasy Product")

def display_products(products):
    if not products:
        print("Brak produktów do wyświetlenia.")
        return
    print("\nProdukty dostępne do dodania:")
    for product in products:
        print(f"- {product.name_tag}: {product.price} PLN")

def add_product_to_cart(cart, available_products):
    display_products(available_products)
    product_choice = input("Podaj nazwę produktu, który chcesz dodać: ")
    normalized_choice = normalize_string(product_choice)
    product_added = False  # Flag to check if product was found
    for product in available_products:
        if normalize_string(product.name_tag) == normalized_choice:
            cart.add_product(product)
            print(f"Produkt {product.name_tag} dodano do koszyka.")
            return product
    if not product_added:
        print("Nie znaleziono produktu o podanej nazwie.")
    return None

def main():
    cart = CartSummary()

    # Example products
    available_products = [
        Product("Wiśnia 3D", 23, "Farmer X", 2000),
        Product("Jabłko", 10, "Farmer Y", 1500),
        Product("Gruszka", 12, "Farmer Z", 1000),
        Product("Mango", 30, "Farmer A", 1500),
    ]

    while True:
        print("\nDostępne opcje:\n1. Kontynuuj zakupy\n2. Przejdź do płatności")

        total_price = cart.total_price()
        if total_price < 10:
            print("3. Dodaj produkt do koszyka i pomnóż swoje punkty")
        choice = input("Wybierz opcję: ")
        if choice == "1":
            add_product_to_cart(cart, available_products)
        elif choice == "2":
            print("Przechodzimy do płatności...")
            break
        elif choice == "3" and total_price < 10:
            print("Dodaj produkt do koszyka i pomnóż swoje punkty")
            product = add_product_to_cart(cart, available_products)
            if product:
                cart.loyalty_points *= 2
                print(f"Twoje punkty lojalnościowe zostały podwojone! Aktualne punkty: {cart.loyalty_points}")
        else:
            print("Nieprawidłowy wybór, spróbuj ponownie")

        cart.summary()

if __name__ == '__main__':
    main()
