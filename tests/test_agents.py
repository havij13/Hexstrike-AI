"""
Tests for AI Agents

This module contains unit tests for the AI agent functionality.
"""

import pytest
import asyncio
from agents.base_agent import BaseAgent, AgentResult, AgentStatus
from agents.bugbounty_agent import BugBountyWorkflowManager, BugBountyTarget
from agents.ctf_agent import CTFWorkflowManager, CTFChallenge
from agents.vulnerability_agent import VulnerabilityCorrelator
from agents.browser_agent import BrowserAgent


class TestBaseAgent:
    """Test cases for BaseAgent"""

    def test_agent_initialization(self):
        """Test agent initialization"""
        config = {"test_param": "test_value"}
        
        class TestAgent(BaseAgent):
            async def execute(self, target, parameters=None):
                return AgentResult(True, {}, "Test successful", AgentStatus.COMPLETED)
            
            def validate_parameters(self, parameters):
                return True
        
        agent = TestAgent("test_agent", config)
        
        assert agent.name == "test_agent"
        assert agent.config == config
        assert agent.status == AgentStatus.IDLE
        assert len(agent.execution_history) == 0

    def test_agent_status_management(self):
        """Test agent status management"""
        class TestAgent(BaseAgent):
            async def execute(self, target, parameters=None):
                return AgentResult(True, {}, "Test successful", AgentStatus.COMPLETED)
            
            def validate_parameters(self, parameters):
                return True
        
        agent = TestAgent("test_agent")
        
        assert agent.get_status() == AgentStatus.IDLE
        
        agent.set_status(AgentStatus.RUNNING)
        assert agent.get_status() == AgentStatus.RUNNING
        
        agent.set_status(AgentStatus.COMPLETED)
        assert agent.get_status() == AgentStatus.COMPLETED

    def test_agent_result_history(self):
        """Test agent result history management"""
        class TestAgent(BaseAgent):
            async def execute(self, target, parameters=None):
                return AgentResult(True, {}, "Test successful", AgentStatus.COMPLETED)
            
            def validate_parameters(self, parameters):
                return True
        
        agent = TestAgent("test_agent")
        
        # Add test results
        result1 = AgentResult(True, {"data": 1}, "First result", AgentStatus.COMPLETED, 1.0)
        result2 = AgentResult(False, {}, "Second result", AgentStatus.FAILED, 2.0, ["Error"])
        
        agent.add_result(result1)
        agent.add_result(result2)
        
        history = agent.get_execution_history()
        assert len(history) == 2
        assert history[0] == result1
        assert history[1] == result2
        
        last_result = agent.get_last_result()
        assert last_result == result2

    def test_agent_statistics(self):
        """Test agent statistics calculation"""
        class TestAgent(BaseAgent):
            async def execute(self, target, parameters=None):
                return AgentResult(True, {}, "Test successful", AgentStatus.COMPLETED)
            
            def validate_parameters(self, parameters):
                return True
        
        agent = TestAgent("test_agent")
        
        # Add test results
        agent.add_result(AgentResult(True, {}, "Success 1", AgentStatus.COMPLETED, 1.0))
        agent.add_result(AgentResult(True, {}, "Success 2", AgentStatus.COMPLETED, 2.0))
        agent.add_result(AgentResult(False, {}, "Failure", AgentStatus.FAILED, 3.0))
        
        stats = agent.get_statistics()
        
        assert stats["total_executions"] == 3
        assert stats["successful_executions"] == 2
        assert stats["failed_executions"] == 1
        assert stats["success_rate"] == 2/3
        assert stats["average_execution_time"] == 2.0  # (1+2+3)/3


class TestBugBountyWorkflowManager:
    """Test cases for BugBountyWorkflowManager"""

    def setup_method(self):
        """Setup test fixtures"""
        self.agent = BugBountyWorkflowManager()

    def test_initialization(self):
        """Test bug bounty agent initialization"""
        assert self.agent.name == "BugBountyWorkflowManager"
        assert len(self.agent.high_impact_vulns) > 0
        assert len(self.agent.reconnaissance_tools) > 0

    def test_validate_parameters(self):
        """Test parameter validation"""
        # Valid parameters
        valid_params = {"workflow_type": "reconnaissance"}
        assert self.agent.validate_parameters(valid_params)
        
        # Invalid parameters
        invalid_params = {"workflow_type": "invalid_type"}
        assert not self.agent.validate_parameters(invalid_params)
        
        # Empty parameters should be valid
        assert self.agent.validate_parameters({})

    def test_get_capabilities(self):
        """Test capabilities listing"""
        capabilities = self.agent.get_capabilities()
        
        assert isinstance(capabilities, list)
        assert "reconnaissance_workflow" in capabilities
        assert "vulnerability_hunting_workflow" in capabilities

    @pytest.mark.asyncio
    async def test_execute_reconnaissance_workflow(self):
        """Test reconnaissance workflow execution"""
        target = "example.com"
        parameters = {"workflow_type": "reconnaissance"}
        
        result = await self.agent.execute(target, parameters)
        
        assert isinstance(result, AgentResult)
        assert result.success
        assert result.status == AgentStatus.COMPLETED
        assert "phases" in result.data

    @pytest.mark.asyncio
    async def test_execute_vulnerability_hunting_workflow(self):
        """Test vulnerability hunting workflow execution"""
        target = "example.com"
        parameters = {
            "workflow_type": "vulnerability_hunting",
            "priority_vulns": ["rce", "sqli"]
        }
        
        result = await self.agent.execute(target, parameters)
        
        assert isinstance(result, AgentResult)
        assert result.success
        assert "vulnerability_tests" in result.data

    def test_create_reconnaissance_workflow(self):
        """Test reconnaissance workflow creation"""
        target = BugBountyTarget(domain="example.com")
        workflow = self.agent.create_reconnaissance_workflow(target)
        
        assert isinstance(workflow, dict)
        assert workflow["target"] == "example.com"
        assert "phases" in workflow
        assert len(workflow["phases"]) > 0
        assert workflow["estimated_time"] > 0

    def test_create_vulnerability_hunting_workflow(self):
        """Test vulnerability hunting workflow creation"""
        target = BugBountyTarget(
            domain="example.com",
            priority_vulns=["rce", "sqli", "xss"]
        )
        workflow = self.agent.create_vulnerability_hunting_workflow(target)
        
        assert isinstance(workflow, dict)
        assert workflow["target"] == "example.com"
        assert "vulnerability_tests" in workflow
        assert len(workflow["vulnerability_tests"]) > 0

    def test_get_test_scenarios(self):
        """Test test scenario generation"""
        rce_scenarios = self.agent._get_test_scenarios("rce")
        assert isinstance(rce_scenarios, list)
        assert len(rce_scenarios) > 0
        
        sqli_scenarios = self.agent._get_test_scenarios("sqli")
        assert isinstance(sqli_scenarios, list)
        assert len(sqli_scenarios) > 0


class TestCTFWorkflowManager:
    """Test cases for CTFWorkflowManager"""

    def setup_method(self):
        """Setup test fixtures"""
        self.agent = CTFWorkflowManager()

    def test_initialization(self):
        """Test CTF agent initialization"""
        assert self.agent.name == "CTFWorkflowManager"
        assert len(self.agent.category_tools) > 0
        assert len(self.agent.solving_strategies) > 0

    def test_validate_parameters(self):
        """Test parameter validation"""
        # Valid parameters
        valid_params = {
            "category": "web",
            "difficulty": "medium"
        }
        assert self.agent.validate_parameters(valid_params)
        
        # Invalid category
        invalid_params = {"category": "invalid_category"}
        assert not self.agent.validate_parameters(invalid_params)

    @pytest.mark.asyncio
    async def test_execute_challenge_workflow(self):
        """Test CTF challenge workflow execution"""
        target = "https://ctf.example.com/challenge1"
        parameters = {
            "challenge_name": "Web Challenge 1",
            "category": "web",
            "difficulty": "medium",
            "points": 100
        }
        
        result = await self.agent.execute(target, parameters)
        
        assert isinstance(result, AgentResult)
        assert result.success
        assert "tools" in result.data
        assert "strategies" in result.data

    def test_create_ctf_challenge_workflow(self):
        """Test CTF challenge workflow creation"""
        challenge = CTFChallenge(
            name="SQL Injection Challenge",
            category="web",
            description="Find and exploit SQL injection vulnerability",
            points=200,
            difficulty="hard"
        )
        
        workflow = self.agent.create_ctf_challenge_workflow(challenge)
        
        assert isinstance(workflow, dict)
        assert workflow["challenge"] == "SQL Injection Challenge"
        assert workflow["category"] == "web"
        assert workflow["difficulty"] == "hard"
        assert len(workflow["tools"]) > 0
        assert workflow["estimated_time"] > 0

    def test_select_tools_for_challenge(self):
        """Test tool selection for challenges"""
        web_challenge = CTFChallenge(
            name="Web Challenge",
            category="web",
            description="SQL injection in login form"
        )
        
        tools = self.agent._select_tools_for_challenge(web_challenge)
        
        assert isinstance(tools, list)
        assert len(tools) > 0
        assert "sqlmap" in tools  # Should include sqlmap for SQL injection

    def test_create_ctf_team_strategy(self):
        """Test CTF team strategy creation"""
        challenges = [
            CTFChallenge("Web 1", "web", "Easy web challenge", 100, "easy"),
            CTFChallenge("Crypto 1", "crypto", "RSA challenge", 200, "medium"),
            CTFChallenge("Pwn 1", "pwn", "Buffer overflow", 300, "hard")
        ]
        
        strategy = self.agent.create_ctf_team_strategy(challenges, team_size=3)
        
        assert isinstance(strategy, dict)
        assert strategy["team_size"] == 3
        assert "challenge_allocation" in strategy
        assert "expected_score" in strategy


class TestVulnerabilityCorrelator:
    """Test cases for VulnerabilityCorrelator"""

    def setup_method(self):
        """Setup test fixtures"""
        self.agent = VulnerabilityCorrelator()

    def test_initialization(self):
        """Test vulnerability correlator initialization"""
        assert self.agent.name == "VulnerabilityCorrelator"
        assert len(self.agent.vulnerability_patterns) > 0
        assert len(self.agent.severity_scores) > 0

    @pytest.mark.asyncio
    async def test_execute_correlation(self):
        """Test vulnerability correlation execution"""
        vulnerabilities = [
            {
                "name": "SQL Injection",
                "description": "SQL injection vulnerability in login form",
                "severity": "high"
            },
            {
                "name": "XSS",
                "description": "Cross-site scripting in search parameter",
                "severity": "medium"
            }
        ]
        
        parameters = {
            "analysis_type": "correlation",
            "vulnerabilities": vulnerabilities
        }
        
        result = await self.agent.execute("example.com", parameters)
        
        assert isinstance(result, AgentResult)
        assert result.success
        assert "total_vulnerabilities" in result.data
        assert "severity_distribution" in result.data

    def test_correlate_vulnerabilities(self):
        """Test vulnerability correlation"""
        vulnerabilities = [
            {"name": "SQL Injection", "description": "sql injection", "severity": "high"},
            {"name": "XSS", "description": "cross-site scripting", "severity": "medium"}
        ]
        
        correlation = self.agent.correlate_vulnerabilities(vulnerabilities)
        
        assert isinstance(correlation, dict)
        assert correlation["total_vulnerabilities"] == 2
        assert "severity_distribution" in correlation
        assert "vulnerability_types" in correlation

    def test_classify_vulnerability(self):
        """Test vulnerability classification"""
        sql_vuln = {"description": "SQL injection vulnerability", "name": "SQLi"}
        classification = self.agent._classify_vulnerability(sql_vuln)
        assert classification == "sql_injection"
        
        xss_vuln = {"description": "Cross-site scripting attack", "name": "XSS"}
        classification = self.agent._classify_vulnerability(xss_vuln)
        assert classification == "xss"


class TestBrowserAgent:
    """Test cases for BrowserAgent"""

    def setup_method(self):
        """Setup test fixtures"""
        self.agent = BrowserAgent()

    def test_initialization(self):
        """Test browser agent initialization"""
        assert self.agent.name == "BrowserAgent"
        assert len(self.agent.test_scenarios) > 0
        assert "headless" in self.agent.browser_config

    def test_validate_parameters(self):
        """Test parameter validation"""
        # Valid parameters
        valid_params = {"test_type": "reconnaissance"}
        assert self.agent.validate_parameters(valid_params)
        
        # Invalid parameters
        invalid_params = {"test_type": "invalid_type"}
        assert not self.agent.validate_parameters(invalid_params)

    @pytest.mark.asyncio
    async def test_execute_reconnaissance(self):
        """Test web reconnaissance execution"""
        target = "https://example.com"
        parameters = {"test_type": "reconnaissance"}
        
        result = await self.agent.execute(target, parameters)
        
        assert isinstance(result, AgentResult)
        assert result.success
        assert "page_info" in result.data
        assert "forms" in result.data

    @pytest.mark.asyncio
    async def test_perform_web_reconnaissance(self):
        """Test web reconnaissance functionality"""
        target = "https://example.com"
        
        recon_data = await self.agent.perform_web_reconnaissance(target, {})
        
        assert isinstance(recon_data, dict)
        assert recon_data["target"] == target
        assert "page_info" in recon_data
        assert "forms" in recon_data
        assert "security_headers" in recon_data

    @pytest.mark.asyncio
    async def test_authentication_testing(self):
        """Test authentication flow testing"""
        target = "https://example.com"
        
        auth_results = await self.agent.test_authentication_flows(target, {})
        
        assert isinstance(auth_results, dict)
        assert "login_mechanisms" in auth_results
        assert "password_policies" in auth_results
        assert "session_management" in auth_results