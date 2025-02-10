from typing import Optional

from openhands.events.action import Action, IssuesQueryAction
from openhands.events.observation.issues import IssuesQueryObservation
from openhands.runtime.plugins.requirement import Plugin, PluginRequirement


class IssuesPluginRequirement(PluginRequirement):
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
        if not isinstance(action, IssuesQueryAction):
            raise ValueError(
                'Invalid action type, IssuesPlugin only supports IssuesQueryAction'
            )
        # query = action.query
        # Hazel TODO: Add querying logic
        return IssuesQueryObservation(content='', issues=[])
