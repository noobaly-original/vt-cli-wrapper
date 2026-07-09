"""VirusTotal CLI Wrapper - A cross-platform command-line tool for VirusTotal API."""

__version__ = "1.0.0"
__author__ = "CLI Wrapper"

from .api_client import VirusTotalClient
from .config import ConfigManager

__all__ = ["VirusTotalClient", "ConfigManager"]
