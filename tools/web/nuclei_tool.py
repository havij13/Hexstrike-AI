"""
Nuclei Tool

Fast and customizable vulnerability scanner.
"""

import asyncio
import json
import shlex
from typing import Dict, Any, List
from ..base_tool import BaseTool, ToolResult, ToolStatus


class NucleiTool(BaseTool):
    """Nuclei fast and customizable vulnerability scanner"""

    def __init__(self, name: str = "nuclei", category: str = "web", config: Dict[str, Any] = None):
        super().__init__(name, category, config)

    async def execute(self, target: str, parameters: Dict[str, Any] = None) -> ToolResult:
        """Execute nuclei scan"""
        start_time = asyncio.get_event_loop().time()
        self.set_status(ToolStatus.RUNNING)
        
        try:
            if not parameters:
                parameters = {}
            
            # Build nuclei command
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
                parsed_data = self._parse_nuclei_output(raw_output, parameters.get("output_format", "default"))
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
        """Validate nuclei parameters"""
        if not parameters:
            return True
        
        # Validate concurrency
        concurrency = parameters.get("concurrency")
        if concurrency and (not isinstance(concurrency, int) or concurrency < 1 or concurrency > 100):
            return False
        
        # Validate rate limit
        rate_limit = parameters.get("rate_limit")
        if rate_limit and (not isinstance(rate_limit, int) or rate_limit < 1):
            return False
        
        return True

    def get_command(self, target: str, parameters: Dict[str, Any] = None) -> str:
        """Build nuclei command"""
        if not parameters:
            parameters = {}
        
        cmd_parts = ["nuclei"]
        
        # Add target
        if target.startswith(('http://', 'https://')):
            cmd_parts.extend(["-u", shlex.quote(target)])
        else:
            # Assume it's a list of targets or a file
            cmd_parts.extend(["-l", shlex.quote(target)])
        
        # Add templates
        templates = parameters.get("templates")
        if templates:
            cmd_parts.extend(["-t", templates])
        
        # Add tags
        tags = parameters.get("tags")
        if tags:
            cmd_parts.extend(["-tags", tags])
        
        # Add severity
        severity = parameters.get("severity")
        if severity:
            cmd_parts.extend(["-severity", severity])
        
        # Add exclude tags
        exclude_tags = parameters.get("exclude_tags")
        if exclude_tags:
            cmd_parts.extend(["-exclude-tags", exclude_tags])
        
        # Add exclude templates
        exclude_templates = parameters.get("exclude_templates")
        if exclude_templates:
            cmd_parts.extend(["-exclude-templates", exclude_templates])
        
        # Add concurrency
        concurrency = parameters.get("concurrency", 25)
        cmd_parts.extend(["-c", str(concurrency)])
        
        # Add rate limit
        rate_limit = parameters.get("rate_limit")
        if rate_limit:
            cmd_parts.extend(["-rl", str(rate_limit)])
        
        # Add timeout
        timeout = parameters.get("timeout")
        if timeout:
            cmd_parts.extend(["-timeout", str(timeout)])
        
        # Add retries
        retries = parameters.get("retries")
        if retries:
            cmd_parts.extend(["-retries", str(retries)])
        
        # Add proxy
        proxy = parameters.get("proxy")
        if proxy:
            cmd_parts.extend(["-proxy", proxy])
        
        # Add headers
        headers = parameters.get("headers")
        if headers:
            if isinstance(headers, list):
                for header in headers:
                    cmd_parts.extend(["-H", shlex.quote(header)])
            else:
                cmd_parts.extend(["-H", shlex.quote(headers)])
        
        # Add cookies
        cookies = parameters.get("cookies")
        if cookies:
            cmd_parts.extend(["-cookie", shlex.quote(cookies)])
        
        # Add user agent
        user_agent = parameters.get("user_agent")
        if user_agent:
            cmd_parts.extend(["-H", f"User-Agent: {shlex.quote(user_agent)}"])
        
        # Add follow redirects
        if parameters.get("follow_redirects", True):
            cmd_parts.append("-fr")
        
        # Add update templates
        if parameters.get("update", False):
            cmd_parts.append("-update-templates")
        
        # Add silent mode
        if parameters.get("silent", False):
            cmd_parts.append("-silent")
        
        # Add verbose mode
        if parameters.get("verbose", False):
            cmd_parts.append("-v")
        
        # Add debug mode
        if parameters.get("debug", False):
            cmd_parts.append("-debug")
        
        # Add output format
        output_format = parameters.get("output_format")
        if output_format == "json":
            cmd_parts.append("-json")
        elif output_format == "jsonl":
            cmd_parts.append("-jsonl")
        
        # Add output file
        output_file = parameters.get("output_file")
        if output_file:
            cmd_parts.extend(["-o", output_file])
        
        # Add additional arguments
        additional_args = parameters.get("additional_args")
        if additional_args:
            cmd_parts.extend(shlex.split(additional_args))
        
        return " ".join(cmd_parts)

    def get_capabilities(self) -> List[str]:
        """Get nuclei capabilities"""
        return [
            "vulnerability_scanning",
            "template_based_scanning",
            "custom_templates",
            "severity_filtering",
            "tag_based_filtering",
            "concurrent_scanning",
            "rate_limiting",
            "proxy_support"
        ]

    def get_supported_targets(self) -> List[str]:
        """Get supported target types"""
        return ["url", "domain", "ip", "file"]

    def get_default_parameters(self) -> Dict[str, Any]:
        """Get default nuclei parameters"""
        return {
            "concurrency": 25,
            "severity": "critical,high,medium",
            "follow_redirects": True,
            "timeout": 5,
            "retries": 1,
            "output_format": "default"
        }

    def get_parameter_schema(self) -> Dict[str, Any]:
        """Get parameter schema for validation"""
        return {
            "type": "object",
            "properties": {
                "templates": {
                    "type": "string",
                    "description": "Template or template directory to run"
                },
                "tags": {
                    "type": "string",
                    "description": "Tags to run templates for"
                },
                "severity": {
                    "type": "string",
                    "description": "Severity levels to run (critical,high,medium,low,info)"
                },
                "exclude_tags": {
                    "type": "string",
                    "description": "Tags to exclude"
                },
                "exclude_templates": {
                    "type": "string",
                    "description": "Templates to exclude"
                },
                "concurrency": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100,
                    "description": "Maximum number of templates executed in parallel"
                },
                "rate_limit": {
                    "type": "integer",
                    "minimum": 1,
                    "description": "Maximum requests per second"
                },
                "timeout": {
                    "type": "integer",
                    "minimum": 1,
                    "description": "Timeout in seconds"
                },
                "retries": {
                    "type": "integer",
                    "minimum": 0,
                    "description": "Number of retries for failed requests"
                },
                "proxy": {
                    "type": "string",
                    "description": "Proxy URL"
                },
                "headers": {
                    "oneOf": [
                        {"type": "string"},
                        {"type": "array", "items": {"type": "string"}}
                    ],
                    "description": "HTTP headers to include"
                },
                "cookies": {
                    "type": "string",
                    "description": "Cookies to use"
                },
                "user_agent": {
                    "type": "string",
                    "description": "User agent string"
                },
                "follow_redirects": {
                    "type": "boolean",
                    "description": "Follow HTTP redirects"
                },
                "update": {
                    "type": "boolean",
                    "description": "Update templates before scanning"
                },
                "silent": {
                    "type": "boolean",
                    "description": "Silent mode"
                },
                "verbose": {
                    "type": "boolean",
                    "description": "Verbose mode"
                },
                "debug": {
                    "type": "boolean",
                    "description": "Debug mode"
                },
                "output_format": {
                    "type": "string",
                    "enum": ["default", "json", "jsonl"],
                    "description": "Output format"
                },
                "output_file": {
                    "type": "string",
                    "description": "Output file path"
                },
                "additional_args": {
                    "type": "string",
                    "description": "Additional nuclei arguments"
                }
            }
        }

    def _parse_nuclei_output(self, output: str, output_format: str = "default") -> Dict[str, Any]:
        """Parse nuclei output into structured data"""
        parsed = {
            "scan_info": {},
            "vulnerabilities": [],
            "statistics": {}
        }
        
        if output_format == "json" or output_format == "jsonl":
            # Parse JSON output
            lines = output.strip().split('\n')
            for line in lines:
                if line.strip():
                    try:
                        vuln_data = json.loads(line)
                        parsed["vulnerabilities"].append(vuln_data)
                    except json.JSONDecodeError:
                        continue
        else:
            # Parse default text output
            lines = output.split('\n')
            
            for line in lines:
                line = line.strip()
                
                # Parse vulnerability findings
                if '[' in line and ']' in line and ('http://' in line or 'https://' in line):
                    # Format: [severity] [template-id] url [additional-info]
                    parts = line.split(']', 2)
                    if len(parts) >= 3:
                        severity = parts[0].replace('[', '').strip()
                        template_id = parts[1].replace('[', '').strip()
                        rest = parts[2].strip()
                        
                        # Extract URL
                        url_parts = rest.split()
                        url = url_parts[0] if url_parts else ""
                        
                        vuln_info = {
                            "severity": severity,
                            "template_id": template_id,
                            "url": url,
                            "info": rest
                        }
                        
                        parsed["vulnerabilities"].append(vuln_info)
                
                # Parse scan statistics
                elif "Templates loaded:" in line:
                    parsed["scan_info"]["templates_loaded"] = line.split(":")[-1].strip()
                
                elif "Targets loaded:" in line:
                    parsed["scan_info"]["targets_loaded"] = line.split(":")[-1].strip()
                
                elif "Templates executed:" in line:
                    parsed["statistics"]["templates_executed"] = line.split(":")[-1].strip()
                
                elif "Requests executed:" in line:
                    parsed["statistics"]["requests_executed"] = line.split(":")[-1].strip()
        
        # Calculate statistics
        parsed["statistics"]["total_vulnerabilities"] = len(parsed["vulnerabilities"])
        
        # Group by severity
        severity_counts = {}
        for vuln in parsed["vulnerabilities"]:
            severity = vuln.get("severity", "unknown")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        parsed["statistics"]["severity_distribution"] = severity_counts
        
        return parsed

    def is_available(self) -> bool:
        """Check if nuclei is available"""
        try:
            import subprocess
            result = subprocess.run(["nuclei", "-version"], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            return result.returncode == 0
        except:
            return False

    def get_version(self) -> str:
        """Get nuclei version"""
        try:
            import subprocess
            result = subprocess.run(["nuclei", "-version"], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            if result.returncode == 0:
                output = result.stdout.strip()
                # Extract version from output
                lines = output.split('\n')
                for line in lines:
                    if 'nuclei' in line.lower() and any(char.isdigit() for char in line):
                        parts = line.split()
                        for part in parts:
                            if any(char.isdigit() for char in part) and '.' in part:
                                return part
            return "unknown"
        except:
            return "unknown"