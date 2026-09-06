"""Configuration management for AetherST."""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import asdict, dataclass

logger = logging.getLogger(__name__)


@dataclass
class GatewayConfig:
    """Gateway configuration."""
    name: str
    address: str
    port: int
    protocol: str
    enabled: bool = True


@dataclass
class NetworkConfig:
    """Network configuration."""
    dns_servers: list = None
    dns_over_https: bool = True
    ipv6_enabled: bool = True
    killswitch_enabled: bool = True
    
    def __post_init__(self):
        if self.dns_servers is None:
            self.dns_servers = ["1.1.1.1", "1.0.0.1"]  # Cloudflare


class ConfigManager:
    """Manages application configuration."""
    
    DEFAULT_CONFIG_PATH = Path.home() / ".aetherst" / "config.json"
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize config manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.data: Dict[str, Any] = {}
        self.gateways: Dict[str, GatewayConfig] = {}
        self.network = NetworkConfig()
        
        logger.info(f"ConfigManager initialized with path: {self.config_path}")
    
    def load(self) -> None:
        """Load configuration from file."""
        try:
            if self.config_path.exists():
                with open(self.config_path, "r") as f:
                    self.data = json.load(f)
                logger.info(f"Configuration loaded from {self.config_path}")
            else:
                logger.info("No existing configuration found, using defaults")
                self._create_default_config()
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            self._create_default_config()
    
    def save(self) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_path, "w") as f:
                json.dump(self.data, f, indent=2)
            logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
    
    def _create_default_config(self) -> None:
        """Create default configuration."""
        self.data = {
            "version": "1.0.0",
            "ui": {
                "theme": "dark",
                "start_minimized": False,
                "auto_connect": False,
            },
            "connection": {
                "protocol": "masque",
                "auto_select_gateway": True,
            },
            "network": {
                "dns_servers": ["1.1.1.1", "1.0.0.1"],
                "dns_over_https": True,
                "ipv6_enabled": True,
                "killswitch_enabled": True,
            },
        }
        self.save()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key (dot notation supported)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self.data
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value.
        
        Args:
            key: Configuration key (dot notation supported)
            value: Value to set
        """
        keys = key.split(".")
        config = self.data
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save()
