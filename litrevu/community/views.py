from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import View
from .forms import SearchUsersForm
from .models import UserFollows, UserBlocks

from authentication.models import User


class SearchUserView(LoginRequiredMixin, View):
    results = None
    searched = False
    search_form = SearchUsersForm()
    template_name = "community/search_users_form.html"
    followed_users = []
    followed_by = []
    blocked_users = []

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
        self.blocked_users = [
            b.blocked_user
            for b in UserBlocks.objects.filter(user__id=current_user.id)
        ]

        if username:
            self.searched = True
            self.results = []
            query_results = User.objects.filter(username__contains=username)
            for i in query_results:
                if (
                    i.username != current_user.username
                    and i not in self.blocked_users
                ):
                    if not UserBlocks.objects.filter(
                        user=i, blocked_user=current_user
                    ):
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
                "blocked_users": self.blocked_users,
            },
        )


class SubscribeView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        subscribe_to = User.objects.get(pk=self.kwargs.get("user_id"))
        if subscribe_to and subscribe_to != self.request.user:
            return True
        return False

    def get(self, request, *args, **kwargs):
        subscribe_to = User.objects.get(pk=kwargs.get("user_id"))
        new_userfollow = UserFollows(
            user=request.user, followed_user=subscribe_to
        )
        new_userfollow.save()
        return HttpResponseRedirect(reverse_lazy("community:search"))


class UnSubscribeView(LoginRequiredMixin, UserPassesTestMixin, View):
    unsubscribe_from = None
    subscription = None

    def test_func(self):
        self.unsubscribe_from = User.objects.get(pk=self.kwargs.get("user_id"))
        if (
            self.unsubscribe_from
            and self.unsubscribe_from != self.request.user
        ):
            self.subscription = UserFollows.objects.get(
                user__id=self.request.user.id,
                followed_user__id=self.unsubscribe_from.id,
            )
            if self.subscription.user == self.request.user:
                return True
        return False

    def get(self, request, *args, **kwargs):
        self.subscription.delete()
        return HttpResponseRedirect(reverse_lazy("community:search"))


class BlockView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        block_user = User.objects.get(pk=self.kwargs.get("user_id"))
        if block_user and block_user != self.request.user:
            return True
        return False

    def get(self, request, *args, **kwargs):
        block_user = User.objects.get(pk=self.kwargs.get("user_id"))
        new_userblock = UserBlocks(user=request.user, blocked_user=block_user)
        new_userblock.save()
        try:
            previous_subscription = UserFollows.objects.get(
                user=block_user,
                followed_user=request.user,
            )
            if previous_subscription:
                previous_subscription.delete()
        except UserFollows.DoesNotExist:
            pass
        return HttpResponseRedirect(reverse_lazy("community:search"))


class UnBlockView(LoginRequiredMixin, UserPassesTestMixin, View):
    unblock_user = None
    block = None

    def test_func(self):
        unblock_user = User.objects.get(pk=self.kwargs.get("user_id"))
        if unblock_user and unblock_user != self.request.user:
            self.block = UserBlocks.objects.get(
                user__id=self.request.user.id,
                blocked_user__id=unblock_user.id,
            )
            if self.block.user == self.request.user:
                return True
        return False

    def get(self, request, *args, **kwargs):
        self.block.delete()
        return HttpResponseRedirect(reverse_lazy("community:search"))
