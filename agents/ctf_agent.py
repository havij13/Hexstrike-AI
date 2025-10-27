"""
CTF Workflow Manager

This module provides specialized workflow management for CTF competitions.
"""

import time
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent, AgentResult, AgentStatus


@dataclass
class CTFChallenge:
    """CTF challenge information"""
    name: str
    category: str  # web, crypto, pwn, forensics, rev, misc, osint
    description: str
    points: int = 0
    difficulty: str = "unknown"  # easy, medium, hard, insane
    files: List[str] = field(default_factory=list)
    url: str = ""
    hints: List[str] = field(default_factory=list)


class CTFWorkflowManager(BaseAgent):
    """Specialized workflow manager for CTF competitions"""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("CTFWorkflowManager", config)
        
        self.category_tools = {
            "web": {
                "reconnaissance": ["httpx", "katana", "gau", "waybackurls"],
                "vulnerability_scanning": ["nuclei", "dalfox", "sqlmap", "nikto"],
                "content_discovery": ["gobuster", "dirsearch", "feroxbuster"],
                "parameter_testing": ["arjun", "paramspider", "x8"],
                "specialized": ["wpscan", "joomscan", "droopescan"]
            },
            "crypto": {
                "hash_analysis": ["hashcat", "john", "hash-identifier"],
                "cipher_analysis": ["cipher-identifier", "cryptool", "cyberchef"],
                "rsa_attacks": ["rsatool", "factordb", "yafu"],
                "frequency_analysis": ["frequency-analysis", "substitution-solver"],
                "modern_crypto": ["sage", "pycrypto", "cryptography"]
            },
            "pwn": {
                "binary_analysis": ["checksec", "ghidra", "radare2", "gdb-peda"],
                "exploit_development": ["pwntools", "ropper", "one-gadget"],
                "heap_exploitation": ["glibc-heap-analysis", "heap-viewer"],
                "format_string": ["format-string-exploiter"],
                "rop_chains": ["ropgadget", "ropper", "angr"]
            },
            "forensics": {
                "file_analysis": ["file", "binwalk", "foremost", "photorec"],
                "image_forensics": ["exiftool", "steghide", "stegsolve", "zsteg"],
                "memory_forensics": ["volatility", "rekall"],
                "network_forensics": ["wireshark", "tcpdump", "networkminer"],
                "disk_forensics": ["autopsy", "sleuthkit", "testdisk"]
            },
            "rev": {
                "disassemblers": ["ghidra", "ida", "radare2", "binary-ninja"],
                "debuggers": ["gdb", "x64dbg", "ollydbg"],
                "decompilers": ["ghidra", "hex-rays", "retdec"],
                "packers": ["upx", "peid", "detect-it-easy"],
                "analysis": ["strings", "ltrace", "strace", "objdump"]
            },
            "misc": {
                "encoding": ["base64", "hex", "url-decode", "rot13"],
                "compression": ["zip", "tar", "gzip", "7zip"],
                "qr_codes": ["qr-decoder", "zbar"],
                "audio_analysis": ["audacity", "sonic-visualizer"],
                "esoteric": ["brainfuck", "whitespace", "piet"]
            },
            "osint": {
                "search_engines": ["google-dorking", "shodan", "censys"],
                "social_media": ["sherlock", "social-analyzer"],
                "image_analysis": ["reverse-image-search", "exif-analysis"],
                "domain_analysis": ["whois", "dns-analysis", "certificate-transparency"],
                "geolocation": ["geoint", "osm-analysis", "satellite-imagery"]
            }
        }

        self.solving_strategies = {
            "web": [
                {"strategy": "source_code_analysis", "description": "Analyze HTML/JS source for hidden information"},
                {"strategy": "directory_traversal", "description": "Test for path traversal vulnerabilities"},
                {"strategy": "sql_injection", "description": "Test for SQL injection in all parameters"},
                {"strategy": "xss_exploitation", "description": "Test for XSS and exploit for admin access"},
                {"strategy": "authentication_bypass", "description": "Test for auth bypass techniques"},
                {"strategy": "session_manipulation", "description": "Analyze and manipulate session tokens"},
                {"strategy": "file_upload_bypass", "description": "Test file upload restrictions and bypasses"}
            ],
            "crypto": [
                {"strategy": "frequency_analysis", "description": "Perform frequency analysis for substitution ciphers"},
                {"strategy": "known_plaintext", "description": "Use known plaintext attacks"},
                {"strategy": "weak_keys", "description": "Test for weak cryptographic keys"},
                {"strategy": "implementation_flaws", "description": "Look for implementation vulnerabilities"},
                {"strategy": "side_channel", "description": "Exploit timing or other side channels"},
                {"strategy": "mathematical_attacks", "description": "Use mathematical properties to break crypto"}
            ],
            "pwn": [
                {"strategy": "buffer_overflow", "description": "Exploit buffer overflow vulnerabilities"},
                {"strategy": "format_string", "description": "Exploit format string vulnerabilities"},
                {"strategy": "rop_chains", "description": "Build ROP chains for exploitation"},
                {"strategy": "heap_exploitation", "description": "Exploit heap-based vulnerabilities"},
                {"strategy": "race_conditions", "description": "Exploit race condition vulnerabilities"},
                {"strategy": "integer_overflow", "description": "Exploit integer overflow conditions"}
            ],
            "forensics": [
                {"strategy": "file_carving", "description": "Recover deleted or hidden files"},
                {"strategy": "metadata_analysis", "description": "Analyze file metadata for hidden information"},
                {"strategy": "steganography", "description": "Extract hidden data from images/audio"},
                {"strategy": "memory_analysis", "description": "Analyze memory dumps for artifacts"},
                {"strategy": "network_analysis", "description": "Analyze network traffic for suspicious activity"},
                {"strategy": "timeline_analysis", "description": "Reconstruct timeline of events"}
            ],
            "rev": [
                {"strategy": "static_analysis", "description": "Analyze binary without execution"},
                {"strategy": "dynamic_analysis", "description": "Analyze binary during execution"},
                {"strategy": "anti_debugging", "description": "Bypass anti-debugging techniques"},
                {"strategy": "unpacking", "description": "Unpack packed/obfuscated binaries"},
                {"strategy": "algorithm_recovery", "description": "Reverse engineer algorithms"},
                {"strategy": "key_recovery", "description": "Extract encryption keys from binaries"}
            ]
        }

    async def execute(self, target: str, parameters: Dict[str, Any] = None) -> AgentResult:
        """Execute CTF workflow"""
        start_time = time.time()
        self.set_status(AgentStatus.RUNNING)
        
        try:
            if not parameters:
                parameters = {}
            
            # Create CTF challenge object
            challenge = CTFChallenge(
                name=parameters.get("challenge_name", target),
                category=parameters.get("category", "web"),
                description=parameters.get("description", ""),
                points=parameters.get("points", 0),
                difficulty=parameters.get("difficulty", "unknown"),
                files=parameters.get("files", []),
                url=target if target.startswith(('http://', 'https://')) else "",
                hints=parameters.get("hints", [])
            )
            
            workflow_type = parameters.get("workflow_type", "challenge")
            
            if workflow_type == "challenge":
                result_data = self.create_ctf_challenge_workflow(challenge)
            elif workflow_type == "team_strategy":
                challenges = parameters.get("challenges", [challenge])
                team_size = parameters.get("team_size", 4)
                result_data = self.create_ctf_team_strategy(challenges, team_size)
            else:
                result_data = self.create_ctf_challenge_workflow(challenge)
            
            execution_time = time.time() - start_time
            self.set_status(AgentStatus.COMPLETED)
            
            result = AgentResult(
                success=True,
                data=result_data,
                message=f"CTF {workflow_type} workflow created successfully",
                status=AgentStatus.COMPLETED,
                execution_time=execution_time
            )
            
            self.add_result(result)
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.set_status(AgentStatus.FAILED)
            
            result = AgentResult(
                success=False,
                data={},
                message=f"CTF workflow creation failed: {str(e)}",
                status=AgentStatus.FAILED,
                execution_time=execution_time,
                errors=[str(e)]
            )
            
            self.add_result(result)
            return result

    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate input parameters"""
        if not parameters:
            return True
        
        valid_categories = ["web", "crypto", "pwn", "forensics", "rev", "misc", "osint"]
        category = parameters.get("category", "web")
        
        valid_difficulties = ["easy", "medium", "hard", "insane", "unknown"]
        difficulty = parameters.get("difficulty", "unknown")
        
        return category in valid_categories and difficulty in valid_difficulties

    def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities"""
        return [
            "ctf_challenge_workflow",
            "ctf_team_strategy",
            "tool_selection",
            "strategy_recommendation",
            "time_estimation"
        ]

    def create_ctf_challenge_workflow(self, challenge: CTFChallenge) -> Dict[str, Any]:
        """Create advanced specialized workflow for CTF challenge"""
        workflow = {
            "challenge": challenge.name,
            "category": challenge.category,
            "difficulty": challenge.difficulty,
            "points": challenge.points,
            "tools": [],
            "strategies": [],
            "estimated_time": 0,
            "success_probability": 0.0,
            "workflow_steps": []
        }

        # Select tools for the challenge
        workflow["tools"] = self._select_tools_for_challenge(challenge)

        # Get category-specific strategies
        if challenge.category in self.solving_strategies:
            workflow["strategies"] = self.solving_strategies[challenge.category]

        # Time estimation
        base_times = {
            "easy": {"min": 15, "avg": 30, "max": 60},
            "medium": {"min": 30, "avg": 60, "max": 120},
            "hard": {"min": 60, "avg": 120, "max": 240},
            "insane": {"min": 120, "avg": 240, "max": 480},
            "unknown": {"min": 45, "avg": 90, "max": 180}
        }

        # Category complexity multipliers
        category_multipliers = {
            "web": 1.0,
            "crypto": 1.3,
            "pwn": 1.5,
            "forensics": 1.2,
            "rev": 1.4,
            "misc": 0.8,
            "osint": 0.9
        }

        base_time = base_times[challenge.difficulty]["avg"]
        category_mult = category_multipliers.get(challenge.category, 1.0)
        
        # Analyze description complexity
        description_complexity = self._analyze_description_complexity(challenge.description)
        complexity_mult = 1.0 + (description_complexity * 0.3)

        workflow["estimated_time"] = int(base_time * category_mult * complexity_mult * 60)  # Convert to seconds

        # Success probability calculation
        base_success = {
            "easy": 0.85,
            "medium": 0.65,
            "hard": 0.45,
            "insane": 0.25,
            "unknown": 0.55
        }[challenge.difficulty]

        # Adjust based on tool availability
        tool_availability_bonus = min(0.15, len(workflow["tools"]) * 0.02)
        workflow["success_probability"] = min(0.95, base_success + tool_availability_bonus)

        # Create workflow steps
        workflow["workflow_steps"] = self._create_category_workflow(challenge)

        return workflow

    def create_ctf_team_strategy(self, challenges: List[CTFChallenge], team_size: int = 4) -> Dict[str, Any]:
        """Create team strategy for CTF competition"""
        strategy = {
            "team_size": team_size,
            "challenge_allocation": {},
            "priority_order": [],
            "estimated_total_time": 0,
            "expected_score": 0
        }

        # Sort challenges by points/time ratio for optimal strategy
        challenge_efficiency = []
        for challenge in challenges:
            workflow = self.create_ctf_challenge_workflow(challenge)
            efficiency = (challenge.points * workflow["success_probability"]) / (workflow["estimated_time"] / 3600)  # points per hour
            challenge_efficiency.append({
                "challenge": challenge,
                "efficiency": efficiency,
                "workflow": workflow
            })

        # Sort by efficiency (highest first)
        challenge_efficiency.sort(key=lambda x: x["efficiency"], reverse=True)

        # Allocate challenges to team members
        team_workload = [0] * team_size
        for i, item in enumerate(challenge_efficiency):
            # Assign to team member with least workload
            team_member = team_workload.index(min(team_workload))

            if team_member not in strategy["challenge_allocation"]:
                strategy["challenge_allocation"][team_member] = []

            strategy["challenge_allocation"][team_member].append({
                "challenge": item["challenge"].name,
                "category": item["challenge"].category,
                "points": item["challenge"].points,
                "estimated_time": item["workflow"]["estimated_time"],
                "success_probability": item["workflow"]["success_probability"]
            })

            team_workload[team_member] += item["workflow"]["estimated_time"]
            strategy["expected_score"] += item["challenge"].points * item["workflow"]["success_probability"]

        strategy["estimated_total_time"] = max(team_workload)
        strategy["priority_order"] = [item["challenge"].name for item in challenge_efficiency]

        return strategy

    def _select_tools_for_challenge(self, challenge: CTFChallenge) -> List[str]:
        """Select appropriate tools based on challenge details"""
        selected_tools = []
        category_tools = self.category_tools.get(challenge.category, {})

        # Always include reconnaissance tools for the category
        if "reconnaissance" in category_tools:
            selected_tools.extend(category_tools["reconnaissance"][:2])  # Top 2 recon tools

        # Add specialized tools based on challenge description
        description_lower = challenge.description.lower()

        if challenge.category == "web":
            if any(keyword in description_lower for keyword in ["sql", "injection", "database"]):
                selected_tools.append("sqlmap")
            if any(keyword in description_lower for keyword in ["xss", "script", "javascript"]):
                selected_tools.append("dalfox")
            if any(keyword in description_lower for keyword in ["wordpress", "wp"]):
                selected_tools.append("wpscan")
            if any(keyword in description_lower for keyword in ["upload", "file"]):
                selected_tools.extend(["gobuster", "feroxbuster"])

        elif challenge.category == "crypto":
            if any(keyword in description_lower for keyword in ["hash", "md5", "sha"]):
                selected_tools.extend(["hashcat", "john"])
            if any(keyword in description_lower for keyword in ["rsa", "public key"]):
                selected_tools.extend(["rsatool", "factordb"])
            if any(keyword in description_lower for keyword in ["cipher", "encrypt"]):
                selected_tools.extend(["cipher-identifier", "cyberchef"])

        elif challenge.category == "pwn":
            selected_tools.extend(["checksec", "ghidra", "pwntools"])
            if any(keyword in description_lower for keyword in ["heap", "malloc"]):
                selected_tools.append("glibc-heap-analysis")
            if any(keyword in description_lower for keyword in ["format", "printf"]):
                selected_tools.append("format-string-exploiter")

        elif challenge.category == "forensics":
            if any(keyword in description_lower for keyword in ["image", "jpg", "png"]):
                selected_tools.extend(["exiftool", "steghide", "stegsolve"])
            if any(keyword in description_lower for keyword in ["memory", "dump"]):
                selected_tools.append("volatility")
            if any(keyword in description_lower for keyword in ["network", "pcap"]):
                selected_tools.extend(["wireshark", "tcpdump"])

        elif challenge.category == "rev":
            selected_tools.extend(["ghidra", "radare2", "strings"])
            if any(keyword in description_lower for keyword in ["packed", "upx"]):
                selected_tools.extend(["upx", "peid"])

        # Remove duplicates while preserving order
        return list(dict.fromkeys(selected_tools))

    def _create_category_workflow(self, challenge: CTFChallenge) -> List[Dict[str, Any]]:
        """Create category-specific workflow steps"""
        workflows = {
            "web": [
                {"step": 1, "action": "reconnaissance", "description": "Analyze target URL and gather information"},
                {"step": 2, "action": "source_analysis", "description": "Examine HTML/JS source code for clues"},
                {"step": 3, "action": "directory_discovery", "description": "Discover hidden directories and files"},
                {"step": 4, "action": "vulnerability_testing", "description": "Test for common web vulnerabilities"},
                {"step": 5, "action": "exploitation", "description": "Exploit discovered vulnerabilities"},
                {"step": 6, "action": "flag_extraction", "description": "Extract flag from compromised system"}
            ],
            "crypto": [
                {"step": 1, "action": "cipher_identification", "description": "Identify the type of cipher or encoding"},
                {"step": 2, "action": "key_analysis", "description": "Analyze key properties and weaknesses"},
                {"step": 3, "action": "attack_selection", "description": "Select appropriate cryptographic attack"},
                {"step": 4, "action": "implementation", "description": "Implement and execute the attack"},
                {"step": 5, "action": "verification", "description": "Verify the decrypted result"},
                {"step": 6, "action": "flag_extraction", "description": "Extract flag from decrypted data"}
            ],
            "pwn": [
                {"step": 1, "action": "binary_analysis", "description": "Analyze binary protections and architecture"},
                {"step": 2, "action": "vulnerability_discovery", "description": "Find exploitable vulnerabilities"},
                {"step": 3, "action": "exploit_development", "description": "Develop exploit payload"},
                {"step": 4, "action": "local_testing", "description": "Test exploit locally"},
                {"step": 5, "action": "remote_exploitation", "description": "Execute exploit against remote target"},
                {"step": 6, "action": "shell_interaction", "description": "Interact with gained shell to find flag"}
            ],
            "forensics": [
                {"step": 1, "action": "file_analysis", "description": "Analyze provided files and their properties"},
                {"step": 2, "action": "data_recovery", "description": "Recover deleted or hidden data"},
                {"step": 3, "action": "artifact_extraction", "description": "Extract relevant artifacts and evidence"},
                {"step": 4, "action": "timeline_reconstruction", "description": "Reconstruct timeline of events"},
                {"step": 5, "action": "correlation_analysis", "description": "Correlate findings across different sources"},
                {"step": 6, "action": "flag_discovery", "description": "Locate flag in recovered data"}
            ],
            "rev": [
                {"step": 1, "action": "static_analysis", "description": "Perform static analysis of the binary"},
                {"step": 2, "action": "dynamic_analysis", "description": "Run binary and observe behavior"},
                {"step": 3, "action": "algorithm_identification", "description": "Identify key algorithms and logic"},
                {"step": 4, "action": "key_extraction", "description": "Extract keys or important values"},
                {"step": 5, "action": "solution_implementation", "description": "Implement solution based on analysis"},
                {"step": 6, "action": "flag_generation", "description": "Generate or extract the flag"}
            ]
        }

        return workflows.get(challenge.category, [
            {"step": 1, "action": "analysis", "description": "Analyze the challenge"},
            {"step": 2, "action": "research", "description": "Research relevant techniques"},
            {"step": 3, "action": "implementation", "description": "Implement solution"},
            {"step": 4, "action": "testing", "description": "Test the solution"},
            {"step": 5, "action": "refinement", "description": "Refine approach if needed"},
            {"step": 6, "action": "flag_submission", "description": "Submit the flag"}
        ])

    def _analyze_description_complexity(self, description: str) -> float:
        """Analyze challenge description complexity to adjust time estimates"""
        complexity_score = 0.0
        description_lower = description.lower()

        # Length-based complexity
        if len(description) > 500:
            complexity_score += 0.3
        elif len(description) > 200:
            complexity_score += 0.1

        # Technical term density
        technical_terms = [
            "algorithm", "encryption", "decryption", "vulnerability", "exploit",
            "buffer overflow", "sql injection", "xss", "csrf", "authentication",
            "authorization", "cryptography", "steganography", "forensics",
            "reverse engineering", "binary analysis", "memory corruption",
            "heap", "stack", "rop", "shellcode", "payload"
        ]

        term_count = sum(1 for term in technical_terms if term in description_lower)
        complexity_score += min(0.4, term_count * 0.05)

        # Multi-step indicators
        multi_step_indicators = ["first", "then", "next", "after", "finally", "step"]
        step_count = sum(1 for indicator in multi_step_indicators if indicator in description_lower)
        complexity_score += min(0.3, step_count * 0.1)

        return min(1.0, complexity_score)