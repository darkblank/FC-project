from django.http import Http404
from django.shortcuts import get_object_or_404, render

from restaurants.forms import CommentForm
from restaurants.models import Comment


def comment_update_view(request, comment_pk):
    if request.mehtod == "GET":
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user != comment.author:
            raise Http404
        ctx = {
            'comment': comment,
            'form': CommentForm(instance=comment),
        }
        return render(request, 'restaurant/comment_update.html', ctx)
