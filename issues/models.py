from datetime import datetime

import pytz
from django.db import models


class Repository(models.Model):
    """
    Model representing Github API Repository object.
    """

    github_id = models.IntegerField()
    github_name = models.TextField()
    github_full_name = models.TextField()
    open_issues_count = models.IntegerField()
    owner_login = models.TextField()

    def __str__(self):
        return self.github_name


class Issue(models.Model):
    """
    Model representing Github API Issue object, with added custom for application fields: priority and deadline.
    """

    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)

    PRIORITY_CHOICES = (
        (1, '1 - HIGH'),
        (2, '2 - MEDIUM'),
        (3, '3 - LOW')
    )

    github_number = models.IntegerField()
    github_html_url = models.TextField()
    github_state = models.TextField()
    github_title = models.TextField()
    github_body = models.TextField()
    label = models.TextField()
    github_created_at = models.DateTimeField()
    github_updated_at = models.DateTimeField()
    github_comments_number = models.IntegerField()
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=3
    )
    deadline = models.DateTimeField(null=True, blank=True)
    github_assignee_login = models.TextField()
    github_assignee_url_profile = models.TextField()

    def is_out_of_date(self):

        utc = pytz.UTC

        return self.deadline and (utc.localize(datetime.now()) > self.deadline)

    def __str__(self):
        return str(self.github_number) + ' ' + self.github_title
