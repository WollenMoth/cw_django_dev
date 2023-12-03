import json

import pytest
from django.urls import reverse
from model_bakery import baker

from survey.models import Answer, Question


@pytest.fixture
def answer_question(client):
    return lambda answer: client.post(
        reverse('survey:question-answer'), data=json.dumps(answer), content_type='application/json')


@pytest.mark.django_db
class TestAnswerQuestionView:
    def test_if_user_is_anonymous_returns_401(self, answer_question):
        question = baker.make(Question)

        response = answer_question({'question_pk': question.pk, 'value': 3})

        assert response.status_code == 401
        assert response.json()['error'] is not None
        assert Answer.objects.count() == 0

    def test_if_question_pk_is_missing_returns_400(self, authenticate, answer_question):
        response = answer_question({'value': 3})

        assert response.status_code == 400
        assert response.json()['error'] is not None
        assert Answer.objects.count() == 0

    def test_if_value_is_missing_returns_400(self, authenticate, answer_question):
        question = baker.make(Question)

        response = answer_question({'question_pk': question.pk})

        assert response.status_code == 400
        assert response.json()['error'] is not None
        assert Answer.objects.count() == 0

    def test_if_value_is_invalid_returns_400(self, authenticate, answer_question):
        question = baker.make(Question)

        response = answer_question({'question_pk': question.pk, 'value': 6})

        assert response.status_code == 400
        assert response.json()['error'] is not None
        assert Answer.objects.count() == 0

    def test_if_data_is_valid_returns_200(self, authenticate, answer_question):
        question = baker.make(Question)

        response = answer_question({'question_pk': question.pk, 'value': 3})

        assert response.status_code == 200
        assert Answer.objects.count() == 1
        assert Answer.objects.get(question=question).value == 3
