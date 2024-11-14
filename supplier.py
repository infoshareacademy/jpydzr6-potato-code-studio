import json
from user import User

class Supplier(User):

    __slots__ = ("f_name", "l_name", "address", "email", "telephone", "is_supplier", "suppliers", "category")

    def __init__(self, f_name: str, l_name: str, address: str, email: str, telephone: str, is_supplier: bool):
        # Inheritance
        super().__init__(f_name, l_name, address, email, telephone, loyalty_points=0)
        # Attributes of this class
        self.is_supplier = True
        self.suppliers = {}
        self.category = {}

    def add_supplier_name(self, f_name: str, l_name: str) -> None:
        full_name = f"{f_name} {l_name}"
        self.suppliers[full_name] = {"first_name": f_name, "last_name": l_name}

    def add_supplier_details(self, address: str, email: str, telephone: str) -> None:
        full_address = f"{address}, {email}, {telephone}"
        self.suppliers[full_address] = {"customer_address": address, "email": email, "telephone": telephone}

    def get_suppliers(self) -> dict:
        return self.suppliers

    def save_suppliers_to_file(self) -> None:
        record = self.suppliers
        with open("suppliers_details.json", mode="w", encoding="UTF-8") as file:
            json.dump(record, file)

    def save_categories_to_file(self) -> None:
        record = self.category
        with open("supplier_categories.json", mode="w", encoding="UTF-8") as file:
            json.dump(record, file)


### TESTING ###
s1 = Supplier("Jan", "Jabłko", "Jabłkowa 1, 10-100 Jabłoniowo", "jablko@wp.pl",
              "100 200 100", True)
s2 = Supplier("Grzegorz", "Gruszka", "Gruszkowa 5, 50-550 Gruszkowo", "gruszek@gmail.com",
              "605 605 605", True)

# if __name__ == '__main__':
#     print(s1.get_suppliers())
#     s1.add_supplier_name("Basia", "Basiowska")
#     print(s1.get_suppliers())
#     s1.save_suppliers_to_file()
#     s1.save_categories_to_file()
