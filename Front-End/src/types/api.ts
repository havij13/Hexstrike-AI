// API Response Types
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  timestamp: string
}

// Health Check
export interface HealthStatus {
  status: string
  timestamp: string
  version: string
  uptime: number
}

// Telemetry
export interface TelemetryData {
  cpu_usage: number
  memory_usage: number
  disk_usage: number
  active_connections: number
  total_requests: number
  error_rate: number
}

// Process Management
export interface Process {
  pid: number
  command: string
  status: 'running' | 'completed' | 'failed' | 'paused'
  start_time: string
  runtime: string
  progress_percent: string
  progress_bar: string
  eta: string
  bytes_processed: number
  last_output: string
}

export interface ProcessListResponse {
  success: boolean
  active_processes: Record<string, Process>
  total_count: number
}

export interface ProcessDashboard {
  timestamp: string
  total_processes: number
  visual_dashboard: string
  processes: Process[]
  system_load: {
    cpu_percent: number
    memory_percent: number
    active_connections: number
  }
}

// AI Intelligence
export interface TargetProfile {
  target: string
  target_type: 'web_application' | 'network' | 'binary'
  risk_level: 'low' | 'medium' | 'high' | 'critical'
  confidence: number
  vulnerabilities: string[]
  recommendations: string[]
}

export interface AnalyzeTargetResponse {
  success: boolean
  target_profile: TargetProfile
  timestamp: string
}

export interface ToolSelection {
  tool_name: string
  priority: number
  parameters: Record<string, any>
  estimated_duration: number
  success_probability: number
}

export interface SelectToolsResponse {
  success: boolean
  target: string
  objective: string
  target_profile: TargetProfile
  selected_tools: ToolSelection[]
  tool_count: number
  timestamp: string
}

export interface OptimizeParametersResponse {
  success: boolean
  target: string
  tool: string
  context: Record<string, any>
  target_profile: TargetProfile
  optimized_parameters: Record<string, any>
  timestamp: string
}

// Cache Management
export interface CacheStats {
  cache_size: number
  cache_usage: number
  hit_rate: number
  miss_rate: number
  evictions: number
}

export interface ClearCacheResponse {
  success: boolean
  message: string
  cleared_entries: number
}

// Error Handling
export interface ErrorStatistics {
  total_errors: number
  error_counts_by_type: Record<string, number>
  error_counts_by_tool: Record<string, number>
  recent_errors_count: number
  recent_errors: Array<{
    tool: string
    error_type: string
    timestamp: string
  }>
}

export interface ErrorStatsResponse {
  success: boolean
  statistics: ErrorStatistics
  timestamp: string
}

// File Operations
export interface FileInfo {
  name: string
  size: number
  modified: string
  type: 'file' | 'directory'
}

export interface FileListResponse {
  success: boolean
  files: FileInfo[]
  total_count: number
}

// Tool Count
export interface ToolCountResponse {
  total_tools: number
  categories: Record<string, string[]>
  ai_agents: number
  version: string
}

// Tool Execution
export interface ToolExecution {
  execution_time: number
  success: boolean
  output: string
  error?: string
  warnings?: string[]
  metadata?: Record<string, any>
}

export interface NmapExecution extends ToolExecution {
  ports: Array<{
    port: number
    state: string
    service: string
    version?: string
  }>
  host_status: string
  scan_type: string
}

export interface GobusterExecution extends ToolExecution {
  directories_found: string[]
  files_found: string[]
  total_requests: number
  response_codes: Record<string, number>
}

// Command Execution
export interface CommandExecution {
  execution_time: number
  success: boolean
  output: string
  exit_code: number
  duration: number
  cached: boolean
}

// Tool-specific execution types
export interface RustscanExecution extends ToolExecution {
  open_ports: Array<{
    port: number
    state: string
    service: string
    version?: string
  }>
  scan_summary: string
}

export interface MasscanExecution extends ToolExecution {
  open_ports: Array<{
    port: number
    state: string
    service?: string
  }>
  scan_summary: string
  rate: number
}

export interface FeroxbusterExecution extends ToolExecution {
  found_directories: string[]
  found_files: string[]
  total_requests: number
  status_codes: Record<string, number>
}

export interface NucleiExecution extends ToolExecution {
  vulnerabilities: Array<{
    template_id: string
    name: string
    severity: string
    description: string
    url: string
    matched_at: string
  }>
  total_vulnerabilities: number
}

export interface FFufExecution extends ToolExecution {
  discovered_urls: string[]
  total_requests: number
  status_codes: Record<string, number>
  wordlist_size: number
}

export interface NiktoExecution extends ToolExecution {
  vulnerabilities_found: Array<{
    id: string
    severity: string
    description: string
  }>
  services_detected: string[]
  tests_performed: number
}

export interface HydraExecution extends ToolExecution {
  successful_logins: Array<{
    username: string
    password: string
    service: string
  }>
  attempts_made: number
  successful_cracks: number
}

export interface JohnExecution extends ToolExecution {
  cracked_hashes: Array<{
    hash: string
    password: string
    hash_type: string
  }>
  attempts_made: number
  success_rate: number
}

export interface HashcatExecution extends ToolExecution {
  cracked_hashes: Array<{
    hash: string
    password: string
    hash_type: string
  }>
  attempts_made: number
  crack_time: string
}

export interface SQLMapExecution extends ToolExecution {
  injection_points: Array<{
    parameter: string
    type: string
    payload: string
  }>
  databases_found: string[]
  tables_dumped: number
}

export interface WPScanExecution extends ToolExecution {
  wordpress_version: string
  plugins_detected: Array<{
    name: string
    version: string
    vulnerabilities: string[]
  }>
  themes_detected: Array<{
    name: string
    version: string
  }>
  users_found: string[]
}

export interface DalfoxExecution extends ToolExecution {
  xss_found: Array<{
    parameter: string
    payload: string
    url: string
  }>
  blind_xss_detected: boolean
  poc_urls: string[]
}

// Network Reconnaissance Tools
export interface AmassExecution extends ToolExecution {
  subdomains_found: string[]
  ip_addresses: string[]
  total_discovered: number
}

export interface SubfinderExecution extends ToolExecution {
  subdomains: string[]
  total_discovered: number
}

export interface FierceExecution extends ToolExecution {
  dns_records: Array<{
    type: string
    name: string
    value: string
  }>
  subdomains_found: string[]
}

export interface DNSenumExecution extends ToolExecution {
  dns_records: Record<string, string[]>
  subdomains: string[]
  total_found: number
}

export interface AutoReconExecution extends ToolExecution {
  services_detected: string[]
  open_ports: number[]
  vulnerabilities: string[]
}

export interface Enum4linuxExecution extends ToolExecution {
  shares_found: string[]
  users_found: string[]
  groups_found: string[]
}

export interface ResponderExecution extends ToolExecution {
  hashes_captured: string[]
  authentication_events: number
}

export interface SMBmapExecution extends ToolExecution {
  shares: Array<{
    name: string
    path: string
    permissions: string
  }>
  accessible_shares: number
}

export interface RPCClientExecution extends ToolExecution {
  commands_executed: string[]
  results: string[]
}

export interface NBtscanExecution extends ToolExecution {
  hosts_found: Array<{
    ip: string
    netbios_name: string
    mac_address: string
  }>
}

export interface ARPScanExecution extends ToolExecution {
  devices_found: Array<{
    ip: string
    mac: string
    vendor: string
  }>
}

export interface NmapAdvancedExecution extends ToolExecution {
  detailed_scan_results: {
    os_detection: string
    services: Array<{
      port: number
      service: string
      version: string
    }>
  }
}

// Cloud Security Tools
export interface ProwlerExecution extends ToolExecution {
  findings: Array<{
    check_id: string
    status: string
    severity: string
    description: string
  }>
  total_findings: number
  failed_checks: number
}

export interface TrivyExecution extends ToolExecution {
  vulnerabilities: Array<{
    id: string
    severity: string
    package: string
    description: string
  }>
  total_vulnerabilities: number
}

export interface KubeHunterExecution extends ToolExecution {
  vulnerabilities: Array<{
    category: string
    description: string
    severity: string
  }>
  total_issues: number
}

export interface ScoutSuiteExecution extends ToolExecution {
  findings: Array<{
    service: string
    issue: string
    severity: string
  }>
  total_findings: number
}

export interface CloudMapperExecution extends ToolExecution {
  network_map: Record<string, any>
  security_issues: string[]
}

export interface PacuExecution extends ToolExecution {
  modules_executed: string[]
  results: Record<string, any>
}

export interface KubeBenchExecution extends ToolExecution {
  test_results: Array<{
    id: string
    description: string
    status: string
  }>
  passed: number
  failed: number
}

export interface DockerBenchSecurityExecution extends ToolExecution {
  checks: Array<{
    id: string
    description: string
    status: string
  }>
  passed: number
  failed: number
}

export interface ClairExecution extends ToolExecution {
  vulnerabilities: Array<{
    id: string
    severity: string
    package: string
  }>
}

export interface FalcoExecution extends ToolExecution {
  events: Array<{
    timestamp: string
    rule: string
    priority: string
  }>
}

export interface CheckovExecution extends ToolExecution {
  violations: Array<{
    check_id: string
    severity: string
    resource: string
  }>
}

export interface TerrascanExecution extends ToolExecution {
  violations: Array<{
    rule_id: string
    severity: string
    description: string
  }>
}

// Binary Analysis Tools
export interface GhidraExecution extends ToolExecution {
  functions_analyzed: number
  strings_found: string[]
  decompiled_code: string
}

export interface Radare2Execution extends ToolExecution {
  functions: string[]
  strings: string[]
  analysis_complete: boolean
}

export interface GDBExecution extends ToolExecution {
  breakpoints_set: number
  variables_examined: string[]
  stack_trace: string[]
}

export interface BinwalkExecution extends ToolExecution {
  files_found: Array<{
    offset: number
    type: string
    description: string
  }>
}

export interface ChecksecExecution extends ToolExecution {
  protections: {
    nx: boolean
    pie: boolean
    relro: boolean
    canary: boolean
  }
  vulnerabilities: string[]
}

export interface ROPGadgetExecution extends ToolExecution {
  gadgets_found: number
  rop_chains: string[]
}

export interface XXDExecution extends ToolExecution {
  hexdump: string
  length: number
}

export interface StringsExecution extends ToolExecution {
  strings_found: string[]
  total_strings: number
}

export interface ObjdumpExecution extends ToolExecution {
  disassembly: string
  sections: string[]
}

export interface PwntoolsExecution extends ToolExecution {
  exploit_developed: boolean
  shellcode: string
}

export interface OneGadgetExecution extends ToolExecution {
  gadgets_found: Array<{
    offset: string
    constraints: string[]
  }>
}

export interface LibcDatabaseExecution extends ToolExecution {
  symbols_matched: string[]
  libc_identified: string
}

export interface GDBPEDAExecution extends ToolExecution {
  analysis_complete: boolean
  exploits_suggested: string[]
}

export interface AngrExecution extends ToolExecution {
  paths_explored: number
  satisfiable_paths: number
}

export interface RopperExecution extends ToolExecution {
  rop_chains: string[]
  gadgets_found: number
}

export interface PwnInitExecution extends ToolExecution {
  library_loaded: boolean
  exploit_template: string
}

// Forensics Tools
export interface VolatilityExecution extends ToolExecution {
  processes: Array<{
    pid: number
    name: string
    start_time: string
  }>
  network_connections: string[]
}

export interface Volatility3Execution extends ToolExecution {
  plugins_executed: string[]
  artifacts_found: string[]
}

export interface ForemostExecution extends ToolExecution {
  files_recovered: Array<{
    filename: string
    size: number
    type: string
  }>
}

export interface StegHideExecution extends ToolExecution {
  hidden_data_extracted: boolean
  output_file: string
}

export interface ExifToolExecution extends ToolExecution {
  metadata: Record<string, string>
  gps_data?: {
    latitude: number
    longitude: number
  }
}

export interface HashPumpExecution extends ToolExecution {
  signature_forged: boolean
  new_hash: string
}

// Exploitation Tools
export interface MetasploitExecution extends ToolExecution {
  exploit_executed: boolean
  sessions_created: number
}

export interface MSFVenomExecution extends ToolExecution {
  payload_generated: boolean
  payload_size: number
}

// Additional Web Security Tools
export interface GAUExecution extends ToolExecution {
  urls_found: string[]
  total_urls: number
}

export interface WaybackurlsExecution extends ToolExecution {
  historical_urls: string[]
  total_found: number
}

export interface ArjunExecution extends ToolExecution {
  parameters_discovered: string[]
  total_parameters: number
}

export interface ParamspiderExecution extends ToolExecution {
  parameters_found: string[]
  urls_processed: number
}

export interface JaelesExecution extends ToolExecution {
  vulnerabilities: Array<{
    name: string
    severity: string
    url: string
  }>
}

export interface HakrawlerExecution extends ToolExecution {
  endpoints_found: string[]
  forms_discovered: string[]
}

export interface DotDotPwnExecution extends ToolExecution {
  vulnerabilities_found: Array<{
    path: string
    type: string
  }>
}

export interface XSSerExecution extends ToolExecution {
  xss_payloads: string[]
  vulnerable_urls: string[]
}

export interface WFuzzExecution extends ToolExecution {
  discovered_paths: string[]
  response_codes: Record<number, number>
}

export interface HTTPFrameworkExecution extends ToolExecution {
  requests_sent: number
  responses_received: number
}

export interface BrowserAgentExecution extends ToolExecution {
  screenshots_captured: number
  interactions_performed: number
}

export interface BurpsuiteAlternativeExecution extends ToolExecution {
  requests_intercepted: number
  vulnerabilities_detected: string[]
}

export interface ZAPExecution extends ToolExecution {
  alerts: Array<{
    severity: string
    name: string
    url: string
  }>
  total_alerts: number
}

export interface WafW00fExecution extends ToolExecution {
  waf_detected: boolean
  waf_name?: string
  bypass_methods?: string[]
}

export interface JWTAnalyzerExecution extends ToolExecution {
  vulnerabilities: string[]
  jwt_decoded: Record<string, any>
}

export interface APISchemaAnalyzerExecution extends ToolExecution {
  endpoints_analyzed: number
  security_issues: string[]
}

export interface APIFuzzerExecution extends ToolExecution {
  endpoints_tested: string[]
  vulnerabilities: string[]
}

export interface GraphQLScannerExecution extends ToolExecution {
  schema_introspected: boolean
  vulnerabilities: string[]
}

export interface MedusaExecution extends ToolExecution {
  successful_logins: Array<{
    username: string
    password: string
  }>
  attempts_made: number
}

export interface NetExecExecution extends ToolExecution {
  hosts_compromised: string[]
  commands_executed: string[]
}

export interface HTTPxExecution extends ToolExecution {
  endpoints_discovered: string[]
  technologies: string[]
}

export interface AnewExecution extends ToolExecution {
  new_lines_added: number
  duplicates_removed: number
}

export interface QSReplaceExecution extends ToolExecution {
  modified_urls: string[]
  total_modified: number
}

export interface UroExecution extends ToolExecution {
  unique_urls: string[]
  total_unique: number
}

export interface X8Execution extends ToolExecution {
  servers_analyzed: number
  issues_found: string[]
}
