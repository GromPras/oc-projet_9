from itertools import chain
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from authentication.models import User
from community.models import UserFollows

from .models import Review, Ticket
from .forms import NewTicketForm, NewReviewForm


class FeedView(LoginRequiredMixin, ListView):
    template_name = "reviews/index.html"
    context_object_name = "feed"

    def get_queryset(self):
        """
        Retrieves the queryset for the current view.

        Returns:
            list: The queryset containing the tickets and reviews to be displayed in the feed.The queryset is sorted by time created in descending order. The queryset is filtered by ther current users followed users and the users that created a review on the the current user's tickets.

        Raises:
            None
        """
        current_user = self.request.user
        followed_users = UserFollows.objects.filter(
            user__id=current_user.id
        ).values("followed_user__id")
        ticket_list = Ticket.objects.filter(
            Q(user__id__in=[followed_users]) | Q(user=current_user)
        ).order_by("time_created")
        reviews_list = Review.objects.filter(
            Q(user__id__in=[followed_users]) | Q(user=current_user)
        ).order_by("time_created") | Review.objects.filter(
            ticket__user=current_user.id
        ).order_by(
            "time_created"
        )
        for r in reviews_list:
            if r.user.id == current_user.id:
                for ticket in ticket_list:
                    if ticket.id == r.ticket.id:
                        ticket.responded = True
                    if ticket.image is None:
                        ticket.image.url = "ticket_placeholder.webp"

        feed = sorted(
            chain(ticket_list, reviews_list),
            key=lambda i: i.time_created,
            reverse=True,
        )
        return feed

    def get_context_data(self, **kwargs):
        """Add the authenticated user to the context."""
        context = super(FeedView, self).get_context_data(**kwargs)
        current_user = User.objects.get(pk=self.request.user.id)
        context["current_user"] = current_user
        return context


class PostsView(LoginRequiredMixin, ListView):
    template_name = "reviews/index.html"
    context_object_name = "feed"

    def get_queryset(self):
        """
        Retrieves the queryset for the current view.

        Returns:
            list: The queryset containing the tickets and reviews to be displayed in the feed. The queryset is sorted by time created in descending order. The queryset is filtered by the current user's tickets and reviews.

        Raises:
            None
        """
        current_user = self.request.user
        ticket_list = Ticket.objects.filter(user=current_user).order_by(
            "time_created"
        )
        reviews_list = Review.objects.filter(user=current_user).order_by(
            "time_created"
        )
        for r in reviews_list:
            if r.user.id == current_user.id:
                for ticket in ticket_list:
                    if ticket.id == r.ticket.id:
                        ticket.responded = True
                    if ticket.image is None:
                        ticket.image.url = "ticket_placeholder.webp"

        feed = sorted(
            chain(ticket_list, reviews_list),
            key=lambda i: i.time_created,
            reverse=True,
        )

        return feed

    def get_context_data(self, **kwargs):
        """Add the authenticated user to the context."""
        context = super(PostsView, self).get_context_data(**kwargs)
        current_user = User.objects.get(pk=self.request.user.id)
        context["current_user"] = current_user
        context["posts"] = True
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


class UpdateTicketView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ticket
    form_class = NewTicketForm
    template_name = "reviews/ticket_update_form.html"
    success_url = reverse_lazy("reviews:feed")

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update"] = True
        return context


class NewTicketReviewView(LoginRequiredMixin, View):
    review_model = Review
    ticket = None

    def get(self, request, *args, **kwargs):
        """
        Retrieves a ticket and its associated forms for review.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The rendered HTML response containing the review update form.

        Raises:
            ObjectDoesNotExist: If the ticket with the specified ID does not exist.

        Description:
           This function is the GET handler for the NewTicketReviewView class. It retrieves a ticket and its associated forms for review. If a ticket ID is provided in the URL parameters, it retrieves the ticket from the database using the provided ID. If no ticket ID is provided, it initializes the review form and ticket form with default values.
        """
        if self.kwargs.get("ticket_id"):
            self.ticket = Ticket.objects.get(pk=self.kwargs.get("ticket_id"))
        review_form = None
        ticket_form = None
        if self.ticket is not None:
            review_form = NewReviewForm(initial={"ticket": self.ticket})
        else:
            review_form = NewReviewForm()
            ticket_form = NewTicketForm()
        template_name = "reviews/review_update_form.html"
        success_url = reverse_lazy("reviews:feed")

        return render(
            request,
            "reviews/review_update_form.html",
            {
                "review_form": review_form,
                "ticket": self.ticket,
                "ticket_form": ticket_form,
            },
        )

    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request for creating a new ticket and review.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponseRedirect: Redirects to the "reviews:feed" URL if the ticket and review are successfully created.

        Raises:
            None

        Description:
            This function is responsible for handling the HTTP POST request for creating a new ticket and review. It checks if a ticket ID is provided in the URL parameters. If so, it retrieves the corresponding ticket from the database.
            If not, it creates a new instance of the NewTicketForm with the request data and files. If the form is valid, it saves the ticket, sets the user ID, and saves it to the database.

            After that, it creates a new instance of the NewReviewForm with the request data. If the form is valid, it saves the review, sets the ticket ID and user ID, and saves it to the database.

            Finally, it redirects the user to the "reviews:feed" URL.

        """
        request_user = self.request.user
        if self.kwargs.get("ticket_id"):
            self.ticket = Ticket.objects.get(pk=self.kwargs.get("ticket_id"))
        else:
            ticket_form = NewTicketForm(
                request.POST,
                request.FILES,
            )
            if ticket_form.is_valid():
                self.ticket = ticket_form.save(commit=False)
                self.ticket.user_id = request_user.id
                self.ticket.save()

        review_form = NewReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket_id = self.ticket.id
            review.user_id = request_user.id
            review.save()
            return HttpResponseRedirect(reverse_lazy("reviews:feed"))


class UpdateTicketReviewView(
    LoginRequiredMixin, UserPassesTestMixin, UpdateView
):
    model = Review
    form_class = NewReviewForm
    context_object_name = "review_form"
    template_name = "reviews/review_update_form.html"
    success_url = reverse_lazy("reviews:feed")

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket"] = self.object.ticket
        context["review_form"] = context.pop("form")
        context["update"] = True
        return context


class DeleteTicketView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    success_url = reverse_lazy("reviews:posts")

    def test_func(self):
        return self.get_object().user == self.request.user


class DeleteReviewView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    success_url = reverse_lazy("reviews:posts")

    def test_func(self):
        return self.get_object().user == self.request.user
