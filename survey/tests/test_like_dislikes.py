import json

import pytest
from django.urls import reverse
from model_bakery import baker

from survey.models import LikeDislike, Question


@pytest.fixture
def like_dislike_question(client):
    return lambda like_dislike: client.post(
        reverse('survey:question-like'),
        data=json.dumps(like_dislike),
        content_type='application/json',
    )


@pytest.mark.django_db
class TestLikeDislikeQuestionView:
    def test_if_user_is_anonymous_returns_401(self, like_dislike_question):
        question = baker.make(Question)

        response = like_dislike_question({
            'question_pk': question.pk,
            'value': 1
        })

        assert response.status_code == 401
        assert response.json()['error'] is not None
        assert LikeDislike.objects.count() == 0

    def test_if_question_pk_is_missing_returns_400(self, authenticate, like_dislike_question):
        response = like_dislike_question({'value': 1})

        assert response.status_code == 400
        assert response.json()['error'] is not None
        assert LikeDislike.objects.count() == 0

    def test_if_value_is_missing_returns_400(self, authenticate, like_dislike_question):
        question = baker.make(Question)

        response = like_dislike_question({'question_pk': question.pk})

        assert response.status_code == 400
        assert response.json()['error'] is not None
        assert LikeDislike.objects.count() == 0

    def test_if_value_is_invalid_returns_400(self, authenticate, like_dislike_question):
        question = baker.make(Question)

        response = like_dislike_question({
            'question_pk': question.pk,
            'value': 2
        })

        assert response.status_code == 400
        assert response.json()['error'] is not None
        assert LikeDislike.objects.count() == 0

    def test_if_data_is_valid_returns_200(self, authenticate, like_dislike_question):
        question = baker.make(Question)

        response = like_dislike_question({
            'question_pk': question.pk,
            'value': 1
        })

        assert response.status_code == 200
        assert LikeDislike.objects.count() == 1
        assert LikeDislike.objects.get(question=question).value == 1
