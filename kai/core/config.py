"""Configuration management."""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Configuration manager for Kai."""
    
    DEFAULT_CONFIG = {
        "core": {
            "language": "en-US",
            "log_level": "INFO",
            "wake_word": "hey kai",
        },
        "audio": {
            "input_device": "default",
            "output_device": "default",
            "sample_rate": 16000,
        },
        "models": {
            "stt": "whisper-base",
            "llm": "llama3.2:3b",
            "tts": "piper-en_US-lessac-medium",
        },
        "plugins": {
            "enabled": ["system_control", "general_query", "command_executor"],
            "disabled": [],
        },
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            config_path: Path to config file, defaults to ~/.config/kai/config.yaml
        """
        if config_path is None:
            config_path = os.path.expanduser("~/.config/kai/config.yaml")
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                user_config = yaml.safe_load(f) or {}
            # Merge with defaults
            config = self.DEFAULT_CONFIG.copy()
            self._deep_merge(config, user_config)
            return config
        else:
            # Create default config
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            self.save(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
    
    def _deep_merge(self, base: Dict, update: Dict):
        """Recursively merge update into base."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key.
        
        Args:
            key: Configuration key (e.g., 'core.language')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value by dot-notation key.
        
        Args:
            key: Configuration key (e.g., 'core.language')
            value: Value to set
        """
        keys = key.split(".")
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save()
    
    def save(self, config: Optional[Dict] = None):
        """Save configuration to file.
        
        Args:
            config: Configuration dict to save, defaults to current config
        """
        if config is None:
            config = self.config
        
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False)
