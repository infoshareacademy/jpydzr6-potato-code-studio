import json

class Supplier:

    __slots__ = ("supplier_f_name", "supplier_l_name", "supplier_address", "supplier_email", "supplier_telephone", "suppliers", "category")

    def __init__(self, supplier_f_name: str, supplier_l_name: str, supplier_address: str, supplier_email: str,
                 supplier_telephone: str):
        self.supplier_f_name = supplier_f_name
        self.supplier_l_name = supplier_l_name
        self.supplier_address = supplier_address
        self.supplier_email = supplier_email
        self.supplier_telephone = supplier_telephone
        self.suppliers = {}
        self.category = {}

    def __str__(self) -> str:
        return (
            f"\nImię i nazwisko dostawcy: {self.supplier_f_name} {self.supplier_l_name}"
            f"\nAdres dostawcy: {self.supplier_address}"
            f"\nE-mail dostawcy: {self.supplier_email}"
            f"\nTelefon dostawcy: {self.supplier_telephone}"
        )

    def add_supplier_name(self, supplier_f_name: str, supplier_l_name: str) -> None:
        full_name = f"{supplier_f_name} {supplier_l_name}"
        self.suppliers[full_name] = {"supplier_first_name": supplier_f_name, "supplier_last_name": supplier_l_name}

    def add_supplier_details(self, supplier_address: str, supplier_email: str, supplier_telephone: str) -> None:
        full_address = f"{supplier_address}, {supplier_email}, {supplier_telephone}"
        self.suppliers[full_address] = {"supplier_address": supplier_address, "supplier_email": supplier_email, "telephone": supplier_telephone}

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
              "100 200 100")
s2 = Supplier("Grzegorz", "Gruszka", "Gruszkowa 5, 50-550 Gruszkowo", "gruszek@gmail.com",
              "605 605 605")

if __name__ == '__main__':
    print(s1.get_suppliers())
    s1.add_supplier_name("Basia", "Basiowska")
    print(s1.get_suppliers())
    s1.save_suppliers_to_file()
    s1.save_categories_to_file()
    print(str(s1))
