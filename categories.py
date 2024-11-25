import json
from product import Product

class Categories(Product):

    __slots__ = ("categories", "category1", "category2", "category3")

    def __init__(self, name_tag: str, price: float, producer: str, weight: float, category: str,
                 categories: list):
        super().__init__(name_tag, price, producer, weight, category)

        self.categories = categories
        self.category1 = "Owoce"
        self.category2 = "Warzywa"
        self.category3 = ""

    def __str__(self):
        return f"Nasze kategorie produktów: {self.category1}, {self.category2}"

    def add_new_category(self) -> None:
        new_category = {"category": self.category}

        with open("list_of_products.json", "r") as file:
            data = json.load(file)

        data["Categories"].append(new_category)

        with open("list_of_products.json", "w", encoding="UTF-8") as file:
            json.dump(data, file)

    def remove_last_category(self) -> None:
        new_category = {"category": self.category}

        with open("list_of_products.json", "r") as file:
            data = json.load(file)

        data["Categories"].pop(new_category)

        with open("list_of_products.json", "w", encoding="UTF-8") as file:
            json.dump(data, file)
