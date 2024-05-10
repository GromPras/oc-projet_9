from django.shortcuts import render
from django.views.generic import ListView

from .models import Review, Ticket


class FeedView(ListView):
    template_name = "reviews/index.html"
    context_object_name = "latest_review_list"

    def get_queryset(self):
        return Review.objects.all()
