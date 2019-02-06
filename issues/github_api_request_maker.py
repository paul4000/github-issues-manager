import requests


class GithubRequestsMaker:

    def __init__(self, access_token):
        self.github_endpoint = 'https://api.github.com'
        self.headers = {'Accept': 'application/vnd.github.v3+json',
                         'Authorization': 'token ' + access_token}

    def get_repositories(self):
        repos_endpoint = self.github_endpoint + '/user/repos'
        response = requests.get(repos_endpoint, headers=self.headers)

        return response

    def get_issues(self, owner, repo):
        issues_endpoint = self.github_endpoint + ('/repos/%s/%s/issues' % (owner, repo))
        response = requests.get(issues_endpoint, headers=self.headers)

        return response