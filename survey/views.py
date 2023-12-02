import json

from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from survey.models import Answer, LikeDislike, Question


class QuestionListView(ListView):
    model = Question


class QuestionCreateView(CreateView):
    model = Question
    fields = ['title', 'description']
    redirect_url = ''

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)


class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['title', 'description']
    template_name = 'survey/question_form.html'


def answer_question(request):
    question_pk = request.POST.get('question_pk')
    print(request.POST)
    if not request.POST.get('question_pk'):
        return JsonResponse({'ok': False})
    question = Question.objects.filter(pk=question_pk)[0]
    answer = Answer.objects.get(question=question, author=request.user)
    answer.value = request.POST.get('value')
    answer.save()
    return JsonResponse({'ok': True})

def like_dislike_question(request):
    body = json.loads(request.body)

    question_pk = body.get('question_pk')
    author_id = request.user.id
    action = body.get('action')

    if not question_pk or not author_id or not action:
        return JsonResponse({'ok': False})

    like_dislike = LikeDislike.objects.get_or_create(
        question_id=question_pk, author_id=request.user.id)[0]

    if action == 'like':
        like_dislike.value = 1 if like_dislike.value != 1 else 0
    elif action == 'dislike':
        like_dislike.value = -1 if like_dislike.value != -1 else 0

    like_dislike.save()
    return JsonResponse({'ok': True})

