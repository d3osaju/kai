"""System control plugin implementation."""

import subprocess
from kai.plugins.base import Plugin
from kai.core.intent import Intent


class SystemControlPlugin(Plugin):
    """Plugin for controlling system applications and processes."""
    
    def __init__(self):
        super().__init__(
            name="system_control",
            version="1.0.0",
            intents=["launch_app", "close_app"]
        )
        
    async def handle_intent(self, intent: Intent) -> str:
        """Handle system control intents.
        
        Args:
            intent: Intent to handle
            
        Returns:
            Response text
        """
        if intent.name == "launch_app":
            return await self._launch_app(intent)
        elif intent.name == "close_app":
            return await self._close_app(intent)
        
        return "Unknown system control command"
    
    async def _launch_app(self, intent: Intent) -> str:
        """Launch an application.
        
        Args:
            intent: Intent with app name
            
        Returns:
            Response text
        """
        app_name = intent.entities.get("app")
        if not app_name:
            return "I need to know which application to launch"
        
        try:
            subprocess.Popen([app_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return f"Launching {app_name}"
        except FileNotFoundError:
            return f"Could not find application: {app_name}"
        except Exception as e:
            return f"Error launching {app_name}: {str(e)}"
    
    async def _close_app(self, intent: Intent) -> str:
        """Close an application.
        
        Args:
            intent: Intent with app name
            
        Returns:
            Response text
        """
        app_name = intent.entities.get("app")
        if not app_name:
            return "I need to know which application to close"
        
        try:
            subprocess.run(["pkill", app_name], check=True)
            return f"Closed {app_name}"
        except subprocess.CalledProcessError:
            return f"Could not find running process: {app_name}"
        except Exception as e:
            return f"Error closing {app_name}: {str(e)}"
