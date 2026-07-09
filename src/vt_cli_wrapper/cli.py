"""Command-line interface for VirusTotal wrapper."""

import click
from pathlib import Path
from tabulate import tabulate

from .config import ConfigManager
from .api_client import VirusTotalClient
from .utils import format_file_size, validate_file_path, calculate_sha256


@click.group()
@click.version_option("1.0.0")
def cli():
    """VirusTotal CLI Wrapper - Scan files with VirusTotal API."""
    pass


@cli.command()
@click.option(
    "--api-key",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="Your VirusTotal API key",
)
def setup(api_key: str) -> None:
    """Configure your VirusTotal API key."""
    config = ConfigManager()
    client = VirusTotalClient(config)

    click.echo("Validating API key...")
    if client.set_api_key(api_key):
        click.secho("✓ API key configured successfully!", fg="green")
    else:
        click.secho("✗ Invalid API key. Please check and try again.", fg="red")


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option(
    "--force-upload",
    is_flag=True,
    help="Force upload even if file is found on VirusTotal",
)
def scan(file_path: str, force_upload: bool) -> None:
    """Scan a file with VirusTotal."""
    config = ConfigManager()

    # Check if API key is configured
    if not config.get_api_key():
        click.secho("✗ API key not configured. Run 'vt-cli setup' first.", fg="red")
        return

    # Validate file path (supports .app bundles on macOS)
    validated_path, app_name = validate_file_path(file_path)
    if not validated_path:
        click.secho(f"✗ File not found: {file_path}", fg="red")
        click.echo("Supported formats: regular files or macOS .app bundles")
        return

    client = VirusTotalClient(config)
    file_size = validated_path.stat().st_size

    # Display what we're scanning
    if app_name:
        click.echo(f"Scanning: {app_name} (executable: {validated_path.name})")
        click.echo(f"File size: {format_file_size(file_size)}")
    else:
        click.echo(f"Scanning: {validated_path.name} ({format_file_size(file_size)})")

    # Calculate SHA256
    with click.progressbar(length=1, label="Calculating hash") as bar:
        file_hash = calculate_sha256(str(validated_path))
        bar.update(1)

    quota = config.get_remaining_quota()
    click.echo(
        f"Quota remaining - Daily: {quota['daily_remaining']}/500, "
        f"Monthly: {quota['monthly_remaining']}/15500"
    )

    if force_upload:
        _handle_upload(client, str(validated_path))
    else:
        # Try lookup first
        click.echo("Checking VirusTotal database...")
        found, lookup_data = client.lookup_file(file_hash)

        if found:
            _display_scan_results(lookup_data, file_hash)
        elif "error" in lookup_data:
            error = lookup_data["error"]
            if "quota exceeded" in error.lower():
                click.secho(f"✗ {error}", fg="red")
                daily_remaining = lookup_data.get('daily_remaining', 0)
                monthly_remaining = lookup_data.get('monthly_remaining', 0)
                click.echo(f"Daily: {daily_remaining}/500, Monthly: {monthly_remaining}/15500")
            else:
                click.secho(f"✗ Lookup failed: {error}", fg="red")
        else:
            click.echo("File not found on VirusTotal. Submit your email to be eligible to upload:") 
            click.echo("https://www.virustotal.com/")


@cli.command()
def quota():
    """Check API quota usage."""
    config = ConfigManager()

    if not config.get_api_key():
        click.secho("✗ API key not configured.", fg="red")
        return

    stats = config.get_api_stats()
    remaining = config.get_remaining_quota()

    data = [
        ["Access Level", "Limited (Standard Free Public API)"],
        ["Request Rate Limit", "4 lookups / minute"],
        ["", ""],
        ["Daily Limit", f"{stats.get('daily_limit', 500)} lookups/day"],
        ["Lookups Today", stats.get("requests_today", 0)],
        ["Daily Remaining", remaining["daily_remaining"]],
        ["", ""],
        ["Monthly Limit", f"{stats.get('monthly_limit', 15500)} lookups/month"],
        ["Lookups This Month", stats.get("requests_this_month", 0)],
        ["Monthly Remaining", remaining["monthly_remaining"]],
        ["", ""],
        ["Last Daily Reset", stats.get("last_reset", "Never")],
        ["Last Monthly Reset", stats.get("last_month_reset", "Never")],
    ]

    click.echo("=== VirusTotal API Quota (Free Tier) ===\n")
    click.echo(tabulate(data, headers=["Metric", "Value"], tablefmt="simple"))
    click.echo("\n⚠ Usage must not be used in business workflows, commercial products or services.")


@cli.command()
def reset():
    """Reset configuration and API key."""
    if click.confirm("Are you sure you want to reset all settings?"):
        config = ConfigManager()
        config.config = config._default_config()
        config.save_config()
        click.secho("✓ Configuration reset.", fg="green")


def _handle_upload(client: VirusTotalClient, file_path: str) -> None:
    """Handle file upload process.
    
    Args:
        client: VirusTotal API client
        file_path: Path to file to upload
    """
    click.secho(
        "File upload not available on free tier.",
        fg="yellow",
    )
    click.echo("To submit files for analysis, visit: https://www.virustotal.com/")


def _display_scan_results(data: dict, file_hash: str) -> None:
    """Display scan results in a formatted table.
    
    Args:
        data: Scan results dictionary
        file_hash: SHA256 hash of the file
    """
    click.echo("\n" + "=" * 60)
    click.secho("SCAN RESULTS", fg="cyan", bold=True)
    click.echo("=" * 60)

    results_data = [
        ["File Name", data.get("file_name", "Unknown")],
        ["File Type", data.get("file_type", "Unknown")],
        ["File Size", format_file_size(data.get("file_size", 0))],
        ["SHA256", file_hash],
        ["", ""],
    ]

    # Color code the detection results
    malicious = data.get("malicious", 0)
    suspicious = data.get("suspicious", 0)
    undetected = data.get("undetected", 0)
    total = data.get("total_scans", 0)

    results_data.extend([
        ["Detections (Malicious)", click.style(str(malicious), fg="red" if malicious > 0 else "green")],
        ["Detections (Suspicious)", click.style(str(suspicious), fg="yellow" if suspicious > 0 else "green")],
        ["Undetected", str(undetected)],
        ["Total Scans", str(total)],
    ])

    click.echo(tabulate(results_data, tablefmt="simple"))

    # Overall verdict
    if malicious > 0:
        click.secho("\n⚠ WARNING: File is detected as malicious!", fg="red", bold=True)
    elif suspicious > 0:
        click.secho("\n⚠ WARNING: File is detected as suspicious!", fg="yellow", bold=True)
    else:
        click.secho("\n✓ File appears to be clean.", fg="green", bold=True)


if __name__ == "__main__":
    cli()
