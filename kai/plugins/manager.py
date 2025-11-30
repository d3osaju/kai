"""Plugin manager."""

from typing import Dict, List
from kai.core.config import Config
from kai.core.intent import Intent
from kai.plugins.base import Plugin


class PluginManager:
    """Manages plugin loading and execution."""
    
    def __init__(self, config: Config):
        """Initialize plugin manager.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.plugins: Dict[str, Plugin] = {}
        
    async def load_plugins(self):
        """Load enabled plugins."""
        enabled = self.config.get("plugins.enabled", [])
        
        # Import and instantiate enabled plugins
        for plugin_name in enabled:
            try:
                plugin = await self._load_plugin(plugin_name)
                self.plugins[plugin_name] = plugin
            except Exception as e:
                print(f"Failed to load plugin {plugin_name}: {e}")
    
    async def _load_plugin(self, name: str) -> Plugin:
        """Load a single plugin by name.
        
        Args:
            name: Plugin name
            
        Returns:
            Plugin instance
        """
        # Dynamic import
        module = __import__(f"kai.plugins.{name}", fromlist=["plugin"])
        plugin_instance = getattr(module, "plugin")
        return plugin_instance
    
    async def execute_intent(self, intent: Intent, conversation_history: list = None) -> str:
        """Execute an intent using appropriate plugin.
        
        Args:
            intent: Intent to execute
            conversation_history: Optional conversation history for context
            
        Returns:
            Response text
        """
        # Find plugin that can handle this intent
        for plugin in self.plugins.values():
            if plugin.can_handle(intent):
                # Pass history if plugin supports it
                if hasattr(plugin, 'handle_intent_with_history') and conversation_history:
                    return await plugin.handle_intent_with_history(intent, conversation_history)
                else:
                    return await plugin.handle_intent(intent)
        
        # No plugin found
        return f"I don't know how to handle: {intent.raw_text}"
    
    def list_plugins(self) -> List[str]:
        """List loaded plugins.
        
        Returns:
            List of plugin names
        """
        return list(self.plugins.keys())
