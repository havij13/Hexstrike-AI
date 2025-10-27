"""
Tool Registry

This module provides a registry for discovering and managing security tools.
"""

import importlib
import pkgutil
from typing import Dict, List, Optional, Type
from .base_tool import BaseTool
import logging


class ToolRegistry:
    """Registry for managing and discovering security tools"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._tools: Dict[str, Type[BaseTool]] = {}
        self._categories: Dict[str, List[str]] = {}
        self._initialized = False

    def initialize(self):
        """Initialize the tool registry by discovering available tools"""
        if self._initialized:
            return

        self.logger.info("Initializing tool registry...")
        
        # Discover tools in each category
        categories = ['network', 'web', 'binary', 'cloud']
        
        for category in categories:
            try:
                self._discover_tools_in_category(category)
            except Exception as e:
                self.logger.warning(f"Failed to discover tools in category {category}: {e}")

        self._initialized = True
        self.logger.info(f"Tool registry initialized with {len(self._tools)} tools")

    def _discover_tools_in_category(self, category: str):
        """Discover tools in a specific category"""
        try:
            # Import the category module
            category_module = importlib.import_module(f'tools.{category}')
            
            # Get all modules in the category package
            category_path = category_module.__path__
            
            for importer, modname, ispkg in pkgutil.iter_modules(category_path):
                if not ispkg and not modname.startswith('_'):
                    try:
                        # Import the tool module
                        tool_module = importlib.import_module(f'tools.{category}.{modname}')
                        
                        # Look for tool classes
                        for attr_name in dir(tool_module):
                            attr = getattr(tool_module, attr_name)
                            
                            # Check if it's a tool class
                            if (isinstance(attr, type) and 
                                issubclass(attr, BaseTool) and 
                                attr != BaseTool):
                                
                                tool_name = attr_name.lower().replace('tool', '')
                                self._register_tool(tool_name, attr, category)
                                
                    except Exception as e:
                        self.logger.warning(f"Failed to import tool module {category}.{modname}: {e}")
                        
        except ImportError as e:
            self.logger.warning(f"Category {category} not found: {e}")

    def _register_tool(self, name: str, tool_class: Type[BaseTool], category: str):
        """Register a tool class"""
        self._tools[name] = tool_class
        
        if category not in self._categories:
            self._categories[category] = []
        
        if name not in self._categories[category]:
            self._categories[category].append(name)
        
        self.logger.debug(f"Registered tool: {name} in category {category}")

    def register_tool(self, name: str, tool_class: Type[BaseTool], category: str):
        """Manually register a tool"""
        self._register_tool(name, tool_class, category)

    def get_tool(self, name: str) -> Optional[Type[BaseTool]]:
        """Get a tool class by name"""
        if not self._initialized:
            self.initialize()
        
        return self._tools.get(name.lower())

    def create_tool(self, name: str, config: Dict = None) -> Optional[BaseTool]:
        """Create an instance of a tool"""
        tool_class = self.get_tool(name)
        if tool_class:
            # Determine category
            category = self._get_tool_category(name)
            return tool_class(name, category, config)
        return None

    def _get_tool_category(self, name: str) -> str:
        """Get the category of a tool"""
        for category, tools in self._categories.items():
            if name.lower() in tools:
                return category
        return "unknown"

    def list_tools(self, category: str = None) -> List[str]:
        """List available tools, optionally filtered by category"""
        if not self._initialized:
            self.initialize()
        
        if category:
            return self._categories.get(category, [])
        else:
            return list(self._tools.keys())

    def list_categories(self) -> List[str]:
        """List available tool categories"""
        if not self._initialized:
            self.initialize()
        
        return list(self._categories.keys())

    def get_tools_by_category(self, category: str) -> List[str]:
        """Get all tools in a specific category"""
        if not self._initialized:
            self.initialize()
        
        return self._categories.get(category, [])

    def search_tools(self, query: str) -> List[str]:
        """Search for tools by name or capability"""
        if not self._initialized:
            self.initialize()
        
        query_lower = query.lower()
        matching_tools = []
        
        for tool_name in self._tools.keys():
            if query_lower in tool_name.lower():
                matching_tools.append(tool_name)
        
        return matching_tools

    def get_tool_info(self, name: str) -> Optional[Dict]:
        """Get information about a tool"""
        tool_class = self.get_tool(name)
        if not tool_class:
            return None
        
        # Create a temporary instance to get info
        category = self._get_tool_category(name)
        temp_tool = tool_class(name, category)
        
        return {
            "name": name,
            "category": category,
            "capabilities": temp_tool.get_capabilities(),
            "supported_targets": temp_tool.get_supported_targets(),
            "default_parameters": temp_tool.get_default_parameters(),
            "parameter_schema": temp_tool.get_parameter_schema(),
            "available": temp_tool.is_available(),
            "version": temp_tool.get_version()
        }

    def validate_tool_parameters(self, name: str, parameters: Dict) -> bool:
        """Validate parameters for a specific tool"""
        tool_class = self.get_tool(name)
        if not tool_class:
            return False
        
        category = self._get_tool_category(name)
        temp_tool = tool_class(name, category)
        
        return temp_tool.validate_parameters(parameters)

    def get_registry_stats(self) -> Dict:
        """Get registry statistics"""
        if not self._initialized:
            self.initialize()
        
        stats = {
            "total_tools": len(self._tools),
            "categories": len(self._categories),
            "tools_by_category": {}
        }
        
        for category, tools in self._categories.items():
            stats["tools_by_category"][category] = len(tools)
        
        return stats


# Global tool registry instance
tool_registry = ToolRegistry()