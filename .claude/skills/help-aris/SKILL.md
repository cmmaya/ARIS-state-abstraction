---
name: help-aris
description: "Explains how to use any skill in this repo (ARIS or custom) in the context of this project: what it does, setup it needs and whether that's done, syntax and options, examples, files it reads/writes, how it connects to STATUS/backlog/wiki/results macros, and what comes before/after. Also recommends skills for a goal, and explains how to create a new custom skill. Use when the user says \"/help-aris\", \"how do I use /x\", \"which skill should I use to…\", \"help with ARIS\", \"how do I make a skill\"."
argument-hint: "[skill-name | goal in words | new <skill idea> | (empty = overview)]"
allowed-tools: Read, Glob, Grep, Bash(ls:*), Bash(claude mcp list:*), Bash(printenv:*), Bash(awk:*), Bash(test:*)
---

# Help ARIS

Request: $ARGUMENTS

Read-only: never edit files (except Mode D after the user approves). Answer in the user's language.

## Sources (open only what the mode needs)

- G = docs/GUIDE.md (this repo's guide). Grep it for the skill/topic with context first; read whole only in Mode A.
- S = .claude/skills/<name>/SKILL.md (works for ARIS junctions and custom skills).
- R = ARIS repo root: `awk -F'\t' '$1=="repo_root"{print $2}' .aris/installed-skills.txt`.
  - R/tools/skill-groups.tsv: catalog (`skill<TAB>name<TAB>group<TAB>requires<TAB>short-desc`, descriptions in Chinese; translate).
  - R/docs/SKILLS_CATALOG.md, R/README.md (grep `### Workflow`, `Research Wiki`, `9. ⚙️ Setup` sections), R/docs/PROJECT_FILES_GUIDE.md, R/docs/GPU_SETUP.md, R/docs/CUSTOMIZATION.md.
  - .claude/skills/shared-references/<file>.md when S links to one that matters for usage (e.g. reviewer-backends.md, effort-contract.md).
- CLAUDE.md rules (already in context) for how the skill must interact with our state files.

## Mode A: empty request → overview

From G §2, §4 and §8: the session loop (start/end/Friday), how to ask the wiki, the 8–10 most useful commands for the current stage (stage from CLAUDE.md Pipeline Status), and `/help-aris <skill>` / `/help-aris <goal>` usage. ≤ 25 lines.

## Mode B: a skill name (with or without `/`)

1. Read S fully. Unknown name → fuzzy-match names in .claude/skills/ and the catalog; suggest the closest 3.
2. Grep G and R/README.md for the name (±5 lines). Open referenced shared-references only if they define options or setup.
3. Check setup needed by S, without printing secrets:
   - Reviewer/Codex MCP (`mcp__codex`, "reviewer", "Codex"): run `claude mcp list`, report if `codex` is connected.
   - API keys named in S (e.g. EXA_API_KEY, GEMINI_API_KEY, S2_API_KEY): `test -n "$NAME"` → set / not set.
   - Wiki needed: `test -d research-wiki`. GPU/remote: whether CLAUDE.md Compute Budget is filled.
   - `requires` column in the catalog → list skills it calls.
4. Answer with this card (≤ 40 lines, no SKILL.md dump):

```
## /<name>: <one-line purpose>
**Use it when:** …            **Don't use it for:** … (point to the better skill)
**Setup:** ✅/❌ each requirement + the exact fix command (from G §0 or R/README) if missing
**Syntax:** /<name> "<arg>" — option: value …   (list options with defaults from S Constants / argument-hint)
**Examples (this project):**
  /<name> …     → what happens
  /<name> …     → what happens
**Reads:** files   **Writes:** files
**Our repo rules:** how it connects to STATUS / backlog (Decided/Discarded/Parked) / hypotheses / wiki / results macros, per CLAUDE.md
**Before → after:** previous skill → /<name> → next skill
**Gotchas:** cost/long runs, overwrites, Windows notes (python3 shim, admin for installer)
```

## Mode C: a goal in words ("compare my results", "find papers on X")

Match against catalog short descriptions + S descriptions (grep `description:` in .claude/skills/*/SKILL.md). Return the top 1–3 skills, one line each with why, then a Mode B card for the best one. Prefer our custom skills (stage-summarizer, related-work-matrix, weekly-report) when they fit.

## Mode D: `new <idea>` → create a custom skill

1. Check no existing skill covers it (Mode C). If one does, say so and stop.
2. Explain the repo conventions:
   - Folder `.claude/skills/<kebab-name>/SKILL.md`; frontmatter `name`, `description` (what + trigger phrases), `argument-hint`, `allowed-tools` (minimum needed).
   - Body terse, for the agent: numbered steps, exact files to read/write, no figures, ≤ ~60 lines.
   - Must follow CLAUDE.md rules (wiki query discipline, backlog rows, `\res…` macros).
   - Add `!.claude/skills/<name>/` to .gitignore (upstream skills are ignored by default), and a one-line rule in CLAUDE.md if it should trigger automatically.
   - Never edit ARIS junction skills in place; copy one to a new name if you want a variant (R/docs/CUSTOMIZATION.md).
3. Draft the SKILL.md in the reply. Write the files (skill, .gitignore line, CLAUDE.md rule, GUIDE §5 entry) only after the user approves.
