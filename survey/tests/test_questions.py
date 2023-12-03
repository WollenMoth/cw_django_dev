import pytest
from django.urls import reverse
from model_bakery import baker

from survey.models import Question


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


@pytest.mark.django_db
class TestQuestionModel:
    def test_if_user_likes_returns_true(self, user):
        question = baker.make('Question')

        baker.make('LikeDislike', question=question, author=user, value=1)

        assert question.user_likes(user)

    def test_if_user_not_likes_returns_false(self, user):
        question = baker.make('Question')

        assert not question.user_likes(user)

    def test_if_user_dislikes_returns_true(self, user):
        question = baker.make('Question')

        baker.make('LikeDislike', question=question, author=user, value=-1)

        assert question.user_dislikes(user)

    def test_if_user_not_dislikes_returns_false(self, user):
        question = baker.make('Question')

        assert not question.user_dislikes(user)

    def test_if_user_value_returns_value(self, user):
        question = baker.make('Question')

        baker.make('Answer', question=question, author=user, value=3)

        assert question.user_value(user) == 3

    def test_if_not_user_value_returns_none(self, user):
        question = baker.make('Question')

        assert question.user_value(user) is None

    def test_if_get_absolute_url_returns_url(self):
        question = baker.make('Question')

        assert question.get_absolute_url() == reverse(
            'survey:question-edit', args=[question.pk])

    def test_if_likes_is_counted(self):
        question = baker.make('Question')

        baker.make('LikeDislike', question=question, value=1, _quantity=3)

        assert Question.objects.get(pk=question.pk).likes == 3

    def test_if_dislikes_is_counted(self):
        question = baker.make('Question')

        baker.make('LikeDislike', question=question, value=-1, _quantity=3)

        assert Question.objects.get(pk=question.pk).dislikes == 3

    def test_if_ranking_is_calculated(self):
        question = baker.make('Question')

        baker.make('Answer', question=question, value=3, _quantity=2)
        baker.make('LikeDislike', question=question, value=1, _quantity=3)
        baker.make('LikeDislike', question=question, value=-1, _quantity=2)

        # 2 * 10 + 3 * 5 - 2 * 3 + 10 = 39
        assert Question.objects.get(pk=question.pk).ranking == 39
