"""Utility functions for VirusTotal CLI Wrapper."""

import hashlib
import os
from pathlib import Path
from typing import Optional, Tuple


def calculate_sha256(file_path: str) -> str:
    """Calculate SHA256 hash of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        SHA256 hash as a hex string
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


def get_file_size(file_path: str) -> int:
    """Get file size in bytes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File size in bytes
    """
    return Path(file_path).stat().st_size


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Human-readable file size
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"


def get_app_executable(app_path: Path) -> Optional[Path]:
    """Extract executable path from macOS .app bundle.
    
    For .app files, tries to find the main executable in:
    1. Contents/MacOS/ directory (standard location)
    2. First executable found in the bundle
    
    Args:
        app_path: Path to the .app bundle
        
    Returns:
        Path to the executable, or None if not found
    """
    if not app_path.exists() or not app_path.is_dir():
        return None
    
    if not app_path.name.endswith('.app'):
        return None
    
    # Try standard location: Contents/MacOS/
    macos_dir = app_path / "Contents" / "MacOS"
    if macos_dir.exists() and macos_dir.is_dir():
        # Look for the main executable (usually has the same name as the app)
        app_name = app_path.name.replace('.app', '')
        main_exec = macos_dir / app_name
        
        if main_exec.exists() and main_exec.is_file():
            return main_exec
        
        # If not found, try first executable
        for item in macos_dir.iterdir():
            if item.is_file() and os.access(item, os.X_OK):
                return item
    
    return None


def validate_file_path(file_path: str) -> Tuple[Optional[Path], Optional[str]]:
    """Validate and return a Path object if file exists.
    
    Supports both regular files and macOS .app bundles.
    
    Args:
        file_path: Path to validate (file or .app bundle)
        
    Returns:
        Tuple of (Path object, app_name or None)
        Path object if valid, None otherwise
        app_name is set if it's a .app file
    """
    path = Path(file_path).resolve()
    
    # Check if it's a regular file
    if path.exists() and path.is_file():
        return path, None
    
    # Check if it's a macOS .app bundle
    if path.exists() and path.is_dir() and path.name.endswith('.app'):
        executable = get_app_executable(path)
        if executable:
            return executable, path.name
    
    return None, None
