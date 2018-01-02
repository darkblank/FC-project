from django import forms

from restaurants.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['star_rate', 'comment']
        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                }
            )
        }
