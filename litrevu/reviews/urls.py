import re
from django.urls import path

from . import views


app_name = "reviews"
urlpatterns = [
    path("feed/", views.FeedView.as_view(), name="feed"),
    path("ticket/new", views.NewTicketView.as_view(), name="new_ticket"),
    path(
        "ticket/update/<int:pk>",
        views.UpdateTicketView.as_view(),
        name="update_ticket",
    ),
    path(
        "review/new/<int:ticket_id>",
        views.NewTicketReviewView,
        name="new_ticket_review",
    ),
    path(
        "review/new/",
        views.NewReviewView.as_view(),
        name="new_review",
    ),
]
