"""Application state management."""

from enum import Enum
from typing import Callable, List
import logging

logger = logging.getLogger(__name__)


class ConnectionState(Enum):
    """Connection states."""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    DISCONNECTING = "disconnecting"
    ERROR = "error"


class StateManager:
    """Manages application state with observers."""
    
    def __init__(self):
        """Initialize state manager."""
        self._state = ConnectionState.DISCONNECTED
        self._observers: List[Callable] = []
        logger.info("StateManager initialized")
    
    def subscribe(self, callback: Callable) -> None:
        """Subscribe to state changes.
        
        Args:
            callback: Function to call on state change
        """
        self._observers.append(callback)
    
    def unsubscribe(self, callback: Callable) -> None:
        """Unsubscribe from state changes.
        
        Args:
            callback: Function to unsubscribe
        """
        if callback in self._observers:
            self._observers.remove(callback)
    
    def set_state(self, state: ConnectionState) -> None:
        """Set new state and notify observers.
        
        Args:
            state: New connection state
        """
        if self._state != state:
            old_state = self._state
            self._state = state
            logger.info(f"State changed: {old_state.value} → {state.value}")
            self._notify_observers()
    
    def get_state(self) -> ConnectionState:
        """Get current state.
        
        Returns:
            Current connection state
        """
        return self._state
    
    def _notify_observers(self) -> None:
        """Notify all observers of state change."""
        for observer in self._observers:
            try:
                observer(self._state)
            except Exception as e:
                logger.error(f"Error calling observer: {e}")
