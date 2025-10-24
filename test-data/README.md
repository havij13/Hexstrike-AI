# Test Data Directory

This directory contains sample data for testing HexStrike AI security tools.

## Directory Structure

```
test-data/
├── binaries/           # Binary files for reverse engineering tools
├── hashes/            # Password hashes for cracking tools
├── wordlists/         # Custom wordlists for enumeration
├── targets/           # Safe testing targets configuration
└── forensics/         # Forensic analysis files
```

## Usage Guidelines

### ⚠️ Important Security Notice

- **ONLY use these test files for educational and testing purposes**
- **DO NOT use real passwords or sensitive data**
- **Always test on systems you own or have explicit permission to test**
- **Follow responsible disclosure practices**

### Safe Testing Targets

The `targets/` directory contains pre-configured safe testing targets:

- **web-targets.json**: Web applications safe for testing
- **network-targets.json**: Network hosts safe for scanning

### Test Data Files

#### Binary Analysis (`binaries/`)
- Sample ELF file headers for testing reverse engineering tools
- Safe for educational purposes

#### Password Cracking (`hashes/`)
- Example MD5 and SHA256 hashes
- Common password examples for testing
- **DO NOT use in production environments**

#### Wordlists (`wordlists/`)
- Common directories and files for enumeration
- Basic password lists for testing
- Custom wordlists for specific tools

#### Forensic Files (`forensics/`)
- Sample files for forensic analysis tools
- Safe for educational purposes

## Tool Integration

These test files are designed to work with:

- **Network Security Tools**: Nmap, Rustscan, Masscan
- **Web Application Tools**: Gobuster, Feroxbuster, Nuclei
- **Authentication Tools**: Hydra, John the Ripper, Hashcat
- **Binary Analysis Tools**: Ghidra, Radare2, GDB
- **Cloud Security Tools**: Prowler, Trivy, Kube-Hunter

## Legal and Ethical Considerations

1. **Only test on systems you own or have explicit permission to test**
2. **Respect rate limits and don't overwhelm target systems**
3. **Follow responsible disclosure if vulnerabilities are found**
4. **Document all testing activities**
5. **Use appropriate tools for the testing scope**

## Contributing

When adding new test data:

1. Ensure all data is safe and educational
2. Add appropriate documentation
3. Follow the existing directory structure
4. Include usage examples where applicable
