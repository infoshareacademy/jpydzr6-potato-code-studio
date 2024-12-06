from cart import Cart

cart = Cart()

class Payment(Cart):
    def __init__(self):
        super().__init__()

    def make_basket_empty(self) -> None:
            self.basket = []

    def protection_payment(self) -> None:
        if not self.basket:
            print("Twój koszyk jest pusty nie możesz przejść do płatności.")
            return
        else:
            payment_menu()

def payment_menu(cart_instance:Cart):
    while True:
        payment_choice = input("[1] Przejście do zapłaty\n"
                               "[2] Powrót do menu\n"
                               "Twój wybór: ")

        match payment_choice:

            case "1":
                while True:
                    final_choice = input("Czy na pewno chcesz zapłacić tak / nie ?")

                    match final_choice:
                        case "tak":
                            while True:
                                print("Brawo właśnie kupiłeś u nas produkt.")
                                cart_instance.basket.clear()
                                print("Twój koszyk został opróżniony.")
                                return

                        case "nie":
                            return
                        case _:
                            print("Spróbuj jeszcze raz. Podałeś zły wybór.")
            case "2":
                break

            case _:
                print("Podałeś zły wybór. Spróbuj jeszcze raz.")








