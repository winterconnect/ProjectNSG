from .models import Member, Comment, Board
from django import forms


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('memberID', 'content',)