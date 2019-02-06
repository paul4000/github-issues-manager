from django.contrib.admin.widgets import AdminSplitDateTime
from django.forms import modelform_factory, SelectDateWidget
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from issues.database_updater import create_repository, update_repository, create_issue, update_issue
from issues.github_api_request_maker import GithubRequestsMaker
from issues.models import Repository, Issue


def index(request):
    return HttpResponse("Hello, world. You're in Github app.")


@login_required
def homepage(request):
    return render(request, 'issues/homepage.html')


def logout(request):
    auth_logout(request)
    return redirect('/login')


@login_required
def sync_repositories(request):
    """
    Displays refreshed list of user's repositories.
    Compares local list of repositories with repositories on Github. If necessary updates
    this in database.

    :param request:
    :return: redirect for /issues/repositories
    """
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
    """
    Displays refreshed list of user's issues connected with repository.
    Compares local list of issues with issues on Github. If necessary updates
    this in database.

    :param request:
    :param pk: repository database id
    :return: redirect for /issues/repositories/:repo_id
    """

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
        if issue['number'] not in existing_issues and issue['state'] != 'closed':
            create_issue(issue, current_repo)
        else:
            if issue['number'] in existing_issues:
                update_issue(issue, current_repo)

    closed_task = current_repo.issue_set.all().filter(github_state="closed")

    for close_task in closed_task:
        messages.warning(request, 'Issue '+ close_task.github_html_url + ' was closed meanwhile')
        close_task.delete()

    messages.success(request, 'Issues are up-to-date')
    return redirect('/issues/repositories/' + pk)


@login_required
def close_issue(request, pk):
    """
    Displays issues list after deleting chosen issue. In case of error
    displays warning.
    :param request:
    :param pk: issue databse id
    :return: redirect to /issues/repositories/:repo_id
    """

    current_user = request.user
    social_account = current_user.social_auth.get(provider='github')
    access_token = social_account.extra_data['access_token']

    issue = Issue.objects.get(pk=pk)
    repository = issue.repository
    r = GithubRequestsMaker(access_token).close_issue(current_user.username, repository.github_name, issue.github_number)

    if r.status_code != 200:
        messages.warning(request, 'Error occured while closing issues...')
        return redirect('/issues/repositories/' + str(repository.pk))

    messages.warning(request, 'Issue ' + issue.github_html_url + ' was closed')
    issue.delete()

    return redirect('/issues/repositories/' + str(repository.pk))


# generic views
class RepositoryListView(LoginRequiredMixin, generic.ListView):
    model = Repository
    ordering = ['-open_issues_count']

    def get_queryset(self):
        """ Repositories only for currently logged user """
        return Repository.objects.filter(owner_login=self.request.user.username)


class RepositoryView(LoginRequiredMixin, generic.DetailView):
    model = Repository


class ModelFormWidgetMixin(object):
    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields, widgets=self.widgets)


class IssueUpdateView(ModelFormWidgetMixin, generic.UpdateView):
    model = Issue
    fields = ('priority', 'deadline', )
    template_name = 'issues/edit_issue.html'
    pk_url_kwarg = 'issue_pk'
    context_object_name = 'issue'
    widgets = {
        'deadline' : SelectDateWidget,
    }

    def form_valid(self, form):
        issue = form.save(commit=False)
        issue.save()
        return redirect('issues:repositories_issues', pk=issue.repository.pk)
