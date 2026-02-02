# Claude System Complete Structure (Final Restored v2)

This document organizes the core system components of the AI agent located at `~/.claude`. Integrates the full structure from PDF pages 90-91 and detailed folder contents from pages 92, 97, 98, 107.

---

## 1. Complete Folder Structure

| Folder              | Description                                               | Details      |
|---------------------|-----------------------------------------------------------|--------------|
| **agents**          | Individual agent persona and config data                  | -            |
| **archive**         | Archive of completed projects and old configs             | -            |
| **backups**         | Auto backups of system settings and core data             | -            |
| **cache**           | Temp data and search result cache for performance         | -            |
| **cheatsheets**     | Quick reference for commands and workflows                | -            |
| **chrome**          | Browser automation profiles and settings                  | -            |
| **commands**        | Custom commands and script executables                    | **[Detail]** |
| **debug**           | System error diagnosis and debug logs                     | -            |
| **docs**            | System operation guides and detailed manuals              | **[Detail]** |
| **error-kb**        | Error knowledge base (pending, resolved, patterns)        | -            |
| **file-history**    | File change history and version control data              | -            |
| **hooks**           | Automation hooks triggered on specific events             | -            |
| **ide**             | IDE (VS Code etc.) integration settings and plugins       | -            |
| **jarvis**          | Jarvis system core logic and state management             | -            |
| **logs**            | Agent activity and system execution logs                  | -            |
| **mcp-router**      | MCP server connection and routing config                  | -            |
| **output-styles**   | Markdown/PDF/HTML style templates for output              | -            |
| **patterns**        | Recurring code structures and solution patterns           | -            |
| **personas**        | 27+ professional persona definitions                      | -            |
| **plans**           | Project planning and execution plan data                  | -            |
| **plugins**         | External plugins extending system functionality           | -            |
| **profiles**        | User/purpose-specific environment profiles                | -            |
| **projects**        | Metadata for currently managed projects                   | -            |
| **prompts**         | System prompts and template collection                    | -            |
| **references**      | External data/formats for research and analysis           | **[Detail]** |
| **scripts**         | Various scripts for system automation                     | -            |
| **session-env**     | Per-session environment variables and state               | -            |
| **sessions**        | Conversation session history and context data             | -            |
| **shell-snapshots** | Shell execution state and environment snapshots           | -            |
| **skills**          | Agent special function definitions (research, prd-create) | -            |
| **statsig**         | Feature flags and experimental settings                   | -            |
| **telemetry**       | System usage stats and performance monitoring             | -            |
| **templates**       | Standard templates for document and code generation       | -            |
| **todos**           | Project and session-level todo list management            | -            |

---

## 2. Detailed Folder Contents

### 2.1 `docs` Folder (PDF p.92)
Documents defining core system principles and workflows.

* **ARCH-PRINCIPLES.md**: System architecture design principles
* **DOC-TEMPLATE.md**: Standard document template
* **HOOKS-SYSTEM.md**: Hook system operation and config
* **PERSONAS.md**: Persona system definition and usage guide
* **PLAN-MODE.md**: Strategic plan mode detailed guide
* **PRD-WORKFLOW.md**: PRD writing workflow
* **PROJECT-CONTEXT.md**: Project context management strategy
* **PROJECT-PLANNING.md**: Project planning and phase analysis guide
* **QUALITY-GATES.md**: Code and deliverable quality criteria
* **SETTINGS-GUIDE.md**: System settings detailed manual
* **VERSION-POLICY.md**: Version management and release policy
* **VIBE-WORKFLOW.md**: Vibe (tone/manner) management workflow
* **WRITER-REVIEWER-SYSTEM.md**: Writer-reviewer loop system definition

### 2.2 `commands` Folder (PDF p.97)
Execution commands and scripts controlling agent behavior.

* **sc/**: Sub-command folder (see 2.3)
* **code-with-review.md**: Code generation with review command
* **error-search.md**: Error analysis and solution search command
* **i.md**: Immediate info query or interaction command
* **project-continue.md**: Resume interrupted project
* **project-plan.md**: Project plan creation command
* **project-status.md**: Current project status check
* **recover.md**: System or session recovery command
* **vibe.md**: Current session vibe settings check

### 2.3 `commands/sc` Folder (PDF p.98)
Detailed execution units for specific tasks.

* **analyze.md**, **build.md**, **cleanup.md**, **design.md**, **document.md**, **estimate.md**, **explain.md**, **git.md**, **implement.md**, **improve.md**, **index.md**, **load.md**, **spawn.md**, **task.md**, **test.md**, **troubleshoot.md**, **workflow.md**

### 2.4 `references` Folder (PDF p.107)
External libraries, SDKs, and guides for research and development.

* **claude-agent-sdk-typescript**: TypeScript Claude Agent SDK reference
* **claude-code-action**: Claude code action definitions and examples
* **claude-code-security-review**: Code security review guide and checklist
* **claude-cookbooks**: Cookbook recipes with various implementations
* **claude-quickstarts**: Quick start tutorials and sample projects
* **devcontainer-features**: Dev container environment setup reference
* **rhi-rhf**: RHI/RHF technical reference data

---

## 3. Core Files (Root)

| File                          | Description                                         |
|-------------------------------|-----------------------------------------------------|
| **.credentials.json**         | External API and service auth info (encrypted)      |
| **superclaude-metadata.json** | System-wide metadata and version info               |
| **AGENTS.md**                 | Active agent list and role definitions              |
| **CLAUDE.md**                 | Project-specific core directives and workflow       |
| **CLAUDE_SKILLS_GUIDE.md**    | Skill usage and extension guide                     |
| **CONTEXT-MANAGER.md**        | Context window management and DCP strategy          |
| **history.json**              | Full execution history and timeline data            |
| **INSTALLED_SKILLS.md**       | Currently installed skills list and status          |
| **KEYWORD-TRIGGERS.md**       | Automation trigger keywords and action definitions  |
| **mcp.json**                  | MCP server config and connection details            |
| **SESSION-MANAGER.md**        | Session persistence and recovery strategy           |
| **settings.json**             | Global system settings file                         |
| **settings.local.json**       | Local environment override settings                 |
| **stats-cache.json**          | Statistics data cache file                          |
| **WRITER-REVIEWER.md**        | Code quality review loop and weight settings        |
| **todo.md**                   | System-level integrated todo management             |
| **VERSION**                   | Current system version info file                    |
