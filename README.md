# jiji

A command line to query and print Jira issues in an Excel workbook.

Example:
```bash
python jiji --query "project in (PRJ1, PRJ2) AND status = Open ORDER BY key ASC" --username robert@company.com --password [SECRET] --host https://jira.mycompany.com/rest/api/2/search --start_date_field customfield_10444 --end_date_field customfield_10445 --dest my_issue_report.xlsx
```
