from list_of_question import list_of_question
def showing_question():

    total_points = 0

    for question in list_of_question:
        print(question.show_question())
        print(question.good_answer())
        total_points += question.add_points()
        print(f"Aktualna liczba punktów: {total_points}")
        print("".join(["-" for _ in range(40)]))

    print(f"Całkowita liczba punktów to {total_points}.")
