# jiji

A command line to query and print Jira issues in an Excel workbook.

Example:
```bash
python jiji --query "project in (PRJ1, PRJ2) AND status = Open ORDER BY key ASC" --username robert@company.com --password [SECRET] --host https://jira.mycompany.com/rest/api/2/search --start_date_field customfield_10444 --end_date_field customfield_10445 --dest my_issue_report.xlsx
```

# Prerequisites

- Set up two custom fields of issue for start-date and end-date. The names of fields don't matter. Jiji only need to know the ``id of the field`` 
- Ensure Jira REST API is enabled.
- Ensure you have access to the projects or filter you'll be querying.

# Installation
You can install by ``pip`` via this repository. 

```bash
python3 -m pip install -e git+https://github.com/rshiue/jiji.git/#egg=jiji
```

# Usage

1. Prepare your JQL on your Jira server.
1. install jiji
1. call jiji 
   ```shell
   python jiji --query "[YOUR JQL]" --username [USER NAME] --password [SECRET] --host https://[YOUR JIRA SERVER]/rest/api/2/search --start_date_field [FIELD NAME of your custom start date] --end_date_field [FIELD NAME of your custom end date] --dest [YOUR FILE NAME].xlsx
   ```
1. An Excel workbook should be generated.


