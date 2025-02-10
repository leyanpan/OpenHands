"""File-related observation classes for tracking file operations."""

from dataclasses import dataclass
from typing import List

from openhands.core.schema import ObservationType
from openhands.events.observation.observation import Observation


@dataclass
class JiraIssue:
    id: str
    # Hazel TODO: Add more fields as needed

    def __str__(self) -> str:
        """Get a string representation of the Jira issue that gets passed to the agent"""
        return f'Jira issue {self.id}'


@dataclass
class GithubIssue:
    id: str
    # Hazel TODO: Add more fields as needed


@dataclass
class GithubPR:
    id: str
    # Hazel TODO: Add more fields as needed


@dataclass
class GithubCommit:
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
