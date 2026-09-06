"""Tunnel manager orchestrates VPN connections and protocol handling."""

import asyncio
import logging
from typing import Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


class TunnelState(Enum):
    """Connection state enumeration."""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    DISCONNECTING = "disconnecting"
    ERROR = "error"


class ProtocolType(Enum):
    """Supported VPN protocols."""
    MASQUE = "masque"
    WIREGUARD = "wireguard"
    GOOL = "gool"
    CLOUDFLARE_ZT = "cloudflare_zt"
    PSIPHON = "psiphon"


@dataclass
class ConnectionStats:
    """Connection statistics."""
    connected_at: Optional[datetime] = None
    disconnected_at: Optional[datetime] = None
    bytes_sent: int = 0
    bytes_received: int = 0
    packets_sent: int = 0
    packets_received: int = 0
    current_latency_ms: float = 0.0
    protocol: Optional[ProtocolType] = None
    gateway_address: Optional[str] = None
    local_ip: Optional[str] = None
    remote_ip: Optional[str] = None
    errors: list = field(default_factory=list)


class TunnelManager:
    """Manages VPN tunnel lifecycle and protocol handling."""
    
    def __init__(self):
        """Initialize tunnel manager."""
        self.state = TunnelState.DISCONNECTED
        self.stats = ConnectionStats()
        self.current_protocol: Optional[ProtocolType] = None
        self._connection_task: Optional[asyncio.Task] = None
        self._stats_task: Optional[asyncio.Task] = None
        logger.info("TunnelManager initialized")
    
    async def connect(self, protocol: ProtocolType, config: Dict[str, Any]) -> bool:
        """Connect using specified protocol.
        
        Args:
            protocol: Protocol type to use
            config: Protocol configuration dictionary
            
        Returns:
            True if connection successful, False otherwise
        """
        if self.state != TunnelState.DISCONNECTED:
            logger.warning(f"Cannot connect: tunnel in {self.state.value} state")
            return False
        
        try:
            self.state = TunnelState.CONNECTING
            self.current_protocol = protocol
            self.stats.protocol = protocol
            self.stats.connected_at = datetime.now()
            
            logger.info(f"Connecting via {protocol.value} protocol...")
            
            # Protocol-specific connection logic would go here
            # For now, simulate connection
            await asyncio.sleep(1)
            
            self.state = TunnelState.CONNECTED
            logger.info(f"Successfully connected via {protocol.value}")
            return True
            
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            self.state = TunnelState.ERROR
            self.stats.errors.append(str(e))
            return False
    
    async def disconnect(self) -> bool:
        """Disconnect from VPN.
        
        Returns:
            True if disconnection successful, False otherwise
        """
        if self.state != TunnelState.CONNECTED:
            logger.warning(f"Cannot disconnect: tunnel in {self.state.value} state")
            return False
        
        try:
            self.state = TunnelState.DISCONNECTING
            logger.info("Disconnecting...")
            
            # Protocol-specific disconnection logic would go here
            await asyncio.sleep(1)
            
            self.state = TunnelState.DISCONNECTED
            self.stats.disconnected_at = datetime.now()
            self.current_protocol = None
            
            logger.info("Successfully disconnected")
            return True
            
        except Exception as e:
            logger.error(f"Disconnection failed: {e}")
            self.state = TunnelState.ERROR
            self.stats.errors.append(str(e))
            return False
    
    def get_connection_duration(self) -> Optional[float]:
        """Get connection duration in seconds.
        
        Returns:
            Duration in seconds or None if not connected
        """
        if self.stats.connected_at is None:
            return None
        
        end_time = self.stats.disconnected_at or datetime.now()
        return (end_time - self.stats.connected_at).total_seconds()
    
    def is_connected(self) -> bool:
        """Check if tunnel is connected.
        
        Returns:
            True if connected, False otherwise
        """
        return self.state == TunnelState.CONNECTED
    
    def get_stats(self) -> ConnectionStats:
        """Get connection statistics.
        
        Returns:
            Connection statistics object
        """
        return self.stats
