"""Tests for configuration management."""

import pytest
import tempfile
from pathlib import Path
from kai.core.config import Config


def test_default_config():
    """Test default configuration creation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        config = Config(str(config_path))
        
        assert config.get("core.language") == "en-US"
        assert config.get("models.llm") == "llama3.2:3b"


def test_config_get():
    """Test getting configuration values."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        config = Config(str(config_path))
        
        assert config.get("core.language") == "en-US"
        assert config.get("nonexistent.key", "default") == "default"


def test_config_set():
    """Test setting configuration values."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        config = Config(str(config_path))
        
        config.set("core.language", "es-ES")
        assert config.get("core.language") == "es-ES"
