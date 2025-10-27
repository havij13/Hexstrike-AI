"""
Gobuster Tool

Directory and file brute-forcing tool.
"""

import asyncio
import shlex
from typing import Dict, Any, List
from ..base_tool import BaseTool, ToolResult, ToolStatus


class GobusterTool(BaseTool):
    """Gobuster directory and file brute-forcing tool"""

    def __init__(self, name: str = "gobuster", category: str = "web", config: Dict[str, Any] = None):
        super().__init__(name, category, config)

    async def execute(self, target: str, parameters: Dict[str, Any] = None) -> ToolResult:
        """Execute gobuster scan"""
        start_time = asyncio.get_event_loop().time()
        self.set_status(ToolStatus.RUNNING)
        
        try:
            if not parameters:
                parameters = {}
            
            # Build gobuster command
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
                parsed_data = self._parse_gobuster_output(raw_output)
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
        """Validate gobuster parameters"""
        if not parameters:
            return True
        
        # Validate threads
        threads = parameters.get("threads")
        if threads and (not isinstance(threads, int) or threads < 1 or threads > 100):
            return False
        
        # Validate timeout
        timeout = parameters.get("timeout")
        if timeout and (not isinstance(timeout, int) or timeout < 1):
            return False
        
        return True

    def get_command(self, target: str, parameters: Dict[str, Any] = None) -> str:
        """Build gobuster command"""
        if not parameters:
            parameters = {}
        
        cmd_parts = ["gobuster"]
        
        # Add mode
        mode = parameters.get("mode", "dir")
        cmd_parts.append(mode)
        
        # Add URL
        cmd_parts.extend(["-u", shlex.quote(target)])
        
        # Add wordlist
        wordlist = parameters.get("wordlist", "/usr/share/wordlists/dirb/common.txt")
        cmd_parts.extend(["-w", wordlist])
        
        # Add threads
        threads = parameters.get("threads", 10)
        cmd_parts.extend(["-t", str(threads)])
        
        # Add timeout
        timeout = parameters.get("timeout")
        if timeout:
            cmd_parts.extend(["--timeout", f"{timeout}s"])
        
        # Add extensions
        extensions = parameters.get("extensions")
        if extensions:
            cmd_parts.extend(["-x", extensions])
        
        # Add status codes
        status_codes = parameters.get("status_codes")
        if status_codes:
            cmd_parts.extend(["-s", status_codes])
        
        # Add negative status codes
        negative_status_codes = parameters.get("negative_status_codes")
        if negative_status_codes:
            cmd_parts.extend(["-b", negative_status_codes])
        
        # Add user agent
        user_agent = parameters.get("user_agent")
        if user_agent:
            cmd_parts.extend(["-a", shlex.quote(user_agent)])
        
        # Add cookies
        cookies = parameters.get("cookies")
        if cookies:
            cmd_parts.extend(["-c", shlex.quote(cookies)])
        
        # Add headers
        headers = parameters.get("headers")
        if headers:
            if isinstance(headers, list):
                for header in headers:
                    cmd_parts.extend(["-H", shlex.quote(header)])
            else:
                cmd_parts.extend(["-H", shlex.quote(headers)])
        
        # Add proxy
        proxy = parameters.get("proxy")
        if proxy:
            cmd_parts.extend(["-p", proxy])
        
        # Add follow redirects
        if parameters.get("follow_redirects", False):
            cmd_parts.append("-r")
        
        # Add expanded mode
        if parameters.get("expanded", False):
            cmd_parts.append("-e")
        
        # Add no status
        if parameters.get("no_status", False):
            cmd_parts.append("-q")
        
        # Add no error
        if parameters.get("no_error", False):
            cmd_parts.append("-z")
        
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
        """Get gobuster capabilities"""
        return [
            "directory_bruteforce",
            "file_bruteforce",
            "dns_bruteforce",
            "vhost_bruteforce",
            "s3_bucket_bruteforce",
            "custom_wordlists",
            "status_code_filtering"
        ]

    def get_supported_targets(self) -> List[str]:
        """Get supported target types"""
        return ["url", "domain"]

    def get_default_parameters(self) -> Dict[str, Any]:
        """Get default gobuster parameters"""
        return {
            "mode": "dir",
            "wordlist": "/usr/share/wordlists/dirb/common.txt",
            "threads": 10,
            "timeout": 10,
            "status_codes": "200,204,301,302,307,401,403",
            "extensions": "php,html,txt,js"
        }

    def get_parameter_schema(self) -> Dict[str, Any]:
        """Get parameter schema for validation"""
        return {
            "type": "object",
            "properties": {
                "mode": {
                    "type": "string",
                    "enum": ["dir", "dns", "vhost", "s3"],
                    "description": "Gobuster mode"
                },
                "wordlist": {
                    "type": "string",
                    "description": "Path to wordlist file"
                },
                "threads": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100,
                    "description": "Number of concurrent threads"
                },
                "timeout": {
                    "type": "integer",
                    "minimum": 1,
                    "description": "HTTP timeout in seconds"
                },
                "extensions": {
                    "type": "string",
                    "description": "File extensions to search for"
                },
                "status_codes": {
                    "type": "string",
                    "description": "Positive status codes"
                },
                "negative_status_codes": {
                    "type": "string",
                    "description": "Negative status codes to filter out"
                },
                "user_agent": {
                    "type": "string",
                    "description": "User agent string"
                },
                "cookies": {
                    "type": "string",
                    "description": "Cookies to use"
                },
                "headers": {
                    "oneOf": [
                        {"type": "string"},
                        {"type": "array", "items": {"type": "string"}}
                    ],
                    "description": "HTTP headers to include"
                },
                "proxy": {
                    "type": "string",
                    "description": "Proxy URL"
                },
                "follow_redirects": {
                    "type": "boolean",
                    "description": "Follow redirects"
                },
                "expanded": {
                    "type": "boolean",
                    "description": "Expanded mode"
                },
                "no_status": {
                    "type": "boolean",
                    "description": "Don't print status codes"
                },
                "no_error": {
                    "type": "boolean",
                    "description": "Don't display errors"
                },
                "output_file": {
                    "type": "string",
                    "description": "Output file path"
                },
                "additional_args": {
                    "type": "string",
                    "description": "Additional gobuster arguments"
                }
            }
        }

    def _parse_gobuster_output(self, output: str) -> Dict[str, Any]:
        """Parse gobuster output into structured data"""
        parsed = {
            "scan_info": {},
            "found_paths": [],
            "statistics": {}
        }
        
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Parse found paths
            if line.startswith('/') or line.startswith('http'):
                # Format varies by mode, but typically: /path (Status: 200) [Size: 1234]
                parts = line.split()
                if len(parts) >= 1:
                    path = parts[0]
                    
                    # Extract status code
                    status_code = None
                    size = None
                    
                    for part in parts:
                        if part.startswith('(Status:') and part.endswith(')'):
                            status_code = part.replace('(Status:', '').replace(')', '')
                        elif part.startswith('[Size:') and part.endswith(']'):
                            size = part.replace('[Size:', '').replace(']', '')
                    
                    path_info = {
                        "path": path,
                        "status_code": status_code,
                        "size": size
                    }
                    
                    parsed["found_paths"].append(path_info)
            
            # Parse scan information
            elif "Gobuster" in line and "by OJ Reeves" in line:
                parsed["scan_info"]["version"] = line
            
            elif "Mode:" in line:
                parsed["scan_info"]["mode"] = line.split("Mode:")[1].strip()
            
            elif "URL/Domain:" in line:
                parsed["scan_info"]["target"] = line.split("URL/Domain:")[1].strip()
            
            elif "Threads:" in line:
                parsed["scan_info"]["threads"] = line.split("Threads:")[1].strip()
            
            elif "Wordlist:" in line:
                parsed["scan_info"]["wordlist"] = line.split("Wordlist:")[1].strip()
            
            elif "Status codes:" in line:
                parsed["scan_info"]["status_codes"] = line.split("Status codes:")[1].strip()
            
            elif "Timeout:" in line:
                parsed["scan_info"]["timeout"] = line.split("Timeout:")[1].strip()
            
            # Parse completion message
            elif "Finished" in line:
                parsed["statistics"]["completion"] = line
        
        # Sort found paths
        parsed["found_paths"].sort(key=lambda x: x["path"])
        parsed["statistics"]["total_found"] = len(parsed["found_paths"])
        
        return parsed

    def is_available(self) -> bool:
        """Check if gobuster is available"""
        try:
            import subprocess
            result = subprocess.run(["gobuster", "version"], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            return result.returncode == 0
        except:
            return False

    def get_version(self) -> str:
        """Get gobuster version"""
        try:
            import subprocess
            result = subprocess.run(["gobuster", "version"], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            if result.returncode == 0:
                output = result.stdout.strip()
                if "Gobuster" in output:
                    parts = output.split()
                    for i, part in enumerate(parts):
                        if part == "Gobuster" and i + 1 < len(parts):
                            return parts[i + 1]
            return "unknown"
        except:
            return "unknown"