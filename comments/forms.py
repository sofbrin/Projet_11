from django.forms.utils import ErrorList
from django import forms
from .models import CommentsDb


class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="error">%s</p>' % e for e in self])


class CommentsForm(forms.ModelForm):
    class Meta:
        model = CommentsDb
        fields = ('text')
