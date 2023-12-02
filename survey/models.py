from datetime import date

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Question(models.Model):
    created = models.DateField('Creada', auto_now_add=True)
    author = models.ForeignKey(get_user_model(), related_name="questions", verbose_name='Pregunta',
                               on_delete=models.CASCADE)
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descripción')
    likes = models.IntegerField('Likes', default=0)
    dislikes = models.IntegerField('Dislikes', default=0)

    @property
    def ranking(self):
        bonus = 10 if self.created == date.today() else 0
        return self.answers.count() * 10 + self.likes * 5 - self.dislikes * 3 + bonus

    def get_absolute_url(self):
        return reverse('survey:question-edit', args=[self.pk])


class Answer(models.Model):
    ANSWERS_VALUES = ((0,'Sin Responder'),
                      (1,'Muy Bajo'),
                      (2,'Bajo'),
                      (3,'Regular'),
                      (4,'Alto'),
                      (5,'Muy Alto'),)

    question = models.ForeignKey(Question, related_name="answers", verbose_name='Pregunta', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), related_name="answers", verbose_name='Autor', on_delete=models.CASCADE)
    value = models.PositiveIntegerField("Respuesta", default=0)
    comment = models.TextField("Comentario", default="", blank=True)
