from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from .forms import SearchUsersForm
from .models import UserFollows

from authentication.models import User


class SearchUserView(LoginRequiredMixin, View):
    results = None
    searched = False
    search_form = SearchUsersForm()
    template_name = "community/search_users_form.html"
    followed_users = []
    followed_by = []

    def get(self, request, *args, **kwargs):
        username = self.request.GET.get("username")
        current_user = self.request.user
        self.followed_users = UserFollows.objects.filter(
            user__id=current_user.id
        )
        self.followed_users = [f.followed_user for f in self.followed_users]
        self.followed_by = UserFollows.objects.filter(
            followed_user__id=current_user.id
        )
        self.followed_by = [
            {"user": f.user, "followed": f.user in self.followed_users}
            for f in self.followed_by
        ]

        if username:
            self.searched = True
            self.results = []
            query_results = User.objects.filter(username__contains=username)
            for i in query_results:
                if i.username != current_user.username:
                    self.results.append(
                        {
                            "user": {"username": i.username, "id": i.id},
                            "followed": i in self.followed_users,
                        }
                    )

        return render(
            request,
            "community/search_users_form.html",
            {
                "search_form": self.search_form,
                "results": self.results,
                "searched": self.searched,
                "followed_users": self.followed_users,
                "followed_by": self.followed_by,
            },
        )


class SubscribeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        subscribe_to = User.objects.get(pk=kwargs.get("user_id"))
        if subscribe_to and subscribe_to != request.user:
            new_userfollow = UserFollows(
                user=request.user, followed_user=subscribe_to
            )
            new_userfollow.save()
        return HttpResponseRedirect(reverse_lazy("community:search"))


class UnSubscribeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        unsubscribe_from = User.objects.get(pk=kwargs.get("user_id"))
        current_user = self.request.user
        subscription = UserFollows.objects.get(
            user__id=current_user.id, followed_user__id=unsubscribe_from.id
        )
        subscription.delete()
        return HttpResponseRedirect(reverse_lazy("community:search"))
