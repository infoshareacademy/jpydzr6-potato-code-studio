from product import Product
'''
I've decided to create a separate module in order to keep it all clean, 
this func's been made simply for menu purposes, all of magic happens in product.py 

'''

def add_product():
    print("Dodawanie nowego produktu do sklepu:")

    name_tag = input("Podaj nazwę produktu: ").title()
    price = float(input("Podaj cenę produktu: "))
    producer = input("Podaj producenta: ")
    weight = float(input("Podaj wagę produktu (w gramach): "))
    category = input("Podaj kategorię produktu (Warzywa/Owoce): ").title()
    amount = int(input("Podaj ilość produktu: "))
    promo = 0 # by def, can be changed manually :)

    new_product = Product(name_tag, price, producer, weight, category, amount, promo=promo)

    new_product.add_new_product()
    print(f"Produkt {name_tag} został dodany do sklepu!")
