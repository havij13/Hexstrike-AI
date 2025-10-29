"""
Tests for Security Tools

This module contains unit tests for the security tools functionality.
"""

import pytest
import asyncio
from tools.base_tool import BaseTool, ToolResult, ToolStatus
from tools.tool_registry import ToolRegistry
from tools.network.nmap_tool import NmapTool
from tools.network.rustscan_tool import RustscanTool
from tools.web.gobuster_tool import GobusterTool
from tools.web.nuclei_tool import NucleiTool


class TestBaseTool:
    """Test cases for BaseTool"""

    def test_tool_initialization(self):
        """Test tool initialization"""
        config = {"timeout": 30}
        
        class TestTool(BaseTool):
            async def execute(self, target, parameters=None):
                return ToolResult(True, {}, "Test output", "", ToolStatus.COMPLETED)
            
            def validate_parameters(self, parameters):
                return True
            
            def get_command(self, target, parameters=None):
                return f"test_command {target}"
        
        tool = TestTool("test_tool", "test_category", config)
        
        assert tool.name == "test_tool"
        assert tool.category == "test_category"
        assert tool.config == config
        assert tool.status == ToolStatus.IDLE

    def test_tool_status_management(self):
        """Test tool status management"""
        class TestTool(BaseTool):
            async def execute(self, target, parameters=None):
                return ToolResult(True, {}, "Test output", "", ToolStatus.COMPLETED)
            
            def validate_parameters(self, parameters):
                return True
            
            def get_command(self, target, parameters=None):
                return f"test_command {target}"
        
        tool = TestTool("test_tool", "test_category")
        
        assert tool.get_status() == ToolStatus.IDLE
        
        tool.set_status(ToolStatus.RUNNING)
        assert tool.get_status() == ToolStatus.RUNNING

    def test_tool_result_history(self):
        """Test tool result history"""
        class TestTool(BaseTool):
            async def execute(self, target, parameters=None):
                return ToolResult(True, {}, "Test output", "", ToolStatus.COMPLETED)
            
            def validate_parameters(self, parameters):
                return True
            
            def get_command(self, target, parameters=None):
                return f"test_command {target}"
        
        tool = TestTool("test_tool", "test_category")
        
        result1 = ToolResult(True, {"data": 1}, "Output 1", "", ToolStatus.COMPLETED, 1.0)
        result2 = ToolResult(False, {}, "Output 2", "Error", ToolStatus.FAILED, 2.0)
        
        tool.add_result(result1)
        tool.add_result(result2)
        
        history = tool.get_execution_history()
        assert len(history) == 2
        
        last_result = tool.get_last_result()
        assert last_result == result2


class TestToolRegistry:
    """Test cases for ToolRegistry"""

    def setup_method(self):
        """Setup test fixtures"""
        self.registry = ToolRegistry()

    def test_registry_initialization(self):
        """Test registry initialization"""
        assert not self.registry._initialized
        assert len(self.registry._tools) == 0
        assert len(self.registry._categories) == 0

    def test_manual_tool_registration(self):
        """Test manual tool registration"""
        class TestTool(BaseTool):
            async def execute(self, target, parameters=None):
                return ToolResult(True, {}, "Test", "", ToolStatus.COMPLETED)
            
            def validate_parameters(self, parameters):
                return True
            
            def get_command(self, target, parameters=None):
                return f"test {target}"
        
        self.registry.register_tool("test_tool", TestTool, "test_category")
        
        assert "test_tool" in self.registry._tools
        assert "test_category" in self.registry._categories
        assert "test_tool" in self.registry._categories["test_category"]

    def test_get_tool(self):
        """Test getting tool class"""
        class TestTool(BaseTool):
            async def execute(self, target, parameters=None):
                return ToolResult(True, {}, "Test", "", ToolStatus.COMPLETED)
            
            def validate_parameters(self, parameters):
                return True
            
            def get_command(self, target, parameters=None):
                return f"test {target}"
        
        self.registry.register_tool("test_tool", TestTool, "test_category")
        
        tool_class = self.registry.get_tool("test_tool")
        assert tool_class == TestTool
        
        # Test case insensitive
        tool_class = self.registry.get_tool("TEST_TOOL")
        assert tool_class == TestTool

    def test_create_tool(self):
        """Test tool instance creation"""
        class TestTool(BaseTool):
            async def execute(self, target, parameters=None):
                return ToolResult(True, {}, "Test", "", ToolStatus.COMPLETED)
            
            def validate_parameters(self, parameters):
                return True
            
            def get_command(self, target, parameters=None):
                return f"test {target}"
        
        self.registry.register_tool("test_tool", TestTool, "test_category")
        
        tool_instance = self.registry.create_tool("test_tool")
        assert isinstance(tool_instance, TestTool)
        assert tool_instance.name == "test_tool"
        assert tool_instance.category == "test_category"

    def test_list_tools(self):
        """Test listing tools"""
        class TestTool(BaseTool):
            async def execute(self, target, parameters=None):
                return ToolResult(True, {}, "Test", "", ToolStatus.COMPLETED)
            
            def validate_parameters(self, parameters):
                return True
            
            def get_command(self, target, parameters=None):
                return f"test {target}"
        
        self.registry.register_tool("test_tool1", TestTool, "category1")
        self.registry.register_tool("test_tool2", TestTool, "category2")
        
        all_tools = self.registry.list_tools()
        assert "test_tool1" in all_tools
        assert "test_tool2" in all_tools
        
        category1_tools = self.registry.list_tools("category1")
        assert "test_tool1" in category1_tools
        assert "test_tool2" not in category1_tools


class TestNmapTool:
    """Test cases for NmapTool"""

    def setup_method(self):
        """Setup test fixtures"""
        self.tool = NmapTool()

    def test_initialization(self):
        """Test nmap tool initialization"""
        assert self.tool.name == "nmap"
        assert self.tool.category == "network"

    def test_validate_parameters(self):
        """Test parameter validation"""
        # Valid parameters
        valid_params = {"scan_type": "-sS", "ports": "80,443"}
        assert self.tool.validate_parameters(valid_params)
        
        # Empty parameters should be valid
        assert self.tool.validate_parameters({})

    def test_get_command(self):
        """Test command generation"""
        target = "192.168.1.1"
        parameters = {
            "scan_type": "-sS",
            "ports": "80,443",
            "timing": "-T4"
        }
        
        command = self.tool.get_command(target, parameters)
        
        assert "nmap" in command
        assert "-sS" in command
        assert "-p 80,443" in command
        assert "-T4" in command
        assert target in command

    def test_get_capabilities(self):
        """Test capabilities listing"""
        capabilities = self.tool.get_capabilities()
        
        assert isinstance(capabilities, list)
        assert "port_scanning" in capabilities
        assert "service_detection" in capabilities

    def test_parse_nmap_output(self):
        """Test nmap output parsing"""
        sample_output = """
Nmap scan report for example.com (192.168.1.1)
Host is up (0.0010s latency).
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.4
80/tcp   open  http    Apache httpd 2.4.6
443/tcp  open  https   Apache httpd 2.4.6
"""
        
        parsed = self.tool._parse_nmap_output(sample_output)
        
        assert isinstance(parsed, dict)
        assert "hosts" in parsed
        assert len(parsed["hosts"]) == 1
        
        host = parsed["hosts"][0]
        assert len(host["ports"]) == 3
        assert host["ports"][0]["port"] == "22"
        assert host["ports"][0]["state"] == "open"
        assert host["ports"][0]["service"] == "ssh"


class TestGobusterTool:
    """Test cases for GobusterTool"""

    def setup_method(self):
        """Setup test fixtures"""
        self.tool = GobusterTool()

    def test_initialization(self):
        """Test gobuster tool initialization"""
        assert self.tool.name == "gobuster"
        assert self.tool.category == "web"

    def test_get_command(self):
        """Test command generation"""
        target = "https://example.com"
        parameters = {
            "mode": "dir",
            "threads": 20,
            "extensions": "php,html"
        }
        
        command = self.tool.get_command(target, parameters)
        
        assert "gobuster" in command
        assert "dir" in command
        assert "-u https://example.com" in command
        assert "-t 20" in command
        assert "-x php,html" in command

    def test_parse_gobuster_output(self):
        """Test gobuster output parsing"""
        sample_output = """
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Mode         : dir
[+] Url/Domain   : https://example.com/
[+] Threads      : 10
[+] Wordlist     : /usr/share/wordlists/dirb/common.txt
[+] Status codes : 200,204,301,302,307,401,403
[+] User Agent   : gobuster/3.1.0
[+] Timeout      : 10s
===============================================================
/admin                (Status: 200) [Size: 1234]
/login                (Status: 200) [Size: 5678]
/api                  (Status: 403) [Size: 0]
===============================================================
Finished
===============================================================
"""
        
        parsed = self.tool._parse_gobuster_output(sample_output)
        
        assert isinstance(parsed, dict)
        assert "found_paths" in parsed
        assert len(parsed["found_paths"]) == 3
        
        admin_path = next(p for p in parsed["found_paths"] if p["path"] == "/admin")
        assert admin_path["status_code"] == "200"
        assert admin_path["size"] == "1234"


class TestNucleiTool:
    """Test cases for NucleiTool"""

    def setup_method(self):
        """Setup test fixtures"""
        self.tool = NucleiTool()

    def test_initialization(self):
        """Test nuclei tool initialization"""
        assert self.tool.name == "nuclei"
        assert self.tool.category == "web"

    def test_get_command(self):
        """Test command generation"""
        target = "https://example.com"
        parameters = {
            "severity": "critical,high",
            "tags": "sqli,xss",
            "concurrency": 50
        }
        
        command = self.tool.get_command(target, parameters)
        
        assert "nuclei" in command
        assert "-u https://example.com" in command
        assert "-severity critical,high" in command
        assert "-tags sqli,xss" in command
        assert "-c 50" in command

    def test_parse_nuclei_output_json(self):
        """Test nuclei JSON output parsing"""
        sample_json_output = """
{"template":"sql-injection","template-url":"","template-id":"sql-injection","info":{"name":"SQL Injection","author":["test"],"tags":["sqli"],"severity":"high"},"type":"http","host":"https://example.com","matched-at":"https://example.com/login","extracted-results":null,"timestamp":"2024-01-15T15:30:00Z","matcher-status":true}
{"template":"xss-reflected","template-url":"","template-id":"xss-reflected","info":{"name":"Reflected XSS","author":["test"],"tags":["xss"],"severity":"medium"},"type":"http","host":"https://example.com","matched-at":"https://example.com/search","extracted-results":null,"timestamp":"2024-01-15T15:31:00Z","matcher-status":true}
"""
        
        parsed = self.tool._parse_nuclei_output(sample_json_output, "json")
        
        assert isinstance(parsed, dict)
        assert "vulnerabilities" in parsed
        assert len(parsed["vulnerabilities"]) == 2
        
        sql_vuln = parsed["vulnerabilities"][0]
        assert sql_vuln["template-id"] == "sql-injection"
        assert sql_vuln["info"]["severity"] == "high"

    def test_parse_nuclei_output_default(self):
        """Test nuclei default output parsing"""
        sample_output = """
[high] [sql-injection] https://example.com/login
[medium] [xss-reflected] https://example.com/search?q=test
[info] [tech-detect] https://example.com [Apache/2.4.6]
"""
        
        parsed = self.tool._parse_nuclei_output(sample_output, "default")
        
        assert isinstance(parsed, dict)
        assert "vulnerabilities" in parsed
        assert len(parsed["vulnerabilities"]) == 3
        
        # Check severity distribution
        assert "statistics" in parsed
        assert "severity_distribution" in parsed["statistics"]
        assert parsed["statistics"]["severity_distribution"]["high"] == 1
        assert parsed["statistics"]["severity_distribution"]["medium"] == 1
        assert parsed["statistics"]["severity_distribution"]["info"] == 1


class TestToolRegistry:
    """Test cases for ToolRegistry"""

    def setup_method(self):
        """Setup test fixtures"""
        self.registry = ToolRegistry()

    def test_registry_initialization(self):
        """Test registry initialization"""
        assert not self.registry._initialized
        
        # Manual registration for testing
        class TestTool(BaseTool):
            async def execute(self, target, parameters=None):
                return ToolResult(True, {}, "Test", "", ToolStatus.COMPLETED)
            
            def validate_parameters(self, parameters):
                return True
            
            def get_command(self, target, parameters=None):
                return f"test {target}"
        
        self.registry.register_tool("test_tool", TestTool, "test_category")
        
        assert "test_tool" in self.registry._tools
        assert "test_category" in self.registry._categories

    def test_get_tool_info(self):
        """Test getting tool information"""
        class TestTool(BaseTool):
            async def execute(self, target, parameters=None):
                return ToolResult(True, {}, "Test", "", ToolStatus.COMPLETED)
            
            def validate_parameters(self, parameters):
                return True
            
            def get_command(self, target, parameters=None):
                return f"test {target}"
            
            def get_capabilities(self):
                return ["test_capability"]
        
        self.registry.register_tool("test_tool", TestTool, "test_category")
        
        tool_info = self.registry.get_tool_info("test_tool")
        
        assert isinstance(tool_info, dict)
        assert tool_info["name"] == "test_tool"
        assert tool_info["category"] == "test_category"
        assert "test_capability" in tool_info["capabilities"]

    def test_search_tools(self):
        """Test tool search functionality"""
        class TestTool(BaseTool):
            async def execute(self, target, parameters=None):
                return ToolResult(True, {}, "Test", "", ToolStatus.COMPLETED)
            
            def validate_parameters(self, parameters):
                return True
            
            def get_command(self, target, parameters=None):
                return f"test {target}"
        
        self.registry.register_tool("nmap_tool", TestTool, "network")
        self.registry.register_tool("gobuster_tool", TestTool, "web")
        
        # Search for "nmap"
        results = self.registry.search_tools("nmap")
        assert "nmap_tool" in results
        assert "gobuster_tool" not in results

    def test_get_registry_stats(self):
        """Test registry statistics"""
        class TestTool(BaseTool):
            async def execute(self, target, parameters=None):
                return ToolResult(True, {}, "Test", "", ToolStatus.COMPLETED)
            
            def validate_parameters(self, parameters):
                return True
            
            def get_command(self, target, parameters=None):
                return f"test {target}"
        
        self.registry.register_tool("tool1", TestTool, "category1")
        self.registry.register_tool("tool2", TestTool, "category1")
        self.registry.register_tool("tool3", TestTool, "category2")
        
        stats = self.registry.get_registry_stats()
        
        assert stats["total_tools"] == 3
        assert stats["categories"] == 2
        assert stats["tools_by_category"]["category1"] == 2
        assert stats["tools_by_category"]["category2"] == 1