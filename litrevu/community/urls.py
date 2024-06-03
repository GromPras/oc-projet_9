from django.urls import path

from . import views


app_name = "community"
urlpatterns = [
    path("search/", views.SearchUserView.as_view(), name="search"),
    path(
        "search/<str:username>", views.SearchUserView.as_view(), name="search"
    ),
    path(
        "subscribe/<int:user_id>",
        views.SubscribeView.as_view(),
        name="subscribe",
    ),
    path(
        "unsubscribe/<int:user_id>",
        views.UnSubscribeView.as_view(),
        name="unsubscribe",
    ),
    path(
        "block/<int:user_id>",
        views.BlockView.as_view(),
        name="block",
    ),
    path("unblock/<int:user_id>", views.UnBlockView.as_view(), name="unblock"),
]
