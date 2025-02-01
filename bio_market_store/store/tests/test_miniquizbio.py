from django.test import TestCase
from .models import MiniQuizBio


class MiniQuizBioTests(TestCase):
    def test_create_quiz(self):
        """Test basic quiz creation and retrieval"""
        quiz = MiniQuizBio.objects.create(
            question="Co oznacza skrót BIO na produktach spożywczych?",
            answer_choices={
                'a': 'Biologiczne Innowacje Organizacyjne',
                'b': 'Biologicznie Izolowane Organizmy',
                'c': 'Biologicznie Intensywna Obserwacja',
                'd': 'Biologiczne'
            },
            correct_answer='d'
        )

        # Test that the quiz was created correctly
        self.assertEqual(quiz.question, "Co oznacza skrót BIO na produktach spożywczych?")
        self.assertEqual(quiz.correct_answer, 'd')

        # Test string representation
        self.assertEqual(str(quiz), "Co oznacza skrót BIO na produktach spożywczych?")