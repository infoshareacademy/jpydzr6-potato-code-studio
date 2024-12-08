from cart import Cart

class Mod_loyalty(Cart):

    __slots__ = "loyalty_points"

    def __init__(self, products):
        # Dziedziczenie:
        super().__init__(products)
        # Atrybuty obecnej klasy:
        self.loyalty_points = 0
        self.old_instance = Cart(products).show_cart()
        self.new_instance = None

    def add_points(self, amount_pln: int):
        if amount_pln < 0:
            raise ValueError("Amount must be 0 or higher")
        points_earned = amount_pln * 5
        self.loyalty_points += points_earned

    def get_points(self) -> int:
        return self.loyalty_points

    def show_cart_summary_with_pts(self) -> str:
        return f"{self.old_instance}, Your Loyalty Points: {self.loyalty_points}"


### TESTING ###
if __name__ == '__main__':
    loyalty_program = Mod_loyalty(products=[])
    loyalty_program.add_points(10)  # EXAMPLE # Your Loyalty Points for 10 PLN
    print(f"Loyalty Points: {loyalty_program.get_points()}")  # Result (Profit)
