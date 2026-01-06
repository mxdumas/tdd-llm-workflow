"""CLI interface for tdd-llm."""

from pathlib import Path
from typing import Annotated, Optional

import click
import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from . import __version__
from .config import (
    Config,
    CoverageThresholds,
    get_available_backends,
    get_available_languages,
    get_global_config_path,
    get_project_config_path,
    is_first_run,
    PROJECT_CONFIG_NAME,
)
from .deployer import deploy

app = typer.Typer(
    name="tdd-llm",
    help="Deploy TDD workflow templates for Claude and Gemini AI assistants.",
    no_args_is_help=True,
)
console = Console()


def run_setup_wizard() -> Config | None:
    """Run interactive setup wizard for first-time configuration.

    Returns:
        Config instance if setup completed, None if cancelled.
    """
    rprint("\n[bold cyan]Welcome to tdd-llm![/bold cyan]")
    rprint("This appears to be your first time running tdd-llm.")
    rprint("Let's set up your global configuration.\n")

    if not typer.confirm("Would you like to configure tdd-llm now?", default=True):
        rprint("[yellow]Setup skipped.[/yellow] You can run 'tdd-llm setup' later.\n")
        return None

    rprint()

    # Language selection
    available_langs = get_available_languages()
    if available_langs:
        rprint(f"[bold]Available languages:[/bold] {', '.join(available_langs)}")
        default_lang = "python" if "python" in available_langs else available_langs[0]
    else:
        default_lang = "python"

    language = typer.prompt(
        "Default programming language",
        default=default_lang,
    )

    # Backend selection
    available_backends = get_available_backends()
    if available_backends:
        rprint(f"\n[bold]Available backends:[/bold]")
        rprint("  - files: Local files (docs/epics/, docs/state.json)")
        rprint("  - jira: Jira via MCP server")

    backend = typer.prompt(
        "\nDefault backend",
        default="files",
        type=click.Choice(["files", "jira"], case_sensitive=False),
    )

    # Target selection
    rprint(f"\n[bold]Deployment targets:[/bold]")
    rprint("  - project: Deploy to .claude/ and .gemini/ in project directory")
    rprint("  - user: Deploy to user-level config directories")

    target = typer.prompt(
        "\nDefault deployment target",
        default="project",
        type=click.Choice(["project", "user"], case_sensitive=False),
    )

    # Platforms selection
    rprint(f"\n[bold]Available platforms:[/bold] claude, gemini")
    platforms_input = typer.prompt(
        "Platforms to deploy (comma-separated)",
        default="claude,gemini",
    )
    platforms = [p.strip().lower() for p in platforms_input.split(",")]

    # Coverage thresholds
    rprint(f"\n[bold]Coverage thresholds[/bold]")
    coverage_line = typer.prompt(
        "Line coverage threshold (%)",
        default=80,
        type=int,
    )
    coverage_line = max(0, min(100, coverage_line))

    coverage_branch = typer.prompt(
        "Branch coverage threshold (%)",
        default=70,
        type=int,
    )
    coverage_branch = max(0, min(100, coverage_branch))

    # Create and save config
    config = Config(
        default_target=target,  # type: ignore
        default_language=language,
        default_backend=backend,  # type: ignore
        platforms=platforms,
        coverage=CoverageThresholds(line=coverage_line, branch=coverage_branch),
    )

    saved_path = config.save(project=False)

    rprint(f"\n[green]Configuration saved to:[/green] {saved_path}")
    rprint()

    # Show summary
    table = Table(title="Global Configuration")
    table.add_column("Setting", style="bold")
    table.add_column("Value", style="cyan")

    table.add_row("Default target", config.default_target)
    table.add_row("Default language", config.default_language)
    table.add_row("Default backend", config.default_backend)
    table.add_row("Platforms", ", ".join(config.platforms))
    table.add_row("Coverage (line)", f"{config.coverage.line}%")
    table.add_row("Coverage (branch)", f"{config.coverage.branch}%")

    console.print(table)
    rprint()

    return config


@app.callback(invoke_without_command=True)
def main_callback(ctx: typer.Context):
    """Check for first run and offer setup wizard."""
    # Skip wizard for certain commands
    if ctx.invoked_subcommand in ("setup", "version"):
        return

    # Check if this is first run
    if is_first_run():
        run_setup_wizard()


def _setup_cmd(
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Re-run setup even if config exists"),
    ] = False,
):
    """Run interactive setup wizard to create global configuration."""
    if not is_first_run() and not force:
        rprint("[yellow]Global configuration already exists.[/yellow]")
        rprint(f"Location: {get_global_config_path()}")
        rprint("\nUse --force to re-run setup and overwrite.")
        raise typer.Exit(0)

    run_setup_wizard()


app.command(name="setup")(_setup_cmd)


@app.command()
def version():
    """Show version information."""
    rprint(f"[bold]tdd-llm[/bold] version {__version__}")


def _deploy_cmd(
    lang: Annotated[
        str,
        typer.Option("--lang", "-l", help="Programming language for placeholders"),
    ] = "",
    backend: Annotated[
        str,
        typer.Option("--backend", "-b", help="Backend for epics/stories (files or jira)"),
    ] = "",
    target: Annotated[
        str,
        typer.Option("--target", "-t", help="Deployment target (project or user)"),
    ] = "",
    platforms: Annotated[
        Optional[list[str]],
        typer.Option("--platform", "-p", help="Platforms to deploy (claude, gemini)"),
    ] = None,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", "-n", help="Show what would be done without doing it"),
    ] = False,
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Overwrite existing files"),
    ] = False,
):
    """Deploy TDD templates to .claude and .gemini directories."""
    config = Config.load()

    # Use config defaults if not specified
    effective_lang = lang or config.default_language
    effective_backend = backend or config.default_backend
    effective_target = target or config.default_target
    effective_platforms = platforms or config.platforms

    # Validate language
    available_langs = get_available_languages()
    if available_langs and effective_lang not in available_langs:
        rprint(f"[red]Error:[/red] Unknown language '{effective_lang}'")
        rprint(f"Available: {', '.join(available_langs)}")
        raise typer.Exit(1)

    # Validate backend
    available_backends = get_available_backends()
    if available_backends and effective_backend not in available_backends:
        rprint(f"[red]Error:[/red] Unknown backend '{effective_backend}'")
        rprint(f"Available: {', '.join(available_backends)}")
        raise typer.Exit(1)

    # Validate target
    if effective_target not in ("project", "user"):
        rprint(f"[red]Error:[/red] Target must be 'project' or 'user'")
        raise typer.Exit(1)

    # Show what we're doing
    rprint(f"\n[bold]Deploying TDD templates[/bold]")
    rprint(f"  Target: [cyan]{effective_target}[/cyan]")
    rprint(f"  Language: [cyan]{effective_lang}[/cyan]")
    rprint(f"  Backend: [cyan]{effective_backend}[/cyan]")
    rprint(f"  Platforms: [cyan]{', '.join(effective_platforms)}[/cyan]")

    if dry_run:
        rprint(f"  [yellow](dry run - no files will be written)[/yellow]")

    rprint()

    # Do the deployment
    result = deploy(
        target=effective_target,  # type: ignore
        lang=effective_lang,
        backend=effective_backend,
        platforms=effective_platforms,
        dry_run=dry_run,
        force=force,
        config=config,
    )

    # Show results
    if result.files_created:
        rprint(f"[green]Created {len(result.files_created)} files[/green]")
        for f in result.files_created[:10]:
            rprint(f"  - {f}")
        if len(result.files_created) > 10:
            rprint(f"  ... and {len(result.files_created) - 10} more")

    if result.files_converted:
        rprint(f"[blue]Converted {len(result.files_converted)} files to TOML[/blue]")

    if result.placeholders_replaced:
        unique_placeholders = set(result.placeholders_replaced)
        rprint(f"[cyan]Replaced {len(unique_placeholders)} placeholders[/cyan]")
        for p in sorted(unique_placeholders):
            rprint(f"  - {{{{{p}}}}}")

    if result.skipped:
        rprint(f"[yellow]Skipped {len(result.skipped)} existing files[/yellow]")
        rprint("  (use --force to overwrite)")

    if result.errors:
        rprint(f"[red]Errors:[/red]")
        for e in result.errors:
            rprint(f"  - {e}")
        raise typer.Exit(1)

    if result.success:
        rprint(f"\n[green]Done![/green]")
    else:
        raise typer.Exit(1)


app.command(name="deploy")(_deploy_cmd)


def _list_cmd():
    """List available languages and backends."""
    # Languages table
    langs = get_available_languages()
    lang_table = Table(title="Available Languages")
    lang_table.add_column("Language", style="cyan")

    if langs:
        for lang in langs:
            lang_table.add_row(lang)
    else:
        lang_table.add_row("[dim]No languages configured[/dim]")

    console.print(lang_table)
    console.print()

    # Backends table
    backends = get_available_backends()
    backend_table = Table(title="Available Backends")
    backend_table.add_column("Backend", style="cyan")
    backend_table.add_column("Description")

    if backends:
        descriptions = {
            "files": "Local files (docs/epics/, docs/state.json)",
            "jira": "Jira via MCP server",
        }
        for backend in backends:
            backend_table.add_row(backend, descriptions.get(backend, ""))
    else:
        backend_table.add_row("[dim]No backends configured[/dim]", "")

    console.print(backend_table)


app.command(name="list")(_list_cmd)


def _init_cmd(
    lang: Annotated[
        str,
        typer.Option("--lang", "-l", help="Default language for this project"),
    ] = "",
    backend: Annotated[
        str,
        typer.Option("--backend", "-b", help="Default backend for this project"),
    ] = "",
    coverage_line: Annotated[
        Optional[int],
        typer.Option("--coverage-line", help="Line coverage threshold (%)"),
    ] = None,
    coverage_branch: Annotated[
        Optional[int],
        typer.Option("--coverage-branch", help="Branch coverage threshold (%)"),
    ] = None,
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Overwrite existing project config"),
    ] = False,
):
    """Initialize project-level configuration (.tdd-llm.yaml)."""
    project_config_path = get_project_config_path()

    if project_config_path.exists() and not force:
        rprint(f"[yellow]Project config already exists:[/yellow] {project_config_path}")
        rprint("Use --force to overwrite")
        raise typer.Exit(1)

    # Start with global config as base
    global_config = Config.load(include_project=False)

    # Create project config with specified or inherited values
    config = Config(
        default_language=lang or global_config.default_language,
        default_backend=backend or global_config.default_backend,  # type: ignore
        default_target="project",
        platforms=global_config.platforms,
        coverage=global_config.coverage,
    )

    # Override coverage if specified
    if coverage_line is not None:
        if not 0 <= coverage_line <= 100:
            rprint(f"[red]Error:[/red] Coverage must be between 0 and 100")
            raise typer.Exit(1)
        config.coverage.line = coverage_line

    if coverage_branch is not None:
        if not 0 <= coverage_branch <= 100:
            rprint(f"[red]Error:[/red] Coverage must be between 0 and 100")
            raise typer.Exit(1)
        config.coverage.branch = coverage_branch

    saved_path = config.save(project=True)
    rprint(f"[green]Created project config:[/green] {saved_path}")
    rprint()

    # Show what was created
    table = Table(title="Project Configuration")
    table.add_column("Setting", style="bold")
    table.add_column("Value", style="cyan")

    table.add_row("Language", config.default_language)
    table.add_row("Backend", config.default_backend)
    table.add_row("Coverage (line)", f"{config.coverage.line}%")
    table.add_row("Coverage (branch)", f"{config.coverage.branch}%")

    console.print(table)


app.command(name="init")(_init_cmd)


def _config_cmd(
    show: Annotated[
        bool,
        typer.Option("--show", "-s", help="Show current configuration"),
    ] = False,
    project: Annotated[
        bool,
        typer.Option("--project", "-p", help="Modify project config instead of global"),
    ] = False,
    set_lang: Annotated[
        Optional[str],
        typer.Option("--set-lang", help="Set default language"),
    ] = None,
    set_backend: Annotated[
        Optional[str],
        typer.Option("--set-backend", help="Set default backend"),
    ] = None,
    set_target: Annotated[
        Optional[str],
        typer.Option("--set-target", help="Set default target (project or user)"),
    ] = None,
    set_coverage_line: Annotated[
        Optional[int],
        typer.Option("--set-coverage-line", help="Set line coverage threshold (%)"),
    ] = None,
    set_coverage_branch: Annotated[
        Optional[int],
        typer.Option("--set-coverage-branch", help="Set branch coverage threshold (%)"),
    ] = None,
):
    """Show or modify configuration."""
    config = Config.load()
    modified = False

    if set_lang:
        config.default_language = set_lang
        modified = True
        rprint(f"Set default language to: [cyan]{set_lang}[/cyan]")

    if set_backend:
        if set_backend not in ("files", "jira"):
            rprint(f"[red]Error:[/red] Backend must be 'files' or 'jira'")
            raise typer.Exit(1)
        config.default_backend = set_backend  # type: ignore
        modified = True
        rprint(f"Set default backend to: [cyan]{set_backend}[/cyan]")

    if set_target:
        if set_target not in ("project", "user"):
            rprint(f"[red]Error:[/red] Target must be 'project' or 'user'")
            raise typer.Exit(1)
        config.default_target = set_target  # type: ignore
        modified = True
        rprint(f"Set default target to: [cyan]{set_target}[/cyan]")

    if set_coverage_line is not None:
        if not 0 <= set_coverage_line <= 100:
            rprint(f"[red]Error:[/red] Coverage must be between 0 and 100")
            raise typer.Exit(1)
        config.coverage.line = set_coverage_line
        modified = True
        rprint(f"Set line coverage threshold to: [cyan]{set_coverage_line}%[/cyan]")

    if set_coverage_branch is not None:
        if not 0 <= set_coverage_branch <= 100:
            rprint(f"[red]Error:[/red] Coverage must be between 0 and 100")
            raise typer.Exit(1)
        config.coverage.branch = set_coverage_branch
        modified = True
        rprint(f"Set branch coverage threshold to: [cyan]{set_coverage_branch}%[/cyan]")

    if modified:
        saved_path = config.save(project=project)
        scope = "project" if project else "global"
        rprint(f"\n[green]Configuration saved to {scope} config:[/green] {saved_path}")

    if show or not modified:
        # Show effective configuration
        table = Table(title="Effective Configuration (merged)")
        table.add_column("Setting", style="bold")
        table.add_column("Value", style="cyan")

        table.add_row("Default target", config.default_target)
        table.add_row("Default language", config.default_language)
        table.add_row("Default backend", config.default_backend)
        table.add_row("Platforms", ", ".join(config.platforms))
        table.add_row("Coverage (line)", f"{config.coverage.line}%")
        table.add_row("Coverage (branch)", f"{config.coverage.branch}%")

        console.print(table)
        console.print()

        # Show config sources
        source_table = Table(title="Configuration Sources")
        source_table.add_column("Level", style="bold")
        source_table.add_column("Path")
        source_table.add_column("Status", style="dim")

        global_path = get_global_config_path()
        global_status = "[green]exists[/green]" if global_path.exists() else "[dim]not found[/dim]"
        source_table.add_row("Global", str(global_path), global_status)

        project_path = get_project_config_path()
        project_status = "[green]exists[/green]" if project_path.exists() else "[dim]not found[/dim]"
        source_table.add_row("Project", str(project_path), project_status)

        console.print(source_table)

        if project_path.exists():
            rprint(f"\n[dim]Project config overrides global config[/dim]")


app.command(name="config")(_config_cmd)


if __name__ == "__main__":
    app()
