"""File-related observation classes for tracking file operations."""

from dataclasses import dataclass, field
from typing import List

from openhands.core.schema import ObservationType
from openhands.events.observation.observation import Observation

# base class


@dataclass
class Issue:
    id: str
    source: str
    title: str
    created: str
    description: str
    status: List[str] = field(default_factory=list)
    comments: List[str] = field(default_factory=list)
    # unified issue datastructure
    # {


#   "id": "5590",
#   "source": "github",
#   "title": "HIVE-28518: Iceberg: Fix ClassCastException during in-place migration to Iceberg tables with timestamp columns",
#   "created": "12/25/24",
#   "description": "### What changes were proposed in this pull request? This fix improves the stability and reliability of in-place migrated Iceberg tables involving timestamp data types. ### Why are the changes needed? The issue occurred due to incorrect type casting in the timestamp handling logic, which caused the migrated Iceberg tables Fetch task to fail. ### Does this PR introduce _any_ user-facing change? No ### Is the change a dependency upgrade? No ### How was this patch tested? Qtest - iceberg_inplace_migration_with_timestamp_column.q",
#   "status": ["closed", "merged"]
#   "comments": [],
#   "jira_tickets": ["28518"],
#   "jira_issue_number": null,
#   "github_related_pr": ["5590"]
# }
# id, source,title, created, description, comments that shared with jira/github issue should be put in the issue base class. For github PR, initialize with base class, create additional attributes e.g. status, patch content, commit list
# one PR the patch file would contain all the modification
# jira issue creates additional attributes e.g. component
# github commit: patch content, if it is in one pr, we won't treat it as a standalone commit. We would include it in githubPR. So githubPR actually would be treated as parent class of githubcommit. For now, we don't care github commit implement.


@dataclass
class JiraIssue(Issue):
    def __str__(self) -> str:
        """Get a string representation of the Jira issue that gets passed to the agent"""
        return (
            f"Jira Issue {self.id}\n"
            f"Created: {self.created}\n"
            f"Title: {self.title}\n"
            f"Description: {self.description}\n"
            f"Status: {' '.join(self.status)}\n"
            f"Comments: {'\n---------------------\n'.join(self.comments)}\n"
        )


@dataclass
class GithubIssue(Issue):
    id: str
    # Hazel TODO: Add more fields as needed


@dataclass
class GithubPR(Issue):
    def __str__(self) -> str:
        return ''


@dataclass
class GithubCommit(Issue):
    id: str
    # Hazel TODO: Add more fields as needed


@dataclass
class IssuesQueryObservation(Observation):
    issues: List[JiraIssue | GithubIssue | GithubPR | GithubCommit]
    # TODO: Add ISSUES to ObservationType
    observation: str = ObservationType.ISSUES

    def get_agent_obs_text(self):
        """Get a concise text that will be shown to the agent."""
        return 'The following issues were found:\n' + '\n\n'.join(
            str(issue) for issue in self.issues
        )


# # --- Utility Functions ---
# def clean_text(text: str) -> str:
#     if not text:
#         return ''
#     text = re.sub(r'\s+', ' ', text).strip()
#     text = re.sub(r'<[^>]+>', '', text)
#     text = re.sub(r'\{.*?\}', '', text)
#     return text.strip()


# def extract_ticket_number(text: str) -> str:
#     match = re.search(r'[A-Z]+-(\d+)', text, flags=re.IGNORECASE)
#     return match.group(1) if match else ''


# def extract_all_ticket_numbers(text: str) -> List[str]:
#     tickets = re.findall(r'([A-Z]+-\d+)', text, flags=re.IGNORECASE)
#     return list(
#         {
#             extract_ticket_number(ticket)
#             for ticket in tickets
#             if extract_ticket_number(ticket)
#         }
#     )


# def extract_ticket_ids(text: str) -> List[str]:
#     return extract_all_ticket_numbers(text)


# def extract_keywords(text: str, num_keywords: int = 3) -> List[str]:
#     rake_extractor = Rake()  # Uses default English stopwords.
#     rake_extractor.extract_keywords_from_text(text)
#     ranked_phrases = rake_extractor.get_ranked_phrases()
#     return ranked_phrases[:num_keywords] if ranked_phrases else []


# def extract_github_info(text: str, github_repo: str) -> dict:
#     commit_pattern = rf'\[[^|]+\|(https://github\.com/{re.escape(github_repo)}/commit/([a-f0-9]{{7,40}}))\]|(https://github\.com/{re.escape(github_repo)}/commit/([a-f0-9]{{7}})[a-f0-9]*)'
#     pr_pattern = rf'\[[^|]+\|(https://github\.com/{re.escape(github_repo)}/pull/\d+)\]|(https://github\.com/{re.escape(github_repo)}/pull/\d+)'

#     commit_matches = re.findall(commit_pattern, text, flags=re.IGNORECASE)
#     commits = []
#     for m in commit_matches:
#         commit_id_full = m[1] or m[3]
#         if commit_id_full:
#             commits.append(commit_id_full[:7])
#     pr_matches = re.findall(pr_pattern, text, flags=re.IGNORECASE)
#     prs = [m[0] or m[1] for m in pr_matches if (m[0] or m[1])]
#     return {'commits': list(set(commits)), 'prs': list(set(prs))}


# # --- Configuration Loader ---
# def load_config(payload: dict) -> dict:
#     """
#     Reads configuration from the payload.
#     Expected keys: "jira_config" and "github_config".
#     """
#     config = {
#         'jira': {
#             'server': payload.get('jira_config', {}).get(
#                 'server', 'https://issues.apache.org/jira'
#             ),
#             'username': payload.get('jira_config', {}).get('username', ''),
#             'token': payload.get('jira_config', {}).get('token', ''),
#         },
#         'github': {
#             'repo': payload.get('github_config', {}).get('repo', ''),
#             'token': payload.get('github_config', {}).get('token', None),
#         },
#     }
#     return config


# def get_top5_related_jira_issues(
#     issue_key: str, config: dict
# ) -> IssuesQueryObservation:
#     """
#     Fetch the content of a given Jira issue, extract keywords using RAKE,
#     and search for up to 5 related issues in the same project.
#     Returns an IssuesQueryObservation containing JiraIssue objects.
#     """
#     from jira import JIRA

#     try:
#         jira_client = JIRA(
#             server=config['jira']['server'],
#             basic_auth=(config['jira']['username'], config['jira']['token']),
#         )
#     except Exception as e:
#         print(f'Error initializing Jira client: {e}')
#         return IssuesQueryObservation(issues=[])
#     try:
#         current_issue = jira_client.issue(issue_key)
#     except Exception as e:
#         print(f'Error fetching issue {issue_key}: {e}')
#         return IssuesQueryObservation(issues=[])

#     summary_text = clean_text(current_issue.fields.summary)
#     description_text = clean_text(current_issue.fields.description or '')
#     combined_text = f'{summary_text} {description_text}'
#     keywords = extract_keywords(combined_text, num_keywords=3)
#     if not keywords:
#         keywords = ['issue']
#     project_key = issue_key.split('-')[0]
#     clauses = [f'(summary ~ "{kw}" OR description ~ "{kw}")' for kw in keywords]
#     jql_query = (
#         f'project = {project_key} AND {" AND ".join(clauses)} ORDER BY created DESC'
#     )
#     try:
#         found_issues = jira_client.search_issues(jql_query, maxResults=5)
#     except Exception as e:
#         print(f'Error executing JQL: {e}')
#         return IssuesQueryObservation(issues=[])
#     related_issues = [i for i in found_issues if i.key != issue_key]
#     jira_issues = []
#     for i in related_issues:
#         sum_text = clean_text(i.fields.summary)
#         desc_text = clean_text(i.fields.description or '')
#         ticket_num = extract_ticket_number(i.key)
#         jira_issues.append(
#             JiraIssue(id=ticket_num, summary=sum_text, description=desc_text)
#         )
#     return IssuesQueryObservation(issues=jira_issues)


# def get_github_pr_details(pr_id: int, config: dict) -> IssuesQueryObservation:
#     """
#     Fetch the details of a GitHub PR (by id), including patch content and title,
#     and extract any Jira ticket numbers from the PR title.
#     Returns an IssuesQueryObservation containing a single GithubPR object.
#     """
#     from github import Github

#     try:
#         gh = (
#             Github(config['github'].get('token'))
#             if config['github'].get('token')
#             else Github()
#         )
#         repo = gh.get_repo(config['github']['repo'])
#         pr = repo.get_pull(pr_id)
#     except Exception as e:
#         print(f'Error fetching GitHub PR {pr_id}: {e}')
#         return IssuesQueryObservation(issues=[])

#     pr_title = pr.title
#     tickets = extract_ticket_ids(pr_title)
#     try:
#         patch_content = pr.patch
#     except Exception:
#         patch_content = ''
#     github_pr = GithubPR(
#         id=str(pr.number),
#         title=pr_title,
#         patch_content=patch_content,
#         jira_tickets=tickets,
#     )
#     return IssuesQueryObservation(issues=[github_pr])


# # --- Main Execution ---
# if __name__ == '__main__':
#     # Load configuration from a JSON payload file if provided; else use defaults.
#     if len(sys.argv) > 1:
#         config_path = sys.argv[1]
#         with open(config_path, 'r') as f:
#             payload = json.load(f)
#         config = load_config(payload)
#     else:
#         config = {
#             'jira': {
#                 'server': os.environ.get(
#                     'JIRA_SERVER', 'https://issues.apache.org/jira'
#                 ),
#                 'username': os.environ.get('JIRA_USERNAME', ''),
#                 'token': os.environ.get('JIRA_TOKEN', ''),
#             },
#             'github': {
#                 'repo': os.environ.get('GITHUB_REPO', ''),
#                 'token': os.environ.get('GITHUB_TOKEN', None),
#             },
#         }

#     # Example usage:
#     # 1) Given a Jira issue key, fetch top 5 related Jira issues.
#     test_jira_key = 'HIVE-28708'  # Replace with a valid issue key.
#     jira_obs = get_top5_related_jira_issues(test_jira_key, config)
#     print('=== Related Jira Issues ===')
#     print(jira_obs.get_agent_obs_text())

#     # 2) Given a GitHub PR id, fetch the PR details.
#     test_pr_id = 5589  # Replace with a valid PR id.
#     github_obs = get_github_pr_details(test_pr_id, config)
#     print('\n=== GitHub PR Details ===')
#     print(github_obs.get_agent_obs_text())

# Optionally, print JSON for debugging:
# print(json.dumps([asdict(issue) for issue in jira_obs.issues], indent=2, default=custom_encoder))
# print(json.dumps([asdict(issue) for issue in github_obs.issues], indent=2, default=custom_encoder))
