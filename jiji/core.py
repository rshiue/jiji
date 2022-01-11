import argparse
import os
from pathlib import Path
from textwrap import dedent
from typing import Dict

import xlsxwriter

from .client import JiraQuery


def main():
    parser = argparse.ArgumentParser(
        description='jiji parameters usage and examples.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent("""
        
        I hope this tool can save your time on querying Jira issues, 
        filling them in an Excel file, and sending your boss.
        
        Example
        -------
        
        $ jiji --query "project in (ABC, EDF) AND status in (Open, \\"InProgress\\")" 
            --username [USERNAME] --password [SECRET] --host https://company.com/rest/api/2/search 
            --start_date_field customfield_NNNN --end_date_field customfield_MMMM --dest issues.xlsx
        
        Bugs
        ----
        
        Please raise issues here. Thank you.
        
            https://github.com/rshiue/jiji/issues
        
        """))

    parser.add_argument('--query', required=True, help='The JQL sent to the Jira server')
    parser.add_argument('--username', required=True, help='The username for the Jira server')
    parser.add_argument('--password', required=True, help='The password for the Jira server')
    parser.add_argument('--host', required=True, help='The URI to the Jira server. E.g. https://jira.compay.com')
    parser.add_argument('--start_date_field', required=True,
                        help='The custom field name to specify start date of an issue. E.g. customfield_10201')
    parser.add_argument('--end_date_field', required=True,
                        help='The custom field name to specify end date of an issue. E.g. customfield_10202')
    parser.add_argument('--sheet_name', required=False, type=ascii, help='The name of worksheet of result workbook')
    parser.add_argument('--title_field', default='summary',
                        help='The field name to represent title of an issue')
    parser.add_argument('--dest', required=True, help='file path to create the workbook')

    args = parser.parse_args()
    query = JiraQuery().resolve(args)
    build_workbook(query(__default_jql_option_adapter), query)


def __default_jql_option_adapter(query: JiraQuery) -> Dict:
    return {
        'jql': query.jql,
        'startAt': query.startAt, 'maxResults': query.max_results,
        'fields': ['id', 'key', 'summary', 'status', 'self', query.start_date_field, query.end_date_field]}


def build_workbook(jira_issue_json, query):
    if not jira_issue_json or 'issues' not in jira_issue_json or not jira_issue_json['issues']:
        print('No issues found. No file will be created')
        return
    if Path(query.dest).exists():
        os.remove(query.dest)
    workbook = xlsxwriter.Workbook(query.dest)
    sheet = workbook.add_worksheet(query.name)
    num_issues = len(jira_issue_json['issues'])
    for index, issue in enumerate(jira_issue_json['issues']):
        sheet.write(index, 0, issue["key"])
        sheet.write(index, 1, issue["fields"]["summary"])
        if query.start_date_field in issue["fields"]:
            sheet.write(index, 2, issue["fields"][query.start_date_field])
        if query.end_date_field in issue["fields"]:
            sheet.write(index, 3, issue["fields"][query.end_date_field])

    workbook.close()
    print(f'Total {num_issues} issues fetched. A workbook has been created at {Path(query.dest).resolve()}')
