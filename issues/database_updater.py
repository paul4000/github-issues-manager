from issues.models import Repository, Issue


def create_repository(repo):

    Repository.objects.create(
        github_id=repo['id'],
        github_name=repo["name"],
        github_full_name=repo["full_name"],
        owner_login=repo["owner"]["login"],
        open_issues_count=repo["open_issues_count"]
    )


def update_repository(repo):
    repository = Repository.objects.get(github_id=repo['id'])
    repository.github_name = repo["name"]
    repository.github_full_name = repo["full_name"]
    repository.open_issues_count = repo["open_issues_count"]
    repository.save()


def create_issue(issue, repo):

    labels = ','.join(list(map(lambda labe: labe["name"], issue["labels"])))

    assignee_login = issue.get('assignee', {}).get('login')
    assignee_url = issue.get('assignee', {}).get('html_url')

    Issue.objects.create(
        repository=repo,
        github_number=issue["number"],
        github_html_url=issue["html_url"],
        github_state=issue["state"],
        github_title=issue["title"],
        github_body=issue["body"],
        label=labels,
        github_created_at=issue["created_at"],
        github_updated_at=issue["updated_at"],
        github_comments_number=issue["comments"],
        github_assignee_login=assignee_login,
        github_assignee_url_profile=assignee_url
    )


def update_issue(issue, repo):

    assignee_login = issue.get('assignee', {}).get('login')
    assignee_url = issue.get('assignee', {}).get('html_url')

    issue_old = Issue.objects.get(github_number=issue["number"], repository=repo)
    issue_old.github_state=issue["state"]
    issue_old.github_title=issue["title"]
    issue_old.github_body=issue["body"]
    issue_old.label = ','.join(list(map(lambda labe: labe["name"], issue["labels"])))
    issue_old.github_updated_at=issue["updated_at"]
    issue_old.github_comments_number=issue["comments"]
    issue_old.github_assignee_login=assignee_login
    issue_old.github_assignee_url_profile=assignee_url
    issue_old.save()

