import json

class User:

    __slots__ =("f_name", "l_name", "address", "email", "telephone", "loyalty_points", "order_history", "customers")

    def __init__(self, f_name: str, l_name: str, address: str, email: str, telephone: str,
                 loyalty_points: int):
        self.f_name = f_name
        self.l_name = l_name
        self.address = address
        self.email = email
        self.telephone = telephone
        self.loyalty_points = loyalty_points
        self.order_history = {}
        self.customers = {}

    def add_customer_name(self, f_name: str, l_name: str) -> None:
        full_name = f"{f_name} {l_name}"
        self.customers[full_name] = {"first_name": f_name, "last_name": l_name}

    def add_customer_details(self, address: str, email: str, telephone: str) -> None:
        full_address = f"{address}, {email}, {telephone}"
        self.customers[full_address] = {"customer_address": address, "email": email, "telephone": telephone}

    def get_customers(self) -> dict:
        return self.customers

    def history(self, order, order_history) -> dict:
        if order in order_history:
            return self.order_history
        else:
            print("You don't have any orders yet.")

    def save_to_file(self) -> None:
        record = self.customers, self.loyalty_points
        with open("customer_details.json", mode="w", encoding="UTF-8") as file:
            json.dump(record, file)


### TESTING ###
u1 = User("Adam", "Kowalski", "Kowalska 4, 80-200 Opole", "acme@gmail.com",
          "500 100 400", 20)
u2 = User("Jacek", "Jackowski", "Morska 1, 35-120 Szczecin", "jaca@interia.pl",
          "605 600 700", 50)

# if __name__ == '__main__':
#     print(u1.get_customers())
#     u1.add_customer_name("Marek", "Markowski")
#     print(u1.get_customers())
#     u1.add_customer_details("Lotnicza 1, 77-600 Gdynia", "bla@wp.pl", "503 503 503")
#     print(u1.get_customers())
#     u1.save_to_file()
