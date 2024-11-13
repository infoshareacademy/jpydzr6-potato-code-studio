from datetime import datetime, timedelta


class Product:
    __slots__ = (
        "name_tag", "price", "creation_date", "exp_date", "producer", "weight", "promo", "delivery_time_to_customer",
        "next_delivery_to_warehouse"
    )

    def __init__(self, name_tag: str, price: float, producer: str, weight: float, next_delivery_to_warehouse: int = 14,
                 delivery_time_to_customer: int = 7,
                 promo: int = 0):

        self.name_tag = name_tag
        self.price = price
        self.creation_date: datetime = datetime.today()  # creation as if an entry to the database
        self.exp_date = (self.creation_date + timedelta(days=14)).strftime('%Y-%m-%d')
        self.producer = producer
        self.weight = weight  # in grams
        self.promo = promo
        self.delivery_time_to_customer = delivery_time_to_customer
        self.next_delivery_to_warehouse = next_delivery_to_warehouse

    def __str__(self) -> str:
        """
        Shows an ID of created object and its details
        """
        return (
            f"Produkt: {self.name_tag} o wadze  {self.weight} gramów, wyprodukowany przez '{self.producer}' kosztuje:"
            f" {self.price}PLN "
            f"jest ważny do: ({self.exp_date} i zostanie dostarczony w ciągu {self.delivery_time_to_customer} dni!)")

    def __repr__(self) -> str:
        return (f"Product(id={id(self)}, name_tag={self.name_tag}, price={self.price}, producer={self.producer}, "
                f"weight={self.weight} (In grams!), exp_date={self.exp_date}, "
                f"delivery_time_to_customer={self.delivery_time_to_customer}, "
                f"next_delivery_to_warehouse={self.next_delivery_to_warehouse})"
                )

    def days_until_expiration(self):
        days_left = (self.creation_date + timedelta(
            days=14)) - self.creation_date  # "timedelta(days=14)) - self.creation_date " treat it as exp_date, had to put it that way
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

    def change_promo(self, promo: int) -> None:
        self.promo = promo

    def change_weight(self, new_weight: float) -> None:
        self.weight = new_weight

    def change_price(self, new_price: float) -> None:
        self.price = new_price

    def change_name_tag(self,
                        new_name_tag: str) -> None:  ## I've added these function just in case if someone makes a mistake
        self.name_tag = new_name_tag  ## while providing data, might be useful later on, if not feel free to delete

    def change_producer(self, new_producer: str) -> None:
        self.producer = new_producer

    def change_delivery_time(self,
                             new_delivery_time: int) -> None:  # in case producer, supplier wants to change the promised duration of delivery, by def. it's set up to 7 days
        self.delivery_time_to_customer = new_delivery_time

    def change_next_delivery_to_warehouse(self, new_next_delivery_to_warehouse: int) -> None:
        self.next_delivery_to_warehouse = new_next_delivery_to_warehouse


p1 = Product("Wiśnia 3D", 23, "Farmer X", 2000)
# print(repr(p1)) # an example of __repr__ meth  usage

# Ex. Output
# Product(id=131048121327328, name_tag=Wiśnia 3D, price=23, producer=Farmer X, weight=2000 (In grams!), exp_date=2024-10-29)
# Fell free to correct it if needed :))
