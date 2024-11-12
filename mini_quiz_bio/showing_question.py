from mini_quiz_bio.list_of_question import list_of_questions

def showing_all():

    total_points = 0

    for question in list_of_questions:
        print(question.show_question())
        print(question.good_answer())
        total_points += question.add_points()
        print(f"Aktualna liczba punktów: {total_points}")
        print("".join(["-" for _ in range(40)]))

    print(f"Całkowita liczba punktów to {total_points}.")