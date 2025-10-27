"""
HexStrike AI Core Module

This module contains the core components of the HexStrike AI system including
the decision engine, visual engine, error handling, and application factory.
"""

from .app import create_app
from .decision_engine import IntelligentDecisionEngine, TargetProfile, TargetType, TechnologyStack, AttackChain, AttackStep
from .visual_engine import ModernVisualEngine
from .error_handler import EnhancedErrorHandler, ErrorSeverity, ErrorContext

__all__ = [
    'create_app',
    'IntelligentDecisionEngine',
    'TargetProfile', 
    'TargetType',
    'TechnologyStack',
    'AttackChain',
    'AttackStep',
    'ModernVisualEngine',
    'EnhancedErrorHandler',
    'ErrorSeverity',
    'ErrorContext'
]

__version__ = '1.0.0'