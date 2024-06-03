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
        "review/new/",
        views.NewTicketReviewView.as_view(),
        name="new_ticket_review",
    ),
    path(
        "review/update/<int:pk>",
        views.UpdateTicketReviewView.as_view(),
        name="update_review",
    ),
    path(
        "review/new/<int:ticket_id>",
        views.NewTicketReviewView.as_view(),
        name="new_ticket_review",
    ),
    path("posts/", views.PostsView.as_view(), name="posts"),
    path(
        "review/delete/<int:pk>",
        views.DeleteReviewView.as_view(),
        name="delete_review",
    ),
    path(
        "ticket/delete/<int:pk>",
        views.DeleteTicketView.as_view(),
        name="delete_ticket",
    ),
]
