class MakingQuestionAnswer:
    def __init__(self, question: str, a: str, b: str, c: str, d: str, correct_answer: str):
        self.question = question
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.correct_answer = correct_answer
        self.choice = None

    def show_question(self):
        return f"{self.question}\n a. {self.a} \n b. {self.b} \n c. {self.c} \n d. {self.d}"

    def good_answer(self):
        while True:
            self.choice = input("Podaj swoją odpowiedź:").strip().lower()
            if self.choice in ("a", "b", "c", "d"):
                if self.choice == self.correct_answer:
                    return "Podałeś poprawną odpowiedź."
                else:
                    return f"Podałeś zła odpowiedź. Poprawna odpowiedź to {self.correct_answer}."
            elif self.choice == "q":
                return "Powrót do menu"
            else:
                print("Podałeś prawdopodobnie zła opcje do wyboru. Spróbuj jeszcze raz :)")

    def add_points(self):
        if self.choice == self.correct_answer:
            return 5
        else:
            return 0

