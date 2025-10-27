"""
Nmap Tool

Network discovery and security auditing tool.
"""

import asyncio
import shlex
from typing import Dict, Any, List
from ..base_tool import BaseTool, ToolResult, ToolStatus


class NmapTool(BaseTool):
    """Nmap network discovery and security auditing tool"""

    def __init__(self, name: str = "nmap", category: str = "network", config: Dict[str, Any] = None):
        super().__init__(name, category, config)

    async def execute(self, target: str, parameters: Dict[str, Any] = None) -> ToolResult:
        """Execute nmap scan"""
        start_time = asyncio.get_event_loop().time()
        self.set_status(ToolStatus.RUNNING)
        
        try:
            if not parameters:
                parameters = {}
            
            # Build nmap command
            command = self.get_command(target, parameters)
            
            # Execute command
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            execution_time = asyncio.get_event_loop().time() - start_time
            
            # Parse results
            raw_output = stdout.decode('utf-8', errors='ignore')
            error_output = stderr.decode('utf-8', errors='ignore')
            
            success = process.returncode == 0
            
            if success:
                parsed_data = self._parse_nmap_output(raw_output)
                self.set_status(ToolStatus.COMPLETED)
            else:
                parsed_data = {}
                self.set_status(ToolStatus.FAILED)
            
            result = ToolResult(
                success=success,
                data=parsed_data,
                raw_output=raw_output,
                error_message=error_output if not success else "",
                status=self.status,
                execution_time=execution_time,
                command_executed=command,
                exit_code=process.returncode
            )
            
            self.add_result(result)
            return result
            
        except Exception as e:
            execution_time = asyncio.get_event_loop().time() - start_time
            self.set_status(ToolStatus.FAILED)
            
            result = ToolResult(
                success=False,
                data={},
                raw_output="",
                error_message=str(e),
                status=ToolStatus.FAILED,
                execution_time=execution_time,
                command_executed="",
                exit_code=-1
            )
            
            self.add_result(result)
            return result

    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate nmap parameters"""
        if not parameters:
            return True
        
        # Check for dangerous parameters
        dangerous_params = ['-oN /etc/passwd', '--script +', 'rm -rf']
        command_str = str(parameters)
        
        for dangerous in dangerous_params:
            if dangerous in command_str:
                return False
        
        return True

    def get_command(self, target: str, parameters: Dict[str, Any] = None) -> str:
        """Build nmap command"""
        if not parameters:
            parameters = {}
        
        cmd_parts = ["nmap"]
        
        # Add scan type
        scan_type = parameters.get("scan_type", "-sS")
        if scan_type:
            cmd_parts.append(scan_type)
        
        # Add ports
        ports = parameters.get("ports")
        if ports:
            cmd_parts.extend(["-p", str(ports)])
        
        # Add timing
        timing = parameters.get("timing", "-T4")
        if timing:
            cmd_parts.append(timing)
        
        # Add version detection
        if parameters.get("version_detection", False):
            cmd_parts.append("-sV")
        
        # Add OS detection
        if parameters.get("os_detection", False):
            cmd_parts.append("-O")
        
        # Add script scanning
        if parameters.get("script_scan", False):
            cmd_parts.append("-sC")
        
        # Add NSE scripts
        nse_scripts = parameters.get("nse_scripts")
        if nse_scripts:
            cmd_parts.extend(["--script", nse_scripts])
        
        # Add additional arguments
        additional_args = parameters.get("additional_args")
        if additional_args:
            cmd_parts.extend(shlex.split(additional_args))
        
        # Add output format
        output_format = parameters.get("output_format", "normal")
        if output_format == "xml":
            cmd_parts.extend(["-oX", "-"])
        elif output_format == "grepable":
            cmd_parts.extend(["-oG", "-"])
        
        # Add target
        cmd_parts.append(shlex.quote(target))
        
        return " ".join(cmd_parts)

    def get_capabilities(self) -> List[str]:
        """Get nmap capabilities"""
        return [
            "port_scanning",
            "service_detection",
            "os_detection", 
            "vulnerability_scanning",
            "script_scanning",
            "network_discovery"
        ]

    def get_supported_targets(self) -> List[str]:
        """Get supported target types"""
        return ["ip", "domain", "cidr", "ip_range"]

    def get_default_parameters(self) -> Dict[str, Any]:
        """Get default nmap parameters"""
        return {
            "scan_type": "-sS",
            "timing": "-T4",
            "ports": "1-1000",
            "version_detection": True,
            "script_scan": True
        }

    def get_parameter_schema(self) -> Dict[str, Any]:
        """Get parameter schema for validation"""
        return {
            "type": "object",
            "properties": {
                "scan_type": {
                    "type": "string",
                    "enum": ["-sS", "-sT", "-sU", "-sA", "-sW", "-sM"],
                    "description": "Scan technique"
                },
                "ports": {
                    "type": "string", 
                    "description": "Port specification (e.g., 80,443,1-1000)"
                },
                "timing": {
                    "type": "string",
                    "enum": ["-T0", "-T1", "-T2", "-T3", "-T4", "-T5"],
                    "description": "Timing template"
                },
                "version_detection": {
                    "type": "boolean",
                    "description": "Enable version detection"
                },
                "os_detection": {
                    "type": "boolean", 
                    "description": "Enable OS detection"
                },
                "script_scan": {
                    "type": "boolean",
                    "description": "Enable default script scanning"
                },
                "nse_scripts": {
                    "type": "string",
                    "description": "NSE scripts to run"
                },
                "additional_args": {
                    "type": "string",
                    "description": "Additional nmap arguments"
                },
                "output_format": {
                    "type": "string",
                    "enum": ["normal", "xml", "grepable"],
                    "description": "Output format"
                }
            }
        }

    def _parse_nmap_output(self, output: str) -> Dict[str, Any]:
        """Parse nmap output into structured data"""
        parsed = {
            "scan_info": {},
            "hosts": [],
            "summary": {}
        }
        
        lines = output.split('\n')
        current_host = None
        
        for line in lines:
            line = line.strip()
            
            # Parse scan info
            if "Nmap scan report for" in line:
                if current_host:
                    parsed["hosts"].append(current_host)
                
                host_info = line.replace("Nmap scan report for ", "")
                current_host = {
                    "host": host_info,
                    "ports": [],
                    "os": "",
                    "status": "up"
                }
            
            # Parse port information
            elif "/" in line and ("open" in line or "closed" in line or "filtered" in line):
                if current_host:
                    parts = line.split()
                    if len(parts) >= 3:
                        port_info = parts[0].split("/")
                        if len(port_info) >= 2:
                            port_data = {
                                "port": port_info[0],
                                "protocol": port_info[1],
                                "state": parts[1],
                                "service": parts[2] if len(parts) > 2 else "",
                                "version": " ".join(parts[3:]) if len(parts) > 3 else ""
                            }
                            current_host["ports"].append(port_data)
            
            # Parse OS information
            elif "OS details:" in line:
                if current_host:
                    current_host["os"] = line.replace("OS details: ", "")
            
            # Parse summary
            elif "Nmap done:" in line:
                parsed["summary"]["scan_completed"] = line
        
        # Add last host
        if current_host:
            parsed["hosts"].append(current_host)
        
        return parsed

    def is_available(self) -> bool:
        """Check if nmap is available"""
        try:
            import subprocess
            result = subprocess.run(["nmap", "--version"], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            return result.returncode == 0
        except:
            return False

    def get_version(self) -> str:
        """Get nmap version"""
        try:
            import subprocess
            result = subprocess.run(["nmap", "--version"], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if "Nmap version" in line:
                        return line.split()[-1]
            return "unknown"
        except:
            return "unknown"