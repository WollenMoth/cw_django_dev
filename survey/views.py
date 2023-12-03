import json

from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from survey.models import Answer, LikeDislike, Question


class QuestionListView(ListView):
    model = Question
    ordering = ['-ranking']


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
    body = json.loads(request.body)

    question_pk = body.get('question_pk')

    if not question_pk:
        return JsonResponse({'error': 'question_pk is required.'}, status=400)

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User must be authenticated.'}, status=401)

    value = body.get('value')

    if value is None:
        print('value is required.')
        return JsonResponse({'error': 'value is required.'}, status=400)

    if value not in range(6):
        print('value must be between 0 and 5.')
        return JsonResponse({'error': 'value must be between 0 and 5.'}, status=400)

    Answer.objects.update_or_create(
        question_id=question_pk, author_id=request.user.id,
        defaults={'value': value})

    return JsonResponse({'ok': True})

def like_dislike_question(request):
    body = json.loads(request.body)

    question_pk = body.get('question_pk')

    if not question_pk:
        return JsonResponse({'error': 'question_pk is required.'}, status=400)

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User must be authenticated.'}, status=401)

    action = body.get('action')

    if not action:
        return JsonResponse({'error': 'action is required.'}, status=400)

    like_dislike = LikeDislike.objects.get_or_create(
        question_id=question_pk, author_id=request.user.id)[0]

    if action == 'like':
        like_dislike.value = 1 if like_dislike.value != 1 else 0
    elif action == 'dislike':
        like_dislike.value = -1 if like_dislike.value != -1 else 0
    else:
        return JsonResponse({'error': 'Invalid action.'}, status=400)

    like_dislike.save()
    return JsonResponse({'ok': True})

