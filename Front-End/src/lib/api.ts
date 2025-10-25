import axios, { AxiosInstance, AxiosResponse } from 'axios'
import {
  ApiResponse,
  HealthStatus,
  TelemetryData,
  ProcessListResponse,
  ProcessDashboard,
  AnalyzeTargetResponse,
  SelectToolsResponse,
  OptimizeParametersResponse,
  CacheStats,
  ClearCacheResponse,
  ErrorStatsResponse,
  FileListResponse,
  ToolExecution,
  CommandExecution,
} from '@/types/api'

class HexStrikeApiClient {
  private client: AxiosInstance

  constructor(baseURL: string = process.env.NEXT_PUBLIC_HEXSTRIKE_API_URL || 'https://hexstrike-ai-v6-0.onrender.com') {
    this.client = axios.create({
      baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`)
        return config
      },
      (error) => {
        console.error('❌ API Request Error:', error)
        return Promise.reject(error)
      }
    )

    // Response interceptor
    this.client.interceptors.response.use(
      (response: AxiosResponse) => {
        console.log(`✅ API Response: ${response.status} ${response.config.url}`)
        return response
      },
      (error) => {
        console.error('❌ API Response Error:', error.response?.status, error.response?.data)
        return Promise.reject(error)
      }
    )
  }

  // Health Check
  async getHealth(): Promise<HealthStatus> {
    const response = await this.client.get<HealthStatus>('/health')
    return response.data
  }

  // Telemetry
  async getTelemetry(): Promise<TelemetryData> {
    const response = await this.client.get<TelemetryData>('/api/telemetry')
    return response.data
  }

  // Process Management
  async getProcessList(): Promise<ProcessListResponse> {
    const response = await this.client.get<ProcessListResponse>('/api/processes/list')
    return response.data
  }

  async getProcessDashboard(): Promise<ProcessDashboard> {
    const response = await this.client.get<ProcessDashboard>('/api/processes/dashboard')
    return response.data
  }

  // AI Intelligence
  async analyzeTarget(target: string, analysisType: string = 'quick'): Promise<AnalyzeTargetResponse> {
    const response = await this.client.post<AnalyzeTargetResponse>('/api/intelligence/analyze-target', {
      target,
      analysis_type: analysisType,
    })
    return response.data
  }

  async selectTools(target: string, targetType: string = 'web', scanDepth: string = 'shallow'): Promise<SelectToolsResponse> {
    const response = await this.client.post<SelectToolsResponse>('/api/intelligence/select-tools', {
      target,
      target_type: targetType,
      scan_depth: scanDepth,
    })
    return response.data
  }

  async optimizeParameters(tool: string, target: string, scanType: string = 'quick'): Promise<OptimizeParametersResponse> {
    const response = await this.client.post<OptimizeParametersResponse>('/api/intelligence/optimize-parameters', {
      tool,
      target,
      scan_type: scanType,
    })
    return response.data
  }

  // Network Security Tools
  async nmapScan(target: string, scanType: string = 'quick', ports: string = '1-100'): Promise<ToolExecution> {
    const response = await this.client.post<ToolExecution>('/api/tools/nmap', {
      target,
      scan_type: scanType,
      ports,
    })
    return response.data
  }

  async gobusterScan(url: string, mode: string = 'dir', wordlist: string = '/usr/share/wordlists/dirb/common.txt'): Promise<ToolExecution> {
    const response = await this.client.post<ToolExecution>('/api/tools/gobuster', {
      url,
      mode,
      wordlist,
    })
    return response.data
  }

  // Cache Management
  async getCacheStats(): Promise<CacheStats> {
    const response = await this.client.get<CacheStats>('/api/cache/stats')
    return response.data
  }

  async clearCache(): Promise<ClearCacheResponse> {
    const response = await this.client.post<ClearCacheResponse>('/api/cache/clear')
    return response.data
  }

  // Error Handling
  async getErrorStatistics(): Promise<ErrorStatsResponse> {
    const response = await this.client.get<ErrorStatsResponse>('/api/error-handling/statistics')
    return response.data
  }

  // File Operations
  async getFileList(): Promise<FileListResponse> {
    const response = await this.client.get<FileListResponse>('/api/files/list')
    return response.data
  }

  // Command Execution
  async executeCommand(command: string): Promise<CommandExecution> {
    const response = await this.client.post<CommandExecution>('/api/command', {
      command,
    })
    return response.data
  }
}

// Export singleton instance
export const apiClient = new HexStrikeApiClient()
export default apiClient
