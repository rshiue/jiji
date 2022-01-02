from typing import Callable, Dict

import requests
from requests.auth import HTTPBasicAuth


class JiraQuery:

    def __init__(self):
        self.name = ''
        self.max_results = -1
        self.api_host = ''
        self.username = ''
        self.password = ''
        self.title_field = ''
        self.start_date_field = ''
        self.end_date_field = ''
        self.jql = ''
        self.startAt = 0
        self.dest = ''

    def resolve(self, args):
        if args is None:
            return self

        self.name = args.sheet_name if args.sheet_name else 'main'
        self.jql = args.query if args else ''
        self.max_results = -1
        self.startAt = 0
        self.start_date_field = args.start_date_field
        self.end_date_field = args.end_date_field
        self.api_host = args.host
        self.password = args.password
        self.username = args.username
        self.title_field = args.title_field
        self.dest = args.dest
        return self

    def __call__(self, adapter_func):
        return self.__collect_issues(adapter_func)

    def __collect_issues(self, adapter_function: Callable[['JiraQuery'], Dict]):
        resp = requests.post(self.api_host,
                             auth=HTTPBasicAuth(self.username, self.password),
                             json=adapter_function(self))
        return resp.json()
