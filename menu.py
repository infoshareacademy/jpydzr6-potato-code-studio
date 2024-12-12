# Menu do projektu "SKLEP Z ŻYWNOŚCIĄ EKOLOGICZNĄ"
# Wersja 1.0
# Potato Code Studio
from products_display import display_products, load_products
from add_product import add_new_product_to_warehouse
from mini_quiz_bio.showing_question import showing_all
from cart import Cart
from product import Product
from payment import Payment

if __name__ == "__main__":
    products = load_products("list_of_products.json")
    basket = {}
    cart = Cart()
    payment_instance = Payment(cart)



def menu():
    print('Witamy w sklepie z ekologiczną żywnością "EKO"!')

    while True:
        command = input("""
Wybierz działanie:

[1] Wyświetl produkty
[2] Pokaż koszyk
[3] Usuń produkt z koszyka
[4] Mini Quiz o tematyce BIO
[5] Dodaj produkt do magazynu
[6] Sortuj produkty
[Q] Wyjście z programu

    """)

        match command:
            case "1":
                products = load_products("list_of_products.json")
                display_products(products)
                cart.add_to_cart_menu()

            case "2":
                cart.show_cart()
                payment_instance.final_payment()

            case "3":
                product_name = input("Nazwa produktu: ")
                cart.remove_product(product_name)

            case "4":
                showing_all()

            case "5":
                add_new_product_to_warehouse()

            case "6":
                products = load_products("list_of_products.json")
                while True:
                    sort_option = input("""
            Wybierz sposób sortowania:
            [a] Cena rosnąco
            [b] Cena malejąco
            [c] Producent A-Z
            [d] Producent Z-A
            [e] Nazwa A-Z
            [f] Nazwa Z-A

                """).lower()
                    match sort_option:
                        case 'a':
                            Product.sort_products(products, 'price', 'asc')
                            break
                        case 'b':
                            Product.sort_products(products, 'price', 'desc')
                            break
                        case 'c':
                            Product.sort_products(products, 'producer', 'asc')
                            break
                        case 'd':
                            Product.sort_products(products, 'producer', 'desc')
                            break
                        case 'e':
                            Product.sort_products(products, 'name', 'asc')
                            break
                        case 'f':
                            Product.sort_products(products, 'name', 'desc')
                            break
                        case _:
                            print("Niewłaściwy wybór. Spróbuj jeszcze raz.")

            case "q":
                print("Zapraszamy ponownie!")
                break
            case _:
                print("Niewłaściwy wybór. Spróbuj jeszcze raz")


menu()
