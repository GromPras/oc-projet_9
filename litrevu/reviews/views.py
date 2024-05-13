from itertools import chain
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from authentication.models import User

from .models import Review, Ticket
from .forms import NewTicketForm, NewReviewForm, NewTicketReviewFormSet


class FeedView(LoginRequiredMixin, ListView):
    template_name = "reviews/index.html"
    context_object_name = "feed"

    def get_queryset(self):
        # TODO: filter by user followed
        current_user = self.request.user
        ticket_list = Ticket.objects.all().order_by("time_created")
        reviews_list = Review.objects.filter(user=current_user.id).order_by(
            "time_created"
        ) | Review.objects.filter(ticket__user=current_user.id).order_by(
            "time_created"
        )
        for r in reviews_list:
            if r.user.id == current_user.id:
                for ticket in ticket_list:
                    if ticket.id == r.ticket.id:
                        ticket.responded = True

        feed = sorted(
            chain(ticket_list, reviews_list),
            key=lambda i: i.time_created,
            reverse=True,
        )
        return feed

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(FeedView, self).get_context_data(**kwargs)
        current_user = User.objects.get(pk=self.request.user.id)
        # Create any data and add it to the context
        context["current_user"] = current_user
        return context


class NewTicketView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = NewTicketForm
    template_name = "reviews/ticket_update_form.html"
    success_url = reverse_lazy("reviews:feed")

    def form_valid(self, form):
        ticket = form.save(commit=False)
        request_user = self.request.user
        ticket.user_id = request_user.id
        ticket.save()
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            print(self.request.FILES)
        return context


class UpdateTicketView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = NewTicketForm
    template_name = "reviews/ticket_update_form.html"
    success_url = reverse_lazy("reviews:feed")


class NewReviewView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = NewTicketForm
    template_name = "reviews/review_update_form.html"
    success_url = reverse_lazy("reviews:feed")

    pass


@login_required(login_url="authentication/signin")
def NewTicketReviewView(request, ticket_id=None):
    model = Review
    ticket = Ticket.objects.get(pk=ticket_id)
    if ticket is not None:
        form_class = NewReviewForm(initial={"ticket": ticket})
    else:
        form_class = NewReviewForm()
    template_name = "reviews/review_update_form.html"
    success_url = reverse_lazy("reviews:feed")

    if request.method == "POST":
        form = NewReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket_id = ticket.id
            request_user = request.user
            review.user_id = request_user.id
            form.save()
            return HttpResponseRedirect(reverse_lazy("reviews:feed"))

    return render(
        request,
        "reviews/review_update_form.html",
        {"form": NewReviewForm(initial={"ticket": ticket}), "ticket": ticket},
    )
