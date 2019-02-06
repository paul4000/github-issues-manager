import requests


class GithubRequestsMaker:
    """
        Helper class to constructing and sending Github API requests.
    """

    def __init__(self, access_token):
        self.github_endpoint = 'https://api.github.com'
        self.headers = {'Accept': 'application/vnd.github.v3+json',
                         'Authorization': 'token ' + access_token}

    def get_repositories(self):
        """
            Method makes GET /user/repos method
        :return: list of repositories of logged user (owned and contributed)
        """
        repos_endpoint = self.github_endpoint + '/user/repos'
        response = requests.get(repos_endpoint, headers=self.headers)

        return response

    def get_issues(self, owner, repo):
        """
        Method makes GET /repos/:owner/:repo/issues
        :param owner: owner of repository
        :param repo: source repository for requested issues
        :return: response with list of all (opened and closed) issues for repository
        """
        issues_endpoint = self.github_endpoint + ('/repos/%s/%s/issues' % (owner, repo)) + '?state=all'
        response = requests.get(issues_endpoint, headers=self.headers)

        return response

    def close_issue(self, owner, repo, issue_number):
        """
        Method makes PATCH /repos/:owner/:repo/issues/:number to close issue
        :param owner: owner of repository
        :param repo: repository to which issue belongs
        :param issue_number: issue's for close number
        :return: response with issue with 'closed' state field
        """

        self.headers['Accept'] = 'application/vnd.github.symmetra-preview+json'
        patch_issue_endpoint = self.github_endpoint + ('/repos/%s/%s/issues/%d' % (owner, repo, issue_number))
        payload = "{ \"state\" : \"closed\"}"
        r = requests.patch(patch_issue_endpoint, payload, headers=self.headers)
        return r
