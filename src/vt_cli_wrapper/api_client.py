"""VirusTotal API client implementation."""

import time
from datetime import datetime
from typing import Dict, Optional, Any, Tuple

import requests

from .config import ConfigManager
from .utils import calculate_sha256, get_file_size


class VirusTotalClient:
    """Client for interacting with VirusTotal API v3."""

    BASE_URL = "https://www.virustotal.com/api/v3"
    FILE_SIZE_LIMIT = 650 * 1024 * 1024  # 650 MB limit

    def __init__(self, config_manager: ConfigManager):
        """Initialize VirusTotal client.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config = config_manager
        self.api_key = self.config.get_api_key()
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create a requests session with appropriate headers."""
        session = requests.Session()
        if self.api_key:
            session.headers.update({
                "x-apikey": self.api_key,
                "User-Agent": "vt-cli-wrapper/1.0",
            })
        return session

    def set_api_key(self, api_key: str) -> bool:
        """Set and validate API key.
        
        Args:
            api_key: VirusTotal API key
            
        Returns:
            True if key is valid, False otherwise
        """
        self.api_key = api_key
        self.session.headers.update({"x-apikey": api_key})

        # Test the key by making a simple API call
        try:
            response = self.session.get(f"{self.BASE_URL}/users/current")
            if response.status_code == 200:
                self.config.set_api_key(api_key)
                return True
            return False
        except requests.RequestException:
            return False

    def lookup_file(self, file_hash: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Look up a file by SHA256 hash.
        
        Args:
            file_hash: SHA256 hash of the file
            
        Returns:
            Tuple of (success, file_data)
        """
        if not self.api_key:
            return False, {"error": "API key not configured"}

        if not self.config.can_make_request():
            quota = self.config.get_remaining_quota()
            return False, {
                "error": "Daily or monthly request quota exceeded",
                "daily_remaining": quota["daily_remaining"],
                "monthly_remaining": quota["monthly_remaining"],
            }

        try:
            response = self.session.get(f"{self.BASE_URL}/files/{file_hash}")
            self.config.update_api_stats("request")

            if response.status_code == 200:
                data = response.json()
                return True, self._parse_file_response(data)
            elif response.status_code == 404:
                return False, {"error": "File not found on VirusTotal"}
            else:
                return False, {"error": f"API error: {response.status_code}"}

        except requests.RequestException as e:
            return False, {"error": f"Network error: {str(e)}"}

    def upload_file(self, file_path: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Upload a file to VirusTotal.
        
        Args:
            file_path: Path to the file to upload
            
        Returns:
            Tuple of (success, response_data)
        """
        if not self.api_key:
            return False, {"error": "API key not configured"}

        if not self.config.can_upload_file():
            quota = self.config.get_remaining_quota()
            return False, {
                "error": "Daily upload quota exceeded",
                "uploads_remaining": quota["uploads_remaining"],
            }

        # Check file size
        file_size = get_file_size(file_path)
        if file_size > self.FILE_SIZE_LIMIT:
            return False, {
                "error": f"File too large. Maximum size is 650 MB, got {file_size / (1024 * 1024):.2f} MB"
            }

        try:
            with open(file_path, "rb") as f:
                files = {"file": f}
                response = self.session.post(
                    f"{self.BASE_URL}/files",
                    files=files,
                    timeout=300  # 5 minute timeout for uploads
                )

            self.config.update_api_stats("upload")

            if response.status_code == 200:
                data = response.json()
                return True, self._parse_upload_response(data)
            else:
                return False, {"error": f"Upload failed: {response.status_code}"}

        except requests.RequestException as e:
            return False, {"error": f"Network error during upload: {str(e)}"}
        except IOError as e:
            return False, {"error": f"File read error: {str(e)}"}

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a file: first try to lookup, then upload if not found.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            Analysis result dictionary
        """
        # Calculate SHA256
        try:
            file_hash = calculate_sha256(file_path)
        except FileNotFoundError:
            return {"error": f"File not found: {file_path}"}

        # Try to lookup first
        found, lookup_data = self.lookup_file(file_hash)
        if found:
            return {
                "status": "found",
                "sha256": file_hash,
                "data": lookup_data,
            }

        # File not found, try to upload
        success, upload_data = self.upload_file(file_path)
        if success:
            return {
                "status": "uploaded",
                "sha256": file_hash,
                "data": upload_data,
                "message": "File uploaded. Analysis will be available shortly.",
            }
        else:
            return {
                "status": "error",
                "sha256": file_hash,
                "data": upload_data,
            }

    @staticmethod
    def _parse_file_response(response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse VirusTotal file lookup response.
        
        Args:
            response: Raw API response
            
        Returns:
            Parsed response
        """
        attributes = response.get("data", {}).get("attributes", {})
        last_analysis = attributes.get("last_analysis_stats", {})

        return {
            "file_name": attributes.get("meaningful_name", "Unknown"),
            "file_type": attributes.get("type_description", "Unknown"),
            "file_size": attributes.get("size", 0),
            "magic": attributes.get("magic", "Unknown"),
            "last_analysis_date": attributes.get("last_analysis_date"),
            "malicious": last_analysis.get("malicious", 0),
            "suspicious": last_analysis.get("suspicious", 0),
            "undetected": last_analysis.get("undetected", 0),
            "timeout": last_analysis.get("timeout", 0),
            "total_scans": sum(last_analysis.values()),
        }

    @staticmethod
    def _parse_upload_response(response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse VirusTotal upload response.
        
        Args:
            response: Raw API response
            
        Returns:
            Parsed response
        """
        data = response.get("data", {})
        attributes = data.get("attributes", {})

        return {
            "analysis_id": data.get("id", "Unknown"),
            "file_type": attributes.get("type", "Unknown"),
            "size": attributes.get("size", 0),
            "message": "File queued for analysis",
        }
