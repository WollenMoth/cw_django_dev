from django import template

register = template.Library()


@register.filter
def user_likes(question, user):
    return question.user_likes(user)


@register.filter
def user_dislikes(question, user):
    return question.user_dislikes(user)
