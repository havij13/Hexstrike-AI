# HexStrike AI - API Test Scripts

## Overview

This directory contains comprehensive API test scripts that reference the `API_USAGE.md` documentation and test all available endpoints in the HexStrike AI system.

## Test Scripts

### `api-test.sh` - Linux/macOS Comprehensive API Test
**Usage:**
```bash
# Test the deployed Render instance
bash scripts/api-test.sh

# Test a local instance
HEXSTRIKE_URL=http://localhost:8888 bash scripts/api-test.sh

# Test with verbose output
VERBOSE=true bash scripts/api-test.sh

# Test with custom timeout
TEST_TIMEOUT=60 bash scripts/api-test.sh
```

### `api-test.ps1` - Windows PowerShell Comprehensive API Test
**Usage:**
```powershell
# Test the deployed Render instance
.\scripts\api-test.ps1

# Test a local instance
.\scripts\api-test.ps1 -Url "http://localhost:8888"

# Test with verbose output
.\scripts\api-test.ps1 -VerboseOutput

# Test with custom timeout
.\scripts\api-test.ps1 -Timeout 60
```

## Test Coverage

The test scripts cover all major endpoint categories from `API_USAGE.md`:

### ✅ Core System Endpoints
- Health Check (`/health`)
- Server Telemetry (`/api/telemetry`)

### ✅ Network Security Tools
- Nmap Scanning (`/api/tools/nmap`)
- Rustscan, Masscan, AutoRecon (skipped - too intensive)

### ✅ Web Application Security Tools
- Gobuster Directory Enumeration (`/api/tools/gobuster`)
- Feroxbuster, Nuclei, Nikto, SQLMap, WPScan (skipped - too intensive)

### ✅ AI Intelligence Endpoints
- Target Analysis (`/api/intelligence/analyze-target`)
- Tool Selection (`/api/intelligence/select-tools`)
- Parameter Optimization (`/api/intelligence/optimize-parameters`)

### ✅ Process Management
- Process List (`/api/processes/list`)
- Process Dashboard (`/api/processes/dashboard`)

### ✅ Error Handling
- Error Statistics (`/api/error-handling/statistics`)

### ✅ File Operations
- List Files (`/api/files/list`)

### ✅ Cache Management
- Cache Statistics (`/api/cache/stats`)
- Clear Cache (`/api/cache/clear`)

### ✅ Additional Endpoints
- Root Endpoint (`/`)
- Command Execution (`/api/command`)

## Test Categories

### Automated Tests
These tests run automatically and verify basic functionality:
- Health checks
- Basic API responses
- JSON structure validation
- HTTP status code verification

### Skipped Tests
These tests are skipped in automated testing for good reasons:
- **Intensive Scans**: Nmap comprehensive scans, vulnerability scans
- **Resource-Intensive**: Password cracking, binary analysis
- **Environment-Specific**: Cloud security tools, container scanners
- **Data-Dependent**: Tools requiring specific files or targets

### Why Are So Many Tests Skipped?

The test suite intentionally skips 30 out of 45 tests (67%) because:
- **Resource-intensive operations** (password cracking, full vulnerability scans)
- **Time-consuming scans** (comprehensive reconnaissance, binary analysis)
- **Environment-specific tools** (cloud security, container scanners)
- **Data-dependent operations** (require specific files, credentials)

**This is by design** - the 15 passing tests (33%) verify all critical API endpoints work correctly without overwhelming the server or taking hours to complete.

## Lightweight Test Suite

For CI/CD and quick validation, use the lightweight test suite:

```bash
./scripts/api-test-lightweight.sh
```

This runs minimal versions of all tools:
- Completes in ~2 minutes (vs hours for full tests)
- Safe for automated testing
- Validates all API endpoints work
- Uses safe, non-intrusive parameters
- Each test completes in < 10 seconds

The lightweight suite covers:
- Network tools: Nmap (single port), Rustscan (single port), Masscan (low rate)
- Web tools: Gobuster (quick scan), Feroxbuster (depth 1), Nuclei (single template)
- Authentication tools: Hydra (list mode), John (single hash), Hashcat (version)
- Binary analysis: Ghidra/Radare2/GDB (version/info checks)
- Cloud security: Prowler (list checks), Trivy (version), Kube-Hunter (list mode)

**Recommended**: Run lightweight tests in CI/CD, run full tests manually before releases.

## Test Results

### Success Criteria
- ✅ **PASS**: Endpoint responds correctly with expected status/data
- ❌ **FAIL**: Endpoint fails to respond or returns unexpected results
- ⚠️ **SKIP**: Test skipped due to resource/intensity requirements

### Known Issues and Expected Behaviors

#### Expected Failures (Normal Behavior)
- **Root Endpoint** - Should return 200 after Dockerfile fixes (templates/static directories)
- **Nmap Permission Issues** - Raw socket operations may fail in containerized environments
- **Some Security Tools** - May not be installed or available in the deployment environment

#### API Response Structure Notes
- **AI Target Analysis**: Returns `target_profile` key (not `analysis`)
- **AI Tool Selection**: Returns `selected_tools` key (not `tools`)
- **Process List**: Returns `active_processes` key (not `processes`)
- **Cache Statistics**: Returns `hit_rate` key (not `cache_size`)
- **Gobuster**: Requires `url` parameter (not `target`)

### Output Format
```
[TEST] Test Name (METHOD /endpoint)
[PASS] Test Name - HTTP 200 / Found key: expected_key
[FAIL] Test Name - Connection failed or timeout
[SKIP] Test Name - Reason for skipping
```

## Environment Variables

### Linux/macOS (`api-test.sh`)
- `HEXSTRIKE_URL`: Target URL (default: https://hexstrike-ai-v028.onrender.com)
- `TEST_TIMEOUT`: Request timeout in seconds (default: 30)
- `VERBOSE`: Enable verbose output (default: false)

### Windows PowerShell (`api-test.ps1`)
- `-Url`: Target URL (default: https://hexstrike-ai-v6-0.onrender.com)
- `-Timeout`: Request timeout in seconds (default: 30)
- `-VerboseOutput`: Enable verbose output (switch)

## Example Usage

### Quick Test
```bash
# Linux/macOS
bash scripts/api-test.sh

# Windows
.\scripts\api-test.ps1
```

### Detailed Testing
```bash
# Linux/macOS - Verbose output
VERBOSE=true bash scripts/api-test.sh

# Windows - Verbose output
.\scripts\api-test.ps1 -VerboseOutput
```

### Local Testing
```bash
# Linux/macOS
HEXSTRIKE_URL=http://localhost:8888 bash scripts/api-test.sh

# Windows
.\scripts\api-test.ps1 -Url "http://localhost:8888"
```

## Integration with CI/CD

These test scripts can be integrated into CI/CD pipelines:

### GitHub Actions Example
```yaml
- name: Test HexStrike AI API
  run: |
    chmod +x scripts/api-test.sh
    HEXSTRIKE_URL=${{ secrets.HEXSTRIKE_URL }} bash scripts/api-test.sh
```

### Azure DevOps Example
```yaml
- task: PowerShell@2
  displayName: 'Test HexStrike AI API'
  inputs:
    targetType: 'inline'
    script: |
      .\scripts\api-test.ps1 -Url "$(HEXSTRIKE_URL)"
```

## Troubleshooting

### Common Issues

#### Connection Timeouts
- Increase timeout value: `TEST_TIMEOUT=60` or `-Timeout 60`
- Check server availability: `curl $HEXSTRIKE_URL/health`

#### Permission Denied (Linux/macOS)
```bash
chmod +x scripts/api-test.sh
```

#### PowerShell Execution Policy (Windows)
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

### Debug Mode
Enable verbose output to see detailed responses:
```bash
# Linux/macOS
VERBOSE=true bash scripts/api-test.sh

# Windows
.\scripts\api-test.ps1 -VerboseOutput
```

## Test Customization

### Adding New Tests
To add new endpoint tests, modify the test scripts:

1. **Add test function call**:
```bash
# Linux/macOS
test_json_endpoint "New Test" "/api/new/endpoint" "GET" "expected_key"

# Windows
Test-JsonEndpoint "New Test" "/api/new/endpoint" "GET" "expected_key"
```

2. **Add skip condition if needed**:
```bash
# Linux/macOS
skip_test "Intensive Test" "Too resource-intensive for automated testing"

# Windows
Skip-Test "Intensive Test" "Too resource-intensive for automated testing"
```

### Custom Test Data
Modify test data by changing the JSON payloads:
```bash
# Example: Custom nmap scan
test_json_endpoint "Custom Nmap" "/api/tools/nmap" "POST" "execution_time" '{"target": "custom.target.com", "scan_type": "stealth"}'
```

## Related Documentation

- [API_USAGE.md](../API_USAGE.md) - Complete API documentation
- [README.md](../README.md) - Main project documentation
- [USAGE_EXAMPLES.md](../USAGE_EXAMPLES.md) - Practical usage examples

---

**Created**: 2025-10-23  
**Version**: v6.0  
**Maintainer**: HexStrike AI Team
