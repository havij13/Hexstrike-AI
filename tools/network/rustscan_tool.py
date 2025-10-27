"""
Rustscan Tool

Ultra-fast port scanner written in Rust.
"""

import asyncio
import json
import shlex
from typing import Dict, Any, List
from ..base_tool import BaseTool, ToolResult, ToolStatus


class RustscanTool(BaseTool):
    """Rustscan ultra-fast port scanner"""

    def __init__(self, name: str = "rustscan", category: str = "network", config: Dict[str, Any] = None):
        super().__init__(name, category, config)

    async def execute(self, target: str, parameters: Dict[str, Any] = None) -> ToolResult:
        """Execute rustscan"""
        start_time = asyncio.get_event_loop().time()
        self.set_status(ToolStatus.RUNNING)
        
        try:
            if not parameters:
                parameters = {}
            
            # Build rustscan command
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
                parsed_data = self._parse_rustscan_output(raw_output)
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
        """Validate rustscan parameters"""
        if not parameters:
            return True
        
        # Validate ulimit
        ulimit = parameters.get("ulimit")
        if ulimit and (not isinstance(ulimit, int) or ulimit < 1 or ulimit > 65535):
            return False
        
        # Validate batch size
        batch_size = parameters.get("batch_size")
        if batch_size and (not isinstance(batch_size, int) or batch_size < 1):
            return False
        
        # Validate timeout
        timeout = parameters.get("timeout")
        if timeout and (not isinstance(timeout, int) or timeout < 100):
            return False
        
        return True

    def get_command(self, target: str, parameters: Dict[str, Any] = None) -> str:
        """Build rustscan command"""
        if not parameters:
            parameters = {}
        
        cmd_parts = ["rustscan"]
        
        # Add ulimit
        ulimit = parameters.get("ulimit", 5000)
        cmd_parts.extend(["--ulimit", str(ulimit)])
        
        # Add batch size
        batch_size = parameters.get("batch_size")
        if batch_size:
            cmd_parts.extend(["-b", str(batch_size)])
        
        # Add timeout
        timeout = parameters.get("timeout")
        if timeout:
            cmd_parts.extend(["-t", str(timeout)])
        
        # Add port range
        ports = parameters.get("ports")
        if ports:
            cmd_parts.extend(["-p", str(ports)])
        
        # Add range (for multiple IPs)
        ip_range = parameters.get("range")
        if ip_range:
            cmd_parts.extend(["-r", str(ip_range)])
        
        # Add scripts (nmap integration)
        if parameters.get("scripts", False):
            cmd_parts.append("--scripts")
        
        # Add accessible flag
        if parameters.get("accessible", False):
            cmd_parts.append("-a")
        
        # Add greppable output
        if parameters.get("greppable", False):
            cmd_parts.append("-g")
        
        # Add additional arguments
        additional_args = parameters.get("additional_args")
        if additional_args:
            cmd_parts.extend(shlex.split(additional_args))
        
        # Add target
        cmd_parts.append(shlex.quote(target))
        
        return " ".join(cmd_parts)

    def get_capabilities(self) -> List[str]:
        """Get rustscan capabilities"""
        return [
            "fast_port_scanning",
            "nmap_integration",
            "adaptive_learning",
            "custom_port_ranges",
            "batch_scanning"
        ]

    def get_supported_targets(self) -> List[str]:
        """Get supported target types"""
        return ["ip", "domain", "cidr", "ip_range"]

    def get_default_parameters(self) -> Dict[str, Any]:
        """Get default rustscan parameters"""
        return {
            "ulimit": 5000,
            "batch_size": 4500,
            "timeout": 1500,
            "ports": "1-65535",
            "scripts": False
        }

    def get_parameter_schema(self) -> Dict[str, Any]:
        """Get parameter schema for validation"""
        return {
            "type": "object",
            "properties": {
                "ulimit": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 65535,
                    "description": "Amount of sockets to open"
                },
                "batch_size": {
                    "type": "integer",
                    "minimum": 1,
                    "description": "Batch size for port scanning"
                },
                "timeout": {
                    "type": "integer",
                    "minimum": 100,
                    "description": "Socket timeout in milliseconds"
                },
                "ports": {
                    "type": "string",
                    "description": "Port range to scan (e.g., 1-1000, 80,443)"
                },
                "range": {
                    "type": "string", 
                    "description": "CIDR range for multiple IPs"
                },
                "scripts": {
                    "type": "boolean",
                    "description": "Enable nmap script integration"
                },
                "accessible": {
                    "type": "boolean",
                    "description": "Accessible mode for screen readers"
                },
                "greppable": {
                    "type": "boolean",
                    "description": "Greppable output format"
                },
                "additional_args": {
                    "type": "string",
                    "description": "Additional rustscan arguments"
                }
            }
        }

    def _parse_rustscan_output(self, output: str) -> Dict[str, Any]:
        """Parse rustscan output into structured data"""
        parsed = {
            "scan_info": {},
            "open_ports": [],
            "host": "",
            "scan_time": 0,
            "ports_scanned": 0
        }
        
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Extract host information
            if "Scanning" in line and "ports" in line:
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == "Scanning":
                        if i + 1 < len(parts):
                            parsed["host"] = parts[i + 1]
                        break
            
            # Extract open ports
            elif "Open" in line and ":" in line:
                # Format: "Open 192.168.1.1:22"
                parts = line.split(":")
                if len(parts) >= 2:
                    port = parts[-1].strip()
                    if port.isdigit():
                        parsed["open_ports"].append(int(port))
            
            # Extract scan statistics
            elif "Nmap done:" in line:
                # This appears when nmap integration is used
                parsed["scan_info"]["nmap_integration"] = True
            
            elif "scanned in" in line:
                # Extract scan time
                parts = line.split()
                for i, part in enumerate(parts):
                    if "scanned" in part and i + 2 < len(parts):
                        try:
                            scan_time = float(parts[i + 2].replace("s", ""))
                            parsed["scan_time"] = scan_time
                        except:
                            pass
        
        # Sort ports
        parsed["open_ports"].sort()
        parsed["ports_scanned"] = len(parsed["open_ports"])
        
        return parsed

    def is_available(self) -> bool:
        """Check if rustscan is available"""
        try:
            import subprocess
            result = subprocess.run(["rustscan", "--version"], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            return result.returncode == 0
        except:
            return False

    def get_version(self) -> str:
        """Get rustscan version"""
        try:
            import subprocess
            result = subprocess.run(["rustscan", "--version"], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            if result.returncode == 0:
                # Extract version from output
                output = result.stdout.strip()
                if "rustscan" in output.lower():
                    parts = output.split()
                    for part in parts:
                        if part.replace(".", "").replace("-", "").isalnum():
                            return part
            return "unknown"
        except:
            return "unknown"