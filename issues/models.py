from django.db import models


class Repository(models.Model):
    github_id = models.IntegerField()
    github_name = models.TextField()
    github_full_name = models.TextField()
    open_issues_count = models.IntegerField()
    owner_login = models.TextField()

    def __str__(self):
        return self.github_name
