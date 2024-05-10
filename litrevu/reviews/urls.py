from django.urls import path

from . import views


app_name = "reviews"
urlpatterns = [
    path("feed/", views.FeedView.as_view(), name="feed"),
    path("ticket/new", views.NewTicketView.as_view(), name="new_ticket"),
]
