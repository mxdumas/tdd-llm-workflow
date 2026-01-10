"""Migration tools for TDD workflow backends."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .backends.files import FilesBackend
from .backends.jira.client import JiraClient
from .config import JiraConfig


@dataclass
class MigrationResult:
    """Result of a migration operation."""

    success: bool = True
    epics_created: int = 0
    tasks_created: int = 0
    epics_skipped: int = 0
    tasks_skipped: int = 0
    mapping: dict[str, str] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


class FilesToJiraMigrator:
    """Migrate from files backend to Jira."""

    def __init__(
        self,
        jira_config: JiraConfig,
        project_root: Path | None = None,
        dry_run: bool = False,
    ):
        """Initialize migrator.

        Args:
            jira_config: Jira configuration.
            project_root: Project root directory.
            dry_run: If True, don't actually create issues.
        """
        self.jira_config = jira_config
        self.project_root = project_root or Path.cwd()
        self.dry_run = dry_run
        self.files_backend = FilesBackend(project_root=self.project_root)
        self._client: JiraClient | None = None

    @property
    def client(self) -> JiraClient:
        """Get or create Jira client."""
        if self._client is None:
            self._client = JiraClient(self.jira_config)
        return self._client

    def _create_epic_in_jira(self, epic_id: str, name: str, description: str) -> str | None:
        """Create an epic in Jira.

        Args:
            epic_id: Local epic ID (E1, E2, etc.)
            name: Epic name.
            description: Epic description.

        Returns:
            Jira issue key or None if dry run.
        """
        if self.dry_run:
            return f"DRY-{epic_id}"

        project = self.jira_config.effective_project_key
        epic_type = self.jira_config.epic_issue_type

        # Create epic via Jira API
        payload = {
            "fields": {
                "project": {"key": project},
                "summary": f"{epic_id}: {name}",
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": description or "No description"}],
                        }
                    ],
                },
                "issuetype": {"name": epic_type},
            }
        }

        response = self.client._client.post("/issue", json=payload)
        data = self.client._handle_response(response)
        return data.get("key")  # type: ignore

    def _create_task_in_jira(
        self,
        task_id: str,
        epic_key: str,
        title: str,
        description: str,
        acceptance_criteria: str | None,
        is_completed: bool,
    ) -> str | None:
        """Create a task in Jira.

        Args:
            task_id: Local task ID (T1, T2, etc.)
            epic_key: Parent Jira epic key.
            title: Task title.
            description: Task description.
            acceptance_criteria: Acceptance criteria.
            is_completed: Whether task is completed.

        Returns:
            Jira issue key or None if dry run.
        """
        if self.dry_run:
            return f"DRY-{task_id}"

        project = self.jira_config.effective_project_key
        task_types = self.jira_config.task_issue_types
        task_type = task_types[0] if task_types else "Story"

        # Build description with acceptance criteria
        full_description = description or ""
        if acceptance_criteria:
            full_description += f"\n\n**Acceptance Criteria:**\n{acceptance_criteria}"

        payload: dict = {
            "fields": {
                "project": {"key": project},
                "summary": f"{task_id}: {title}",
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": full_description or "No description"}],
                        }
                    ],
                },
                "issuetype": {"name": task_type},
                "parent": {"key": epic_key},
            }
        }

        response = self.client._client.post("/issue", json=payload)
        data = self.client._handle_response(response)
        task_key = data.get("key")  # type: ignore

        # Transition to Done if completed
        if is_completed and task_key and not self.dry_run:
            self.client.transition_to_status(task_key, "Done")

        return task_key

    def migrate(self, progress_callback=None) -> MigrationResult:
        """Run the migration.

        Args:
            progress_callback: Optional callback(current, total, message).

        Returns:
            MigrationResult with statistics and mapping.
        """
        result = MigrationResult()

        try:
            # Load all epics from files backend
            epics = self.files_backend.list_epics()

            if not epics:
                result.errors.append("No epics found in docs/epics/")
                result.success = False
                return result

            total_items = len(epics) + sum(len(e.tasks) for e in epics)
            current = 0

            for epic in epics:
                if progress_callback:
                    progress_callback(current, total_items, f"Creating epic {epic.id}")

                try:
                    # Create epic in Jira
                    epic_key = self._create_epic_in_jira(
                        epic_id=epic.id,
                        name=epic.name,
                        description=epic.description,
                    )

                    if epic_key:
                        result.mapping[epic.id] = epic_key
                        result.epics_created += 1

                        # Create tasks for this epic
                        for task in epic.tasks:
                            current += 1
                            if progress_callback:
                                progress_callback(current, total_items, f"Creating task {task.id}")

                            try:
                                task_key = self._create_task_in_jira(
                                    task_id=task.id,
                                    epic_key=epic_key,
                                    title=task.title,
                                    description=task.description,
                                    acceptance_criteria=task.acceptance_criteria,
                                    is_completed=(task.status == "completed"),
                                )

                                if task_key:
                                    # Map as epic_id/task_id -> jira_key
                                    result.mapping[f"{epic.id}/{task.id}"] = task_key
                                    result.tasks_created += 1

                            except Exception as e:
                                result.errors.append(f"Failed to create task {task.id}: {e}")

                except Exception as e:
                    result.errors.append(f"Failed to create epic {epic.id}: {e}")

                current += 1

        except FileNotFoundError as e:
            result.errors.append(str(e))
            result.success = False

        except Exception as e:
            result.errors.append(f"Migration failed: {e}")
            result.success = False

        return result

    def save_mapping(self, mapping: dict[str, str], path: Path | None = None) -> Path:
        """Save ID mapping to JSON file.

        Args:
            mapping: Dict of local_id -> jira_key.
            path: Output path. Defaults to docs/jira-mapping.json.

        Returns:
            Path where mapping was saved.
        """
        output_path = path or (self.project_root / "docs" / "jira-mapping.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(mapping, f, indent=2)

        return output_path
