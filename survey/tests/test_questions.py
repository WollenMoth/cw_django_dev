import pytest
from django.urls import reverse
from model_bakery import baker


@pytest.fixture
def get_questions(client):
    return lambda: client.get(reverse('survey:question-list'))


@pytest.mark.django_db
class TestQuestionListView:
    def test_if_question_list_is_sorted(self, get_questions):
        questions = baker.make('Question', _quantity=5)

        for idx, question in enumerate(questions):
            baker.make('Answer', question=question, value=idx)
            baker.make('LikeDislike', question=question, value=idx % 3 - 1)

        response = get_questions()

        questions = response.context['object_list']
        rankings = [question.ranking for question in questions]

        assert rankings, sorted(rankings, reverse=True)
