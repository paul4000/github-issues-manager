from datetime import timedelta
from datetime import datetime
from django.test import TestCase

from issues.models import Issue, Repository


class IssueTestCase(TestCase):
    """
        Class testing methods from Issue models.
    """

    def setUp(self):
        deadline_1 = datetime.now() + timedelta(days=5)
        deadline_2 = datetime.now() - timedelta(days=2)

        r = Repository.objects.create(github_id=0,
                                      github_name='',
                                      github_full_name='',
                                      owner_login='',
                                      open_issues_count=0)
        Issue.objects.create(
            repository=r,
            github_number=0,
            github_html_url='',
            github_state='',
            github_title='Issue',
            github_body='',
            label='',
            github_created_at=datetime.now(),
            github_updated_at=datetime.now(),
            github_comments_number=0,
            github_assignee_login='',
            github_assignee_url_profile='',
            deadline=deadline_1
        )
        Issue.objects.create(
            repository=r,
            github_number=0,
            github_html_url='',
            github_state='',
            github_title='Issue out of date',
            github_body='',
            label='',
            github_created_at=datetime.now(),
            github_updated_at=datetime.now(),
            github_comments_number=0,
            github_assignee_login='',
            github_assignee_url_profile='',
            deadline=deadline_2
        )

    def test_issue_is_not_out_dated(self):
        issue = Issue.objects.get(github_title='Issue')
        out_of_date = issue.is_out_of_date()
        self.assertFalse(out_of_date)

    def test_issue_is_out_of_dated(self):
        issue = Issue.objects.get(github_title='Issue out of date')
        out_of_date = issue.is_out_of_date()
        self.assertTrue(out_of_date)
