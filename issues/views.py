from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from issues.database_updater import create_repository, update_repository, create_issue, update_issue
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


@login_required
def sync_repositories(request):
    current_user = request.user
    social_account = current_user.social_auth.get(provider='github')
    access_token = social_account.extra_data['access_token']

    response = GithubRequestsMaker(access_token).get_repositories()

    if response.status_code != 200:
        messages.warning(request, 'Error occured while updating repositories...')
        return redirect('/issues/repositories')

    repositories = response.json()
    existing_in_database_repos_ids = Repository.objects.filter(owner_login=current_user.username)\
        .values_list('github_id', flat=True)

    for repo in repositories:
        if repo['id'] not in existing_in_database_repos_ids:
            create_repository(repo)
        else:
            update_repository(repo)

    messages.success(request, 'Repos are up-to-date')
    return redirect('/issues/repositories')


@login_required
def sync_issues(request, pk):
    current_user = request.user
    social_account = current_user.social_auth.get(provider='github')
    access_token = social_account.extra_data['access_token']

    # get repo
    current_repo = Repository.objects.get(pk=pk)

    response = GithubRequestsMaker(access_token).get_issues(current_user, current_repo.github_name)
    if response.status_code != 200:
        messages.warning(request, 'Error occured while updating issues...')
        return redirect('/issues/repositories/' + pk)

    issues = response.json()
    existing_issues = list(map(lambda i: i.github_number, current_repo.issue_set.all()))

    for issue in issues:
        if issue['number'] not in existing_issues:
            create_issue(issue, current_repo)
        else:
            update_issue(issue, current_repo)

    closed_task = current_repo.issue_set.all().filter(github_state="closed")

    messages.success(request, 'Issues are up-to-date')
    return redirect('/issues/repositories/' + pk)


# generic views
class RepositoryListView(LoginRequiredMixin, generic.ListView):
    model = Repository
    ordering = ['-open_issues_count']

    def get_queryset(self):
        return Repository.objects.filter(owner_login=self.request.user.username)


class RepositoryView(LoginRequiredMixin, generic.DetailView):
    model = Repository



