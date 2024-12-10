from cart import Cart

def first_option_in_payment_choice(cart_pay:Cart):
    while True:
        final_choice = input("Czy potwierdzasz płatność tak / nie ?\n"
                             "Twój wybór:")
        match final_choice:
            case "tak":
                while True:
                    print("Brawo właśnie kupiłeś u nas produkt.\n")
                    cart_pay.basket.clear()
                    return

            case "nie":
                return
            case _:
                print("Spróbuj jeszcze raz. Podałeś zły wybór.\n")

def confirmation_email() -> str:
        email = input("Podaj e-mail, a wyślemy Tobie potwierdzenie zakupu.\n"
                      "Twój e-mail:")
        return email

def payment_menu(cart_pay:Cart):
    while True:
        payment_choice = input("[1] Kup\n"
                               "[2] Powrót do menu\n"
                               "Twój wybór: ")
        match payment_choice:
            case "1":
                confirmation_email()
                first_option_in_payment_choice(cart_pay)
                return

            case "2":
                break

            case _:
                print("Podałeś zły wybór. Spróbuj jeszcze raz.\n")

class Payment:
    def __init__(self, cart_pay):
        self.cart = cart_pay

    def final_payment(self) -> None:
        if not self.cart.basket:
            return
        else:
            while True:
                move_to_payment = input("Czy chcesz przejść do płatności? tak / nie: ")
                match move_to_payment:
                    case "tak":
                        self.cart.total_price()
                        payment_menu(self.cart)
                        break
                    case "nie":
                        print("Wracasz do menu głównego.\n")
                        break
                    case _:
                        print("Podałeś zły wybór. Spróbuj jeszcze raz.\n")
