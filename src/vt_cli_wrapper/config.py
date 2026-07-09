"""Configuration management for VirusTotal CLI Wrapper."""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any


class ConfigManager:
    """Manages API keys and configuration settings across platforms."""

    def __init__(self):
        """Initialize the configuration manager."""
        self.config_dir = self._get_config_dir()
        self.config_file = self.config_dir / "vt_config.json"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self._load_config()

    @staticmethod
    def _get_config_dir() -> Path:
        """Get the appropriate config directory for the current platform."""
        if os.name == "nt":  # Windows
            config_path = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        else:  # macOS and Linux
            config_path = Path.home() / ".config"

        return config_path / "vt-cli-wrapper"

    def _load_config(self) -> None:
        """Load configuration from file if it exists."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    self.config = json.load(f)
                # Migrate old config format to new one
                self._migrate_config()
            except (json.JSONDecodeError, IOError):
                self.config = self._default_config()
        else:
            self.config = self._default_config()

    def _migrate_config(self) -> None:
        """Migrate old config format to new format."""
        stats = self.config.get("api_stats", {})
        
        # Migrate from old format (daily_limit: 4) to new format
        if stats.get("daily_limit") == 4 and "monthly_limit" not in stats:
            stats["daily_limit"] = 500
            stats["monthly_limit"] = 15500
            stats["requests_this_month"] = stats.get("requests_today", 0)
            stats["last_month_reset"] = stats.get("last_reset")
            stats["rate_limit_per_minute"] = 4
            
            # Remove old upload fields
            stats.pop("uploads_today", None)
            stats.pop("upload_limit", None)
            
            self.config["api_stats"] = stats
            self.save_config()

    @staticmethod
    def _default_config() -> Dict[str, Any]:
        """Return default configuration."""
        return {
            "api_key": None,
            "api_stats": {
                "requests_today": 0,
                "requests_this_month": 0,
                "last_reset": None,
                "last_month_reset": None,
                "daily_limit": 500,  # Free tier: 500 lookups per day
                "monthly_limit": 15500,  # Free tier: 15.5K lookups per month
                "rate_limit_per_minute": 4,  # Free tier: 4 requests per minute
            }
        }

    def save_config(self) -> None:
        """Save configuration to file."""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=2)
        # Set appropriate permissions
        os.chmod(self.config_file, 0o600)

    def set_api_key(self, api_key: str) -> None:
        """Set and save the API key."""
        self.config["api_key"] = api_key
        self.save_config()

    def get_api_key(self) -> Optional[str]:
        """Get the stored API key."""
        return self.config.get("api_key")

    def get_api_stats(self) -> Dict[str, Any]:
        """Get API usage statistics."""
        return self.config.get("api_stats", {})

    def update_api_stats(self, request_type: str = "request") -> None:
        """Update API usage statistics.
        
        Args:
            request_type: Type of request (currently only "request" is used)
        """
        from datetime import datetime

        stats = self.config["api_stats"]
        today = datetime.now().date().isoformat()
        today_year_month = datetime.now().strftime("%Y-%m")
        last_reset = stats.get("last_reset")
        last_month_reset = stats.get("last_month_reset")

        # Reset daily counter if it's a new day
        if last_reset != today:
            stats["requests_today"] = 0
            stats["last_reset"] = today

        # Reset monthly counter if it's a new month
        if last_month_reset != today_year_month:
            stats["requests_this_month"] = 0
            stats["last_month_reset"] = today_year_month

        stats["requests_today"] += 1
        stats["requests_this_month"] += 1

        self.save_config()

    def get_remaining_quota(self) -> Dict[str, int]:
        """Get remaining quota for requests (daily and monthly)."""
        stats = self.config["api_stats"]
        return {
            "daily_remaining": max(0, stats.get("daily_limit", 500) - stats.get("requests_today", 0)),
            "monthly_remaining": max(0, stats.get("monthly_limit", 15500) - stats.get("requests_this_month", 0)),
        }

    def can_make_request(self) -> bool:
        """Check if we can make another API request."""
        quota = self.get_remaining_quota()
        return quota["daily_remaining"] > 0 and quota["monthly_remaining"] > 0
