from django import template

register = template.Library()

@register.filter
def has_voted(user, question):
    return question.choices.filter(answers__user=user.pk).exists()