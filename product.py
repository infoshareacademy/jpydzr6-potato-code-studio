from datetime import datetime, timedelta

class Product:
    __slots__ = ("name_tag", "price", "creation_date", "exp_date", "producer", "weight", "promo")
    def __init__(self, name_tag: str, price: float, producer: str, weight: float, promo: int = 0):
        self.name_tag = name_tag
        self.price = price
        self.creation_date: datetime = datetime.today() # creation as if an entry to the database
        self.exp_date =  (self.creation_date  + timedelta(days=14)).strftime('%Y-%m-%d')
        self.producer = producer
        self.weight = weight # in grams
        self.promo = promo


    def __str__(self):
        """
        Shows an ID of created object and its details
        """
        return (f"Produkt: {self.name_tag} o wadze  {self.weight} gramów ,wyprodukowany przez '{self.producer}' kosztuje: {self.price}PLN "
                f"jest ważny do: ({self.exp_date})")

    def __repr__(self):
        return f"Product(id={id(self)}, name_tag={self.name_tag}, price={self.price}, producer={self.producer}, weight={self.weight} (In grams!), exp_date={self.exp_date})"



    def days_until_expiration(self):
        days_left = (self.creation_date  + timedelta(days=14)) - self.creation_date  # "timedelta(days=14)) - self.creation_date " treat it as exp_date, had to put it that way
        return days_left.days

    def to_dict(self) -> dict:
        return {
            "name_tag": self.name_tag,
            "price": self.price,
            "creation_date": self.creation_date.strftime("%Y-%m-%d"),
            "exp_date": self.exp_date,
            "producer": self.producer,
            "weight": self.weight,
        }

    def change_promo(self, promo: int):
        self.promo += promo

    def change_weight(self, new_weight: float):
        self.weight = new_weight

    def change_price(self, new_price: float):
        self.price = new_price

    def change_name_tag(self, new_name_tag: str): ## I've added these function just in case if someone makes a mistake
        self.name_tag = new_name_tag              ## while providing data, might be useful later on, if not feel free to delete

    def change_producer(self, new_producer: str):
        self.producer = new_producer


p1 = Product("Wiśnia 3D", 23, "Farmer X", 2000)
# print(repr(p1)) # an example of __repr__ meth  usage

# Ex. Output
# Product(id=131048121327328, name_tag=Wiśnia 3D, price=23, producer=Farmer X, weight=2000 (In grams!), exp_date=2024-10-29)
# Fell free to correct it if needed :))
