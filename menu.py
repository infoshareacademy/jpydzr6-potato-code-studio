# Menu do projektu "SKLEP Z ŻYWNOŚCIĄ EKOLOGICZNĄ"
# Wersja 1.0
# Potato Code Studio

if __name__ == '__main__':

    produkty = {}
    koszyk = {}
    dodawanie_do_koszyka = {}

    def menu():
        while True:
            command = input("""
    Witamy w sklepie z ekologiczną żywnością "EKO"!
    
    
    Wybierz działanie:
                            
    [1] Wyświetl produkty
    [2] Pokaż koszyk
    [3] Dodaj do koszyka
    [Q] Wyjście z programu
                            
    """)


            match command:
                case "1":
                    pass # Trzeba to dalej rozwinąć

                case "2":
                    pass # Trzeba to dalej rozwinąć

                case "3":
                    pass # Trzeba to dalej rozwinąć

                case "q":
                    print("Zapraszamy ponownie!")
                    break

                case other:
                    print("Niewłaściwy wybór. Spróbuj jeszcze raz")

    menu()
