from django.db import migrations
import json

def add_questions(apps, schema_editor):
    MiniQuizBio = apps.get_model("store", "MiniQuizBio")
    from store.mini_quiz_bio.list_of_question import list_of_question

    for item in list_of_question:
        MiniQuizBio.objects.create(
            question=item.question,
            answer_choices=json.dumps({
                "a": item.a, "b": item.b, "c": item.c, "d": item.d
            }),
            correct_answer=item.correct_answer
        )

class Migration(migrations.Migration):
    dependencies = [("store", "0001_initial")]
    operations = [migrations.RunPython(add_questions)]


