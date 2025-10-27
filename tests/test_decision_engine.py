"""
Tests for Intelligent Decision Engine

This module contains unit tests for the decision engine functionality.
"""

import pytest
from core.decision_engine import (
    IntelligentDecisionEngine, 
    TargetProfile, 
    TargetType, 
    TechnologyStack,
    AttackChain,
    AttackStep
)


class TestIntelligentDecisionEngine:
    """Test cases for IntelligentDecisionEngine"""

    def setup_method(self):
        """Setup test fixtures"""
        self.engine = IntelligentDecisionEngine()

    def test_analyze_target_web_application(self):
        """Test target analysis for web applications"""
        target = "https://example.com"
        profile = self.engine.analyze_target(target)
        
        assert profile.target == target
        assert profile.target_type == TargetType.WEB_APPLICATION
        assert profile.confidence_score > 0
        assert isinstance(profile.ip_addresses, list)

    def test_analyze_target_network_host(self):
        """Test target analysis for network hosts"""
        target = "192.168.1.1"
        profile = self.engine.analyze_target(target)
        
        assert profile.target == target
        assert profile.target_type == TargetType.NETWORK_HOST
        assert profile.confidence_score > 0

    def test_analyze_target_api_endpoint(self):
        """Test target analysis for API endpoints"""
        target = "https://api.example.com/v1/users"
        profile = self.engine.analyze_target(target)
        
        assert profile.target == target
        assert profile.target_type == TargetType.API_ENDPOINT

    def test_analyze_target_binary_file(self):
        """Test target analysis for binary files"""
        target = "/path/to/binary.exe"
        profile = self.engine.analyze_target(target)
        
        assert profile.target == target
        assert profile.target_type == TargetType.BINARY_FILE

    def test_select_optimal_tools_web_target(self):
        """Test tool selection for web applications"""
        profile = TargetProfile(
            target="https://example.com",
            target_type=TargetType.WEB_APPLICATION
        )
        
        tools = self.engine.select_optimal_tools(profile, "comprehensive")
        
        assert isinstance(tools, list)
        assert len(tools) > 0
        assert "nuclei" in tools
        assert "gobuster" in tools

    def test_select_optimal_tools_network_target(self):
        """Test tool selection for network hosts"""
        profile = TargetProfile(
            target="192.168.1.1",
            target_type=TargetType.NETWORK_HOST
        )
        
        tools = self.engine.select_optimal_tools(profile, "comprehensive")
        
        assert isinstance(tools, list)
        assert len(tools) > 0
        assert "nmap" in tools

    def test_select_optimal_tools_quick_objective(self):
        """Test tool selection with quick objective"""
        profile = TargetProfile(
            target="https://example.com",
            target_type=TargetType.WEB_APPLICATION
        )
        
        tools = self.engine.select_optimal_tools(profile, "quick")
        
        assert isinstance(tools, list)
        assert len(tools) <= 3  # Quick scan should have fewer tools

    def test_optimize_parameters_nmap(self):
        """Test parameter optimization for nmap"""
        profile = TargetProfile(
            target="192.168.1.1",
            target_type=TargetType.NETWORK_HOST
        )
        
        params = self.engine.optimize_parameters("nmap", profile)
        
        assert isinstance(params, dict)
        assert "target" in params
        assert params["target"] == profile.target

    def test_optimize_parameters_with_context(self):
        """Test parameter optimization with context"""
        profile = TargetProfile(
            target="https://example.com",
            target_type=TargetType.WEB_APPLICATION
        )
        
        context = {"stealth": True}
        params = self.engine.optimize_parameters("nmap", profile, context)
        
        assert isinstance(params, dict)
        assert "target" in params

    def test_create_attack_chain(self):
        """Test attack chain creation"""
        profile = TargetProfile(
            target="https://example.com",
            target_type=TargetType.WEB_APPLICATION,
            confidence_score=0.8
        )
        
        chain = self.engine.create_attack_chain(profile, "comprehensive")
        
        assert isinstance(chain, AttackChain)
        assert chain.target_profile == profile
        assert len(chain.steps) > 0
        assert chain.success_probability > 0

    def test_attack_chain_calculation(self):
        """Test attack chain probability calculation"""
        profile = TargetProfile(
            target="https://example.com",
            target_type=TargetType.WEB_APPLICATION
        )
        
        chain = AttackChain(profile)
        
        # Add test steps
        step1 = AttackStep(
            tool="nmap",
            parameters={"target": "example.com"},
            expected_outcome="Port discovery",
            success_probability=0.9,
            execution_time_estimate=120
        )
        
        step2 = AttackStep(
            tool="nuclei",
            parameters={"target": "example.com"},
            expected_outcome="Vulnerability discovery",
            success_probability=0.7,
            execution_time_estimate=300
        )
        
        chain.add_step(step1)
        chain.add_step(step2)
        chain.calculate_success_probability()
        
        assert len(chain.steps) == 2
        assert chain.estimated_time == 420  # 120 + 300
        assert chain.success_probability == 0.63  # 0.9 * 0.7
        assert "nmap" in chain.required_tools
        assert "nuclei" in chain.required_tools

    def test_technology_detection_wordpress(self):
        """Test WordPress technology detection"""
        target = "https://wordpress-site.com/wp-admin"
        technologies = self.engine._detect_technologies(target)
        
        assert TechnologyStack.WORDPRESS in technologies

    def test_technology_detection_php(self):
        """Test PHP technology detection"""
        target = "https://example.com/index.php"
        technologies = self.engine._detect_technologies(target)
        
        assert TechnologyStack.PHP in technologies

    def test_cms_detection(self):
        """Test CMS detection"""
        wordpress_target = "https://example.com/wp-content"
        cms = self.engine._detect_cms(wordpress_target)
        assert cms == "WordPress"
        
        drupal_target = "https://example.com/drupal"
        cms = self.engine._detect_cms(drupal_target)
        assert cms == "Drupal"

    def test_attack_surface_calculation(self):
        """Test attack surface score calculation"""
        profile = TargetProfile(
            target="https://example.com",
            target_type=TargetType.WEB_APPLICATION,
            technologies=[TechnologyStack.PHP, TechnologyStack.WORDPRESS],
            open_ports=[80, 443, 22],
            subdomains=["api.example.com", "admin.example.com"],
            cms_type="WordPress"
        )
        
        score = self.engine._calculate_attack_surface(profile)
        
        assert isinstance(score, float)
        assert 0 <= score <= 10
        assert score > 7  # Should be high due to multiple factors

    def test_risk_level_determination(self):
        """Test risk level determination"""
        # High risk profile
        high_risk_profile = TargetProfile(
            target="https://example.com",
            target_type=TargetType.WEB_APPLICATION,
            attack_surface_score=9.0
        )
        
        risk_level = self.engine._determine_risk_level(high_risk_profile)
        assert risk_level == "critical"
        
        # Low risk profile
        low_risk_profile = TargetProfile(
            target="https://example.com",
            target_type=TargetType.WEB_APPLICATION,
            attack_surface_score=2.0
        )
        
        risk_level = self.engine._determine_risk_level(low_risk_profile)
        assert risk_level == "low"

    def test_confidence_calculation(self):
        """Test confidence score calculation"""
        # High confidence profile
        high_conf_profile = TargetProfile(
            target="https://example.com",
            target_type=TargetType.WEB_APPLICATION,
            ip_addresses=["192.168.1.1"],
            technologies=[TechnologyStack.PHP],
            cms_type="WordPress"
        )
        
        confidence = self.engine._calculate_confidence(high_conf_profile)
        assert isinstance(confidence, float)
        assert 0 <= confidence <= 1
        assert confidence > 0.8  # Should be high confidence

    def test_target_profile_serialization(self):
        """Test TargetProfile serialization"""
        profile = TargetProfile(
            target="https://example.com",
            target_type=TargetType.WEB_APPLICATION,
            ip_addresses=["192.168.1.1"],
            technologies=[TechnologyStack.PHP],
            cms_type="WordPress"
        )
        
        data = profile.to_dict()
        
        assert isinstance(data, dict)
        assert data["target"] == "https://example.com"
        assert data["target_type"] == "web_application"
        assert data["ip_addresses"] == ["192.168.1.1"]
        assert "php" in data["technologies"]
        assert data["cms_type"] == "WordPress"

    def test_attack_chain_serialization(self):
        """Test AttackChain serialization"""
        profile = TargetProfile(
            target="https://example.com",
            target_type=TargetType.WEB_APPLICATION
        )
        
        chain = AttackChain(profile)
        step = AttackStep(
            tool="nmap",
            parameters={"target": "example.com"},
            expected_outcome="Port discovery",
            success_probability=0.9,
            execution_time_estimate=120
        )
        chain.add_step(step)
        chain.calculate_success_probability()
        
        data = chain.to_dict()
        
        assert isinstance(data, dict)
        assert data["target"] == "https://example.com"
        assert len(data["steps"]) == 1
        assert data["success_probability"] == 0.9
        assert data["estimated_time"] == 120
        assert "nmap" in data["required_tools"]