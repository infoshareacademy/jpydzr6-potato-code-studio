import json

def wczytaj_produkty(nazwa_pliku):
    try:
        with open(nazwa_pliku, 'r') as plik:
            dane = json.load(plik)
        return dane.get('Products', [])
    except FileNotFoundError:
        print("Plik JSON nie został znaleziony.")
    except json.JSONDecodeError:
        print("Błąd dekodowania pliku JSON.")
    return []

def wyswietl_produkt(produkt):
    if not isinstance(produkt, dict):
        return
    pola = {
        'Nazwa': 'name_tag',
        'Cena': 'price',
        'Data ważności': 'exp_date',
        'Promocja': 'promo',
        'Producent': 'producer',
        'Waga': 'weight'
    }

    for nazwa, klucz in pola.items():
        print(f"{nazwa}: {produkt.get(klucz, 'Brak danych')}")

def wyswietl_produkty(produkty):
    if not produkty:
        print("Brak produktów do wyświetlenia.")
        return

    for produkt in produkty:
        wyswietl_produkt(produkt)
        print()

def main():
    nazwa_pliku = 'list_of_products.json'
    produkty = wczytaj_produkty(nazwa_pliku)

    while True:
        print("Menu: \n0. Zakończ \n1. Wyświetl listę produktów")
        wybor = input("Wybierz opcję: ")

        if wybor == '1':
            wyswietl_produkty(produkty)
        elif wybor == '0':
            break
        else:
            print("Nieprawidłowa opcja, spróbuj ponownie.")

if __name__ == "__main__":
    main()