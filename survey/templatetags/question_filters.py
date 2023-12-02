from django import template

register = template.Library()


@register.filter
def user_likes(question, user):
    if not user.is_authenticated:
        return False
    return question.user_likes(user)


@register.filter
def user_dislikes(question, user):
    if not user.is_authenticated:
        return False
    return question.user_dislikes(user)
