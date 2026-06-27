# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in ai-berkshire, please report it privately **before** creating a public issue.

**Contact**: **[xbtlin@gmail.com](mailto:xbtlin@gmail.com)**

We aim to:
- Acknowledge receipt within **48 hours**
- Provide a fix or mitigation within **14 days** for critical issues
- Coordinate public disclosure timing with the reporter

### What to Include
- Description of the vulnerability
- Steps to reproduce (minimal PoC)
- Affected versions and components
- Potential impact
- Any suggested fix (if available)

## Supported Versions

| Version | Supported |
|---------|-----------|
| latest  | ✅ Yes    |
| older   | ❌ No     |

## Security Measures

ai-berkshire is designed to be invoked by AI coding agents with natural language input.
This creates a unique security profile where traditional CLI argument validation
becomes a critical security boundary.

### For Users
- Run ai-berkshire in isolated environments (containers/VMs) when processing
  untrusted data from external sources
- Review skill definitions before execution — they define what the AI agent can do
- Keep dependencies updated (especially `yt-dlp`, `playwright`, and other upstream CLI tools)

### For Developers
- All file path arguments MUST be validated with `os.path.realpath()` + prefix check
- All bash command templates MUST quote interpolated variables
- User input (`$ARGUMENTS`) MUST NOT be embedded directly into prompts without
  input validation

## Scope

### In Scope
- Remote code execution via command injection in tool arguments
- Path traversal / arbitrary file access through file path parameters
- Credential or secret leakage through tool output or log files
- Prompt injection leading to tool/command boundary crossing
- Supply chain vulnerabilities in dependencies

### Out of Scope
- LLM prompt injection that does not cross a security boundary
  (e.g., the model outputs incorrect text but no tool/command is executed)
- Theoretical vulnerabilities without practical exploitation
- Dependency scanner findings without manual verification
- Social engineering of the project maintainers

## Disclosure Policy

1. Reporter submits details to [xbtlin@gmail.com](mailto:xbtlin@gmail.com)
2. Maintainer acknowledges receipt within 2 business days
3. Maintainer develops fix and notifies reporter
4. Fix is released; CVE is published
5. Public disclosure coordinated (typically 90-day window from notification)
6. Reporter is credited in the advisory (if desired)

## Credits

We appreciate responsible disclosure. Researchers who report valid security
issues will be credited in our security advisories and release notes.

---

*This SECURITY.md was contributed by AI4Sec Vulnerability Research Team as part of
a coordinated disclosure of CWE-22 path traversal vulnerabilities in this repository.*
