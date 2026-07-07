# Changelog

All notable changes to the IELTS Coach skill.

## [v2.0] — 2026-07-07

### Added
- **Progressive Topic Discovery** — structured 4-stage mini-interview per topic (Priming → Experience Mining → Content Confirmation → Generation)
- **Official Writing Band Descriptor alignment** — Task 1 & Task 2 calibrated against IELTS public descriptors (updated May 2023)
- **Anti-AI-Flavor Rules** — explicit screening for em dashes, mechanical linkers, cliché phrases, and other AI-generated text patterns
- **MCP Vision Bridge** — `vision_mcp_server.py` for non-vision models (DeepSeek etc.) via Alibaba Cloud Bailian qwen-vl or custom providers
- **Agent auto-configuration** — MCP setup is fully automated (pip install + settings.json editing), user only provides API key
- **Bilingual README** — split into `README.md` (English) and `README_zh.md` (Chinese) with mutual links
- **LICENSE** — standalone MIT license file
- **CONTRIBUTING.md** — contribution guidelines with commit conventions
- **SECURITY.md** — vulnerability reporting policy
- **CHANGELOG.md** — this file

### Changed
- **SKILL.md** — rewritten Step 2.3 (Topic Discovery), Step 2.4 (Writing formats + official criteria), new Image Recognition Fallback section
- **writing-resources.md** — replaced generic band requirements with official 4-criteria descriptor tables
- **writing-band-descriptors.md** — new reference file with full Band 5-9 Task 1 & Task 2 descriptors
- **README** — professional redesign with badges, TOC, comparison tables, workflow diagram, 4D personalization engine

### Removed
- `PRD.md`, `ielts_answers.html`, duplicate `references/question-bank.md` — personal/auto-generated files no longer tracked

## [v1.0] — 2026-07-06

### Added
- Initial release
- 102-topic question bank for May-August 2026
- Onboarding + Study Plan generation
- Band-calibrated model answers for Speaking Part 1/2/3 + Writing Task 1/2
- HTML output rendering
- JSON state management (user_profile, study_plan, progress)
- PDF extraction via PyMuPDF + MinerU API
