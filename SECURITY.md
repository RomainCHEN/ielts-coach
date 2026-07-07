# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in IELTS Coach, please report it via
[GitHub Security Advisories](https://github.com/RomainCHEN/ielts-coach/security/advisories/new)
rather than opening a public issue.

**Please do NOT disclose the vulnerability publicly** until it has been addressed.

## Scope

This security policy applies to:

- The `vision_mcp_server.py` MCP server (API key handling, image data transmission)
- State file management (`state_manager.py`)
- Any script that processes user credentials or personal data

## What We Care About

- **API key exposure:** The vision bridge MCP server reads API keys from environment variables. It must never log, persist, or transmit keys beyond the intended vision API endpoint.
- **Image data privacy:** Chart images sent through the vision bridge are transmitted to the configured vision model provider only. They are not stored locally beyond the original file path.
- **State file integrity:** JSON state files contain user preferences and progress data. Malformed files should be handled gracefully.

## Supported Versions

| Version | Supported |
|---------|-----------|
| v2.x    | ✅ Active |
| v1.x    | ❌ End of life |

## Best Practices for Users

- Never commit `user_profile.json`, `study_plan.json`, or `progress.json` to public repos
- Use environment variables (not hardcoded strings) for API keys
- Rotate API keys periodically
- Review `.gitignore` to ensure auto-generated state files are excluded
