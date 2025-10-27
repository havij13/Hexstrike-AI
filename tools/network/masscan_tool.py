"""
Masscan Tool

High-speed port scanner.
"""

import asyncio
import json
import shlex
from typing import Dict, Any, List
from ..base_tool import BaseTool, ToolResult, ToolStatus


class MasscanTool(BaseTool):
    """Masscan high-speed port scanner"""

    def __init__(self, name: str = "masscan", category: str = "network", config: Dict[str, Any] = None):
        super().__init__(name, category, config)

    async def execute(self, target: str, parameters: Dict[str, Any] = None) -> ToolResult:
        """Execute masscan"""
        start_time = asyncio.get_event_loop().time()
        self.set_status(ToolStatus.RUNNING)
        
        try:
            if not parameters:
                parameters = {}
            
            # Build masscan command
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
                parsed_data = self._parse_masscan_output(raw_output)
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
        """Validate masscan parameters"""
        if not parameters:
            return True
        
        # Validate rate
        rate = parameters.get("rate")
        if rate and (not isinstance(rate, int) or rate < 1 or rate > 100000):
            return False
        
        # Validate max rate
        max_rate = parameters.get("max_rate")
        if max_rate and (not isinstance(max_rate, int) or max_rate < 1):
            return False
        
        return True

    def get_command(self, target: str, parameters: Dict[str, Any] = None) -> str:
        """Build masscan command"""
        if not parameters:
            parameters = {}
        
        cmd_parts = ["masscan"]
        
        # Add rate
        rate = parameters.get("rate", 1000)
        cmd_parts.extend(["--rate", str(rate)])
        
        # Add max rate
        max_rate = parameters.get("max_rate")
        if max_rate:
            cmd_parts.extend(["--max-rate", str(max_rate)])
        
        # Add ports
        ports = parameters.get("ports", "1-65535")
        cmd_parts.extend(["-p", str(ports)])
        
        # Add banners
        if parameters.get("banners", False):
            cmd_parts.append("--banners")
        
        # Add source IP
        source_ip = parameters.get("source_ip")
        if source_ip:
            cmd_parts.extend(["-S", source_ip])
        
        # Add source port
        source_port = parameters.get("source_port")
        if source_port:
            cmd_parts.extend(["--source-port", str(source_port)])
        
        # Add interface
        interface = parameters.get("interface")
        if interface:
            cmd_parts.extend(["-e", interface])
        
        # Add router MAC
        router_mac = parameters.get("router_mac")
        if router_mac:
            cmd_parts.extend(["--router-mac", router_mac])
        
        # Add exclude
        exclude = parameters.get("exclude")
        if exclude:
            cmd_parts.extend(["--exclude", exclude])
        
        # Add include file
        include_file = parameters.get("include_file")
        if include_file:
            cmd_parts.extend(["-iL", include_file])
        
        # Add exclude file
        exclude_file = parameters.get("exclude_file")
        if exclude_file:
            cmd_parts.extend(["--excludefile", exclude_file])
        
        # Add output format
        output_format = parameters.get("output_format")
        if output_format == "xml":
            cmd_parts.extend(["-oX", "-"])
        elif output_format == "grepable":
            cmd_parts.extend(["-oG", "-"])
        elif output_format == "json":
            cmd_parts.extend(["-oJ", "-"])
        elif output_format == "list":
            cmd_parts.extend(["-oL", "-"])
        
        # Add additional arguments
        additional_args = parameters.get("additional_args")
        if additional_args:
            cmd_parts.extend(shlex.split(additional_args))
        
        # Add target
        cmd_parts.append(shlex.quote(target))
        
        return " ".join(cmd_parts)

    def get_capabilities(self) -> List[str]:
        """Get masscan capabilities"""
        return [
            "high_speed_scanning",
            "banner_grabbing",
            "large_scale_scanning",
            "custom_source_ip",
            "rate_limiting",
            "exclude_ranges"
        ]

    def get_supported_targets(self) -> List[str]:
        """Get supported target types"""
        return ["ip", "domain", "cidr", "ip_range"]

    def get_default_parameters(self) -> Dict[str, Any]:
        """Get default masscan parameters"""
        return {
            "rate": 1000,
            "ports": "1-65535",
            "banners": False,
            "output_format": "list"
        }

    def get_parameter_schema(self) -> Dict[str, Any]:
        """Get parameter schema for validation"""
        return {
            "type": "object",
            "properties": {
                "rate": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100000,
                    "description": "Packets per second rate"
                },
                "max_rate": {
                    "type": "integer",
                    "minimum": 1,
                    "description": "Maximum packets per second"
                },
                "ports": {
                    "type": "string",
                    "description": "Port range to scan (e.g., 1-1000, 80,443)"
                },
                "banners": {
                    "type": "boolean",
                    "description": "Enable banner grabbing"
                },
                "source_ip": {
                    "type": "string",
                    "description": "Source IP address"
                },
                "source_port": {
                    "type": "integer",
                    "description": "Source port number"
                },
                "interface": {
                    "type": "string",
                    "description": "Network interface to use"
                },
                "router_mac": {
                    "type": "string",
                    "description": "Router MAC address"
                },
                "exclude": {
                    "type": "string",
                    "description": "IP ranges to exclude"
                },
                "include_file": {
                    "type": "string",
                    "description": "File containing target IPs"
                },
                "exclude_file": {
                    "type": "string",
                    "description": "File containing IPs to exclude"
                },
                "output_format": {
                    "type": "string",
                    "enum": ["list", "xml", "grepable", "json"],
                    "description": "Output format"
                },
                "additional_args": {
                    "type": "string",
                    "description": "Additional masscan arguments"
                }
            }
        }

    def _parse_masscan_output(self, output: str) -> Dict[str, Any]:
        """Parse masscan output into structured data"""
        parsed = {
            "scan_info": {},
            "open_ports": [],
            "banners": {},
            "scan_stats": {}
        }
        
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Parse discovered ports
            if line.startswith("Discovered open port"):
                # Format: "Discovered open port 80/tcp on 192.168.1.1"
                parts = line.split()
                if len(parts) >= 6:
                    port_proto = parts[3]  # "80/tcp"
                    ip = parts[5]
                    
                    if "/" in port_proto:
                        port, protocol = port_proto.split("/")
                        parsed["open_ports"].append({
                            "ip": ip,
                            "port": int(port),
                            "protocol": protocol,
                            "state": "open"
                        })
            
            # Parse banner information
            elif line.startswith("Banner on port"):
                # Format: "Banner on port 80/tcp on 192.168.1.1: [banner data]"
                parts = line.split(": ", 1)
                if len(parts) == 2:
                    header = parts[0]
                    banner = parts[1]
                    
                    # Extract port and IP from header
                    header_parts = header.split()
                    if len(header_parts) >= 6:
                        port_proto = header_parts[3]
                        ip = header_parts[5]
                        
                        key = f"{ip}:{port_proto}"
                        parsed["banners"][key] = banner
            
            # Parse scan statistics
            elif "rate:" in line:
                # Extract rate information
                if "rate:" in line:
                    rate_part = line.split("rate:")[1].strip()
                    parsed["scan_stats"]["rate"] = rate_part
            
            elif "Scanning" in line and "hosts" in line:
                # Extract scan info
                parsed["scan_info"]["scan_line"] = line
        
        # Sort ports by IP and port number
        parsed["open_ports"].sort(key=lambda x: (x["ip"], x["port"]))
        
        return parsed

    def is_available(self) -> bool:
        """Check if masscan is available"""
        try:
            import subprocess
            result = subprocess.run(["masscan", "--version"], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            return result.returncode == 0
        except:
            return False

    def get_version(self) -> str:
        """Get masscan version"""
        try:
            import subprocess
            result = subprocess.run(["masscan", "--version"], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if "Masscan version" in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            return parts[2]
            return "unknown"
        except:
            return "unknown"