from itertools import chain
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from authentication.models import User

from .models import Review, Ticket
from .forms import NewTicketForm


class FeedView(ListView):
    template_name = "reviews/index.html"
    context_object_name = "feed"

    def get_queryset(self):
        # TODO: filter by user followed
        current_user = User.objects.get(pk=self.request.user.id)
        ticket_list = Ticket.objects.all().order_by("time_created")
        reviews_list = Review.objects.filter(user=current_user).order_by(
            "time_created"
        ) | Review.objects.filter(ticket__user=current_user).order_by(
            "time_created"
        )
        feed = sorted(
            chain(ticket_list, reviews_list),
            key=lambda i: i.time_created,
            reverse=True,
        )
        return feed


class NewTicketView(CreateView):
    model = Ticket
    form_class = NewTicketForm
    template_name = "reviews/new_ticket.html"
    success_url = reverse_lazy("reviews:feed")

    def form_valid(self, form):
        ticket = form.save(commit=False)
        request_user = self.request.user
        current_user = User.objects.get(id=request_user.id)
        print(current_user)
        ticket.user = current_user
        ticket.save()
        return HttpResponseRedirect(self.success_url)
