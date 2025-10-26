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
