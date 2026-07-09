"""Tests for configuration management."""

import json
import tempfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from vt_cli_wrapper.config import ConfigManager


def test_config_creation():
    """Test that config is created with defaults."""
    config = ConfigManager()
    assert config.config is not None
    assert config.config.get("api_key") is None
    assert "api_stats" in config.config


def test_api_key_storage():
    """Test API key storage and retrieval."""
    config = ConfigManager()
    test_key = "test_api_key_12345"
    
    config.set_api_key(test_key)
    assert config.get_api_key() == test_key


def test_quota_tracking():
    """Test quota tracking and remaining quota."""
    config = ConfigManager()
    
    initial_quota = config.get_remaining_quota()
    assert initial_quota["daily_remaining"] == 500
    assert initial_quota["monthly_remaining"] == 15500
    
    config.update_api_stats("request")
    quota = config.get_remaining_quota()
    assert quota["daily_remaining"] == 499
    assert quota["monthly_remaining"] == 15499


def test_can_make_request():
    """Test request quota checking."""
    config = ConfigManager()
    assert config.can_make_request() is True
    
    # Exhaust daily quota (500 lookups/day)
    stats = config.config["api_stats"]
    stats["requests_today"] = 500
    config.save_config()
    
    assert config.can_make_request() is False


if __name__ == "__main__":
    test_config_creation()
    test_api_key_storage()
    test_quota_tracking()
    test_can_make_request()
    print("All tests passed!")
