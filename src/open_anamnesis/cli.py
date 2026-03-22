"""
CLI module for Anamnesis. Provides commands for project initialization, compilation, and building.
"""

import click
import os
from pathlib import Path
from .project import Project
from .compiler import Compiler
from .builder import Builder


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Anamnesis - A dbt-like platform for flashcard projects"""
    pass


@main.command()
@click.argument("project_name", required=False, default="anamnesis_project")
def init(project_name):
    """Initialize a new Anamnesis project."""
    try:
        project = Project.create_new(project_name)
        click.secho(f"SUCCESS: Project '{project_name}' initialized successfully!", fg="green")
        click.echo(f"  Location: {project.root_path}")
        click.echo("  Next steps:")
        click.echo(f"    1. cd {project_name}")
        click.echo("    2. Create your decks in the 'decks/' directory")
        click.echo("    3. Run 'anamnesis-compile' to validate your project")
        click.echo("    4. Run 'anamnesis-build' to generate the web interface")
    except Exception as e:
        click.secho(f"ERROR: Error initializing project: {e}", fg="red")
        raise click.Abort()


@main.command()
@click.option("--project-dir", "-d", default=".", help="Project directory")
def compile(project_dir):
    """Compile and validate all project files."""
    compile_cmd(project_dir)


def compile_cmd(project_dir="."):
    """Internal compile command function."""
    try:
        if not Path(project_dir).exists():
            raise FileNotFoundError(f"Project directory not found: {project_dir}")
        
        compiler = Compiler(project_dir)
        results = compiler.compile()
        
        if results["success"]:
            click.secho(f"SUCCESS: Compilation successful!", fg="green")
            click.echo(f"  - Validated {results['decks_count']} deck(s)")
            click.echo(f"  - Validated {results['cards_count']} card(s)")
            click.echo(f"  - No errors found")
        else:
            click.secho(f"ERROR: Compilation failed with {len(results['errors'])} error(s)", fg="red")
            for error in results["errors"]:
                click.echo(f"  • {error}")
            raise click.Abort()
    except Exception as e:
        click.secho(f"ERROR: Error during compilation: {e}", fg="red")
        raise click.Abort()


@main.command()
@click.option("--project-dir", "-d", default=".", help="Project directory")
@click.option("--port", "-p", default=5000, help="Port to run the web server on")
@click.option("--host", default="127.0.0.1", help="Host to run the web server on")
def build(project_dir, port, host):
    """Build and generate the web interface for the project."""
    build_cmd(project_dir, port, host)


def build_cmd(project_dir=".", port=5000, host="127.0.0.1"):
    """Internal build command function."""
    try:
        if not Path(project_dir).exists():
            raise FileNotFoundError(f"Project directory not found: {project_dir}")
        
        # First compile to validate
        compiler = Compiler(project_dir)
        compile_results = compiler.compile()
        
        if not compile_results["success"]:
            click.secho(f"ERROR: Compilation failed. Fix errors before building.", fg="red")
            for error in compile_results["errors"]:
                click.echo(f"  • {error}")
            raise click.Abort()
        
        # Then build
        builder = Builder(project_dir)
        builder.build()
        
        # Serve (will print success message)
        builder.serve(host, port)
        
    except KeyboardInterrupt:
        pass  # Graceful exit
    except Exception as e:
        click.secho(f"ERROR: Error during build: {e}", fg="red")
        raise click.Abort()


if __name__ == "__main__":
    main()
