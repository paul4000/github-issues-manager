from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from issues.github_api_request_maker import GithubRequestsMaker
from issues.models import Repository


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@login_required
def homepage(request):
    return render(request, 'issues/homepage.html')


def logout(request):
    auth_logout(request)
    return redirect('/login')


def sync_repositories(request):
    current_user = request.user
    social_account = current_user.social_auth.get(provider='github')
    access_token = social_account.extra_data['access_token']

    response = GithubRequestsMaker(access_token).get_repositories()

    if response.status_code != 200:
        messages.warning(request, 'Error occured while updating repositories...')
        return render(request, RepositoryListView.as_view())

    repositories = response.json()
    existing_in_database_repos_ids = Repository.objects.filter(owner_login=current_user.username)\
        .values_list('github_id', flat=True)

    for repo in repositories:
        if repo['id'] not in existing_in_database_repos_ids:
            Repository.objects.create(
                github_id=repo['id'],
                github_name=repo["name"],
                github_full_name=repo["full_name"],
                owner_login=repo["owner"]["login"],
                open_issues_count=repo["open_issues_count"]
            )

    messages.success(request, 'Repos are up-to-date')
    return render(request, RepositoryListView.as_view())


class RepositoryListView(LoginRequiredMixin, generic.ListView):
    model = Repository




