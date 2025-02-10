from django.test import TestCase
from store.models import MiniQuizBio
import json

class MiniQuizBioTests(TestCase):
    def test_create_quiz(self):
        quiz = MiniQuizBio.objects.create(
            question="What does BIO stand for?",
            answer_choices=json.dumps({
                'a': 'Biological Organisational Innovation',
                'b': 'Biologically isolated organism',
                'c': 'Biologically Intensive Observation',
                'd': 'Biological'
            }),
            correct_answer='d'
        )

        self.assertEqual(quiz.question, "What does BIO stand for?")
        self.assertEqual(quiz.correct_answer, 'd')
