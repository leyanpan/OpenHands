from dataclasses import dataclass
from typing import ClassVar

from openhands.core.schema import ActionType
from openhands.events.action.action import (
    Action,
    ActionSecurityRisk,
)


@dataclass
class IssuesQueryAction(Action):
    query: str
    thought: str = ''
    # TODO: add ISSUEQUERY to ActionType
    action: str = ActionType.ISSUESQUERY
    runnable: ClassVar[bool] = True
    security_risk: ActionSecurityRisk | None = None
    # Hazel TODO: Add more fields as needed

    @property
    def message(self) -> str:
        return f'I am querying jira and github for issues related to {self.query}'

    def __str__(self) -> str:
        ret = '**IssuesQueryAction**\n'
        if self.thought:
            ret += f'THOUGHT: {self.thought}\n'
        ret += f'Query: {self.query}'
        return ret
