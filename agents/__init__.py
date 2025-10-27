"""
Agents Module

This module contains AI-powered agents for different security testing workflows
including bug bounty hunting, CTF competitions, vulnerability analysis, and browser automation.
"""

from .base_agent import BaseAgent
from .bugbounty_agent import BugBountyWorkflowManager
from .ctf_agent import CTFWorkflowManager
from .vulnerability_agent import VulnerabilityCorrelator
from .browser_agent import BrowserAgent

__all__ = [
    'BaseAgent',
    'BugBountyWorkflowManager',
    'CTFWorkflowManager', 
    'VulnerabilityCorrelator',
    'BrowserAgent'
]