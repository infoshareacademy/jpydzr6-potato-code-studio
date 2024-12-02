# Menu do projektu "SKLEP Z ŻYWNOŚCIĄ EKOLOGICZNĄ"
# Wersja 1.0
# Potato Code Studio
from products_display import display_products, load_products
from add_product import add_new_product
from mini_quiz_bio.showing_question import showing_all
from cart import Cart


if __name__ == "__main__":
    products = load_products("list_of_products.json")
    basket = {}
    cart = Cart()


def menu():
    print('Witamy w sklepie z ekologiczną żywnością "EKO"!')

    while True:
        command = input("""
Wybierz działanie:

[1] Wyświetl produkty
[2] Pokaż koszyk
[3] Usuń produkt z koszuka
[4] Mini Quiz o tematyce BIO
[5] Dodaj produkt do magazynu
[Q] Wyjście z programu

    """)

        match command:
            case "1":
                display_products(products)
                cart.add_to_cart_menu()
            case "2":
                cart.show_cart()

            case "3":
                product_name = input("Nazwa produktu: ")
                cart.remove_product(product_name)

            case "4":
                showing_all()

            case "5":
                add_new_product()

            case "q":
                print("Zapraszamy ponownie!")
                break

            case other:
                print("Niewłaściwy wybór. Spróbuj jeszcze raz")


menu()
