# Menu do projektu "SKLEP Z ŻYWNOŚCIĄ EKOLOGICZNĄ"
# Wersja 1.0
# Potato Code Studio
from products_display import display_products, load_products

from mini_quiz_bio.showing_question import showing_all

if __name__ == "__main__":
    products = load_products("list_of_products.json")
    basket = {}


def menu():
    print('Witamy w sklepie z ekologiczną żywnością "EKO"!')

    while True:
        command = input("""
Wybierz działanie:

[1] Wyświetl produkty
[2] Pokaż koszyk
[3] Dodaj do koszyka
[4] Mini Quiz o tematyce BIO
[Q] Wyjście z programu

    """)

        match command:
            case "1":
                display_products(products)

            case "2":
                pass  # Trzeba to dalej rozwinąć

            case "3":
                pass

            case "4":
                showing_all()

            case "q":
                print("Zapraszamy ponownie!")
                break

            case other:
                print("Niewłaściwy wybór. Spróbuj jeszcze raz")


menu()
