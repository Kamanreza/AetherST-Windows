"""Main entry point for AetherST Windows application."""

import sys
import logging
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from utils.logger import setup_logging
from core.config import ConfigManager
from ui.main_window import MainWindow

logger = logging.getLogger(__name__)


def main():
    """Initialize and run the application."""
    # Setup logging
    setup_logging()
    logger.info("Starting AetherST Windows v1.0.0")
    
    # Check for administrator privileges
    if not _is_admin():
        logger.warning("Not running with administrator privileges")
        print("⚠️  WARNING: This application requires administrator privileges.")
        print("Please run as Administrator for full functionality.")
    
    # Initialize configuration
    config = ConfigManager()
    config.load()
    logger.info(f"Configuration loaded from {config.config_path}")
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("AetherST")
    app.setApplicationVersion("1.0.0")
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    
    # Create and show main window
    window = MainWindow(config)
    window.show()
    
    logger.info("Main window displayed")
    
    # Run application
    sys.exit(app.exec())


def _is_admin():
    """Check if running with administrator privileges."""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


if __name__ == "__main__":
    main()
