from django.http import Http404
from django.shortcuts import render

from restaurants.forms import CommentForm


def comment_create(request, pk):
    if request.method == "POST":
        form = request.POST.get('form')




