---
name: related-work-matrix
description: "Builds/updates research/related_work_matrix.md: papers x dimensions (formulation, state space, reward, evaluation) from the research wiki, the gaps it exposes, and hooks for the related-work section. Use when the user says \"related work matrix\", \"compare papers\", \"where is the gap\", \"update the matrix\", or during formulation."
argument-hint: "[topic | arXiv ids/paper slugs to add | refresh]"
allowed-tools: Bash(*), Read, Write, Edit, Glob, Grep
---

# Related-Work Matrix

Request: $ARGUMENTS (empty/refresh = rebuild for the project topic)

## 0. Helper

```bash
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)" || exit 1
PY=python3; $PY -c "" 2>/dev/null || PY=python
ARIS_REPO="${ARIS_REPO:-$(awk -F'\t' '$1=="repo_root"{print $2; exit}' .aris/installed-skills.txt 2>/dev/null)}"
WIKI_SCRIPT=".aris/tools/research_wiki.py"
[ -f "$WIKI_SCRIPT" ] || { [ -n "${ARIS_REPO:-}" ] && WIKI_SCRIPT="$ARIS_REPO/tools/research_wiki.py"; }
```

## 1. Papers

1. Columns = the `## Dimensions` list in research/related_work_matrix.md.
2. Run `/research-wiki query "<topic from $ARGUMENTS or RESEARCH_BRIEF.md>"` (fallback: `"$PY" "$WIKI_SCRIPT" rebuild_query_pack research-wiki/`, read research-wiki/query_pack.md).
3. Candidates = papers named in the pack + papers in research-wiki/index.md tagged with the topic + papers in $ARGUMENTS.
4. Open only those research-wiki/papers/<slug>.md; read thesis, problem, method, results, assumptions, limitations.
5. Missing from the wiki → ingest first: `"$PY" "$WIKI_SCRIPT" ingest_paper research-wiki/ --arxiv-id <id>`.

## 2. Matrix

- One row per paper, sorted by year: `paper:<slug>` | year | one cell per dimension | key limitation (relative to our problem).
- Cells ≤12 words, from the paper page only; unknown = `?`.
- Last row `Ours` from STATUS.md / backlog.md Decided (blank if no idea chosen).
- Keep hand-written rows; change a cell only if the wiki contradicts it, and say so.

## 3. Gaps

`## Gaps`: empty/rare combinations of dimensions and shared limitations; one line each, with the rows that show it and a G-id (reuse research-wiki/gap_map.md ids; add new ones there). Mark the one we target `← ours`.

## 4. Hooks

`## Related-work hooks`: 3–6 bullets, each a paragraph topic grouping rows by one dimension, citing `paper:<slug>`.

## 5. Record

Unpursued gap-ideas → Parked rows in research/backlog.md. Reply: rows count, gaps, papers with `?`.
