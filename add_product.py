from product import Product

'''
I've decided to create a separate module in order to keep it all clean, 
this func's been made simply for menu purposes, all of magic happens in product.py 

'''


def get_input(prompt, validation_func, error_message):
    while True:
        user_input = input(prompt)
        if validation_func(user_input):
            return user_input
        else:
            print(error_message)


def is_positive_float(value):
    try:
        value = float(value)
        return value > 0
    except ValueError:
        return False


def is_positive_int(value):
    try:
        value = int(value)
        return value > 0
    except ValueError:
        return False


def is_valid_category(value):
    return value.title() in ["Warzywa", "Owoce"]


def is_empty_string(text):
    try:
        text = text.strip()
        return text != ""
    except ValueError:
        return False


def add_new_product_to_warehouse():
    name_tag = get_input("Podaj nazwę produktu: ", is_empty_string, "To miejsce nie może być puste!").title()
    price = float(get_input("Podaj cenę produktu: ", is_positive_float, "Cena musi być liczbą większą niż 0!"))
    producer = get_input("Podaj producenta: ",is_empty_string, "To miejsce nie może być puste!" )
    weight = float(get_input("Podaj wagę produktu (w gramach): ", is_positive_float, "Waga musi być liczbą większą niż 0!"))
    category = get_input("Podaj kategorię produktu (Warzywa/Owoce): ", is_valid_category,
                         "Kategoria musi się nazywać 'Warzywa' lub 'Owoce'!")
    amount = int(get_input("Podaj ilość produktu: ", is_positive_int, "Ilość musi być liczbą  większą niż 0!"))
    promo = 0  # by default, can be changed manually :)

    new_product = Product(name_tag, price, producer, weight, category, amount, promo=promo)

    new_product.add_new_product()
    print(f"Produkt {name_tag} został dodany do sklepu!")


