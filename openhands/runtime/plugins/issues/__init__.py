from dataclasses import dataclass
from typing import Optional

from openhands.events.action import Action, IssueQueryAction
from openhands.events.observation.issues import IssuesQueryObservation, JiraIssue
from openhands.runtime.plugins.requirement import Plugin, PluginRequirement

DUMMY_JIRA_ISSUE = JiraIssue(
    id='28708',
    source='jira',
    title='Migrate Build Scan publication to develocity.apache.org',
    created='01/14/25',
    description='The Hive project publishes Build Scans to the Develocity instance at ge.apache.org. This instance migrating to a new URL, develocity.apache.org. Build scans published to ge.apache.org after today will not be migrated to the new Develocity instance.',
    status=['Resolved'],
    comments=[
        'Merged to master via [69d0a3d|https://github.com/apache/hive/commit/69d0a3ddff695597ad8221bae0ead48f8f38b57f], thanks [~clayburn] for your contribution and [~gmcdonald] for your review!'
    ],
)


@dataclass
class IssuesRequirement(PluginRequirement):
    name: str = 'issues'


class IssuesPlugin(Plugin):
    name: str = 'issues'

    # TODO: Figure out how to let the plugin initialize funciton accept more parameters
    async def initialize(
        self,
        username: str,
        jira_url: Optional[str] = None,
        jira_project: Optional[str] = None,
        github_url: Optional[str] = None,
        github_token: Optional[str] = None,
    ):
        # Hazel TODO: Run setup, including getting connecting to Jira, Github, retriving information and storing them in vdb, ...
        pass

    async def _run(self, action: Action) -> IssuesQueryObservation:
        if not isinstance(action, IssueQueryAction):
            raise ValueError(
                'Invalid action type, IssuesPlugin only supports IssuesQueryAction'
            )
        # query = action.query
        # Hazel TODO: Add querying logic
        return IssuesQueryObservation(content='', issues=[DUMMY_JIRA_ISSUE])
