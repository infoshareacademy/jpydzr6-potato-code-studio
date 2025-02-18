from bio_market_store.store.mini_quiz_bio.list_of_question import list_of_questions

def quiz_bio():

    total_points = 0

    for question in list_of_questions:
        print(question.show_question())
        print("Jeżeli chcesz zakończyć Quiz wpisz 'q'.")

        result = question.good_answer()
        if result == "Powrót do menu":
            print("".join(["-" for _ in range(40)]))
            print(f"Całkowita liczba punktów to {total_points}.")
            break

        print(result)
        total_points += question.add_points()
        print(f"Aktualna liczba punktów: {total_points}")
        print(f"Całkowita liczba punktów to {total_points}.\n")
        print("".join(["-" for _ in range(40)]))