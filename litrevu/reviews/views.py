from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from authentication.models import User

from .models import Review, Ticket
from .forms import NewTicketForm


class FeedView(ListView):
    template_name = "reviews/index.html"
    context_object_name = "review_list"

    def get_queryset(self):
        return Ticket.objects.all()


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
